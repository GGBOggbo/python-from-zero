# ============================================================
# Day 20: 最终项目 — 轻量级模型服务监控系统
# 目标：整合 11-19 天所学，写一个完整的监控系统
# 用法：python day20.py 运行监控系统
# ============================================================

"""
轻量级模型服务监控系统
功能：
1. 定时检查 API 健康状态 (requests)
2. 定时采集 GPU 信息 (subprocess)
3. 定时检查 Docker 容器状态 (docker-py)
4. 异常自动重启容器
5. 告警推送到钉钉/企业微信 (webhook)
6. 日志记录 (logging)
7. 可配置的巡检间隔和告警阈值

依赖：pip install requests schedule docker
"""

import requests
import subprocess
import time
import json
import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# 尝试导入可选依赖
try:
    import docker
    HAS_DOCKER = True
except ImportError:
    HAS_DOCKER = False
    print("[提示] docker 未安装，容器监控功能不可用")

try:
    import schedule
    HAS_SCHEDULE = True
except ImportError:
    HAS_SCHEDULE = False
    print("[提示] schedule 未安装，使用简单循环代替")

# --------------------------------------------------
# 1. 配置
# --------------------------------------------------

CONFIG = {
    # 要监控的服务列表
    "services": [
        {"name": "vllm-qwen", "url": "http://localhost:8000/health", "type": "api"},
        {"name": "vllm-llama", "url": "http://localhost:8001/health", "type": "api"},
    ],
    # 告警配置
    "alert": {
        "dingtalk_url": "",  # 钉钉 Webhook URL
        "wechat_url": "",    # 企业微信 Webhook URL
        "gpu_temp_threshold": 85,    # GPU 温度告警阈值
        "cooldown_seconds": 300,     # 告警冷却时间
    },
    # 巡检间隔
    "interval": {
        "health_check": 30,    # 秒
        "gpu_check": 60,       # 秒
        "container_check": 60, # 秒
    },
    # 日志配置
    "log_file": "monitor.log",
}

# --------------------------------------------------
# 2. 日志模块
# --------------------------------------------------

def setup_logger(log_file="monitor.log"):
    """配置日志"""
    logger = logging.getLogger("monitor")
    logger.setLevel(logging.INFO)

    # 控制台输出
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
    ))
    logger.addHandler(console)

    # 文件输出（按天滚动，保留7天）
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", backupCount=7
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))
    logger.addHandler(file_handler)

    return logger

logger = setup_logger(CONFIG["log_file"])

# --------------------------------------------------
# 3. 告警模块
# --------------------------------------------------

class Alerter:
    """告警发送器（带冷却机制）"""

    def __init__(self, config):
        self.dingtalk_url = config.get("dingtalk_url", "")
        self.wechat_url = config.get("wechat_url", "")
        self.cooldown = config.get("cooldown_seconds", 300)
        self.last_alert = {}
        self.stats = {"sent": 0, "cooled": 0}

    def _check_cooldown(self, key):
        now = time.time()
        if key in self.last_alert and now - self.last_alert[key] < self.cooldown:
            self.stats["cooled"] += 1
            return False
        self.last_alert[key] = now
        return True

    def send(self, title, content):
        """发送告警到所有配置的渠道"""
        if not self._check_cooldown(title):
            logger.debug(f"告警冷却中: {title}")
            return False

        self.stats["sent"] += 1

        # 钉钉
        if self.dingtalk_url:
            try:
                requests.post(self.dingtalk_url, json={
                    "msgtype": "text",
                    "text": {"content": f"[模型监控] {content}"}
                }, timeout=5)
            except Exception:
                pass

        # 企业微信
        if self.wechat_url:
            try:
                requests.post(self.wechat_url, json={
                    "msgtype": "text",
                    "text": {"content": f"[模型监控] {content}"}
                }, timeout=5)
            except Exception:
                pass

        logger.warning(f"告警已发送: {content}")
        return True

alerter = Alerter(CONFIG["alert"])

# --------------------------------------------------
# 4. 健康检查模块 (requests)
# --------------------------------------------------

def check_api_health(services):
    """检查 API 服务健康状态"""
    results = []

    for svc in services:
        if svc["type"] != "api":
            continue

        try:
            resp = requests.get(svc["url"], timeout=5)
            healthy = resp.status_code == 200
            status = "正常" if healthy else f"异常({resp.status_code})"
        except requests.exceptions.ConnectionError:
            healthy = False
            status = "无法连接"
        except requests.exceptions.Timeout:
            healthy = False
            status = "超时"
        except Exception as e:
            healthy = False
            status = str(e)

        results.append({
            "name": svc["name"],
            "healthy": healthy,
            "status": status,
        })

        if not healthy:
            alerter.send(f"api-{svc['name']}",
                f"服务 {svc['name']} 异常: {status}")

    return results

# --------------------------------------------------
# 5. GPU 监控模块 (subprocess)
# --------------------------------------------------

def check_gpu_status(threshold=85):
    """检查 GPU 状态"""
    try:
        result = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=index,utilization.gpu,temperature.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )

        if result.returncode != 0:
            logger.error("nvidia-smi 执行失败")
            return []

        gpus = []
        for line in result.stdout.strip().split("\n"):
            parts = [p.strip() for p in line.split(", ")]
            if len(parts) < 5:
                continue

            gpu = {
                "index": int(parts[0]),
                "utilization": float(parts[1]),
                "temperature": float(parts[2]),
                "memory_used": float(parts[3]),
                "memory_total": float(parts[4]),
            }
            gpus.append(gpu)

            # 温度告警
            if gpu["temperature"] >= threshold:
                alerter.send(
                    f"gpu-temp-{gpu['index']}",
                    f"GPU #{gpu['index']} 温度 {gpu['temperature']}°C 超过阈值 {threshold}°C"
                )

        return gpus

    except FileNotFoundError:
        logger.warning("nvidia-smi 未安装")
        return []
    except Exception as e:
        logger.error(f"GPU 检查异常: {e}")
        return []

# --------------------------------------------------
# 6. 容器监控模块 (docker-py)
# --------------------------------------------------

def check_containers():
    """检查 Docker 容器状态"""
    if not HAS_DOCKER:
        return []

    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
    except Exception as e:
        logger.error(f"Docker 连接失败: {e}")
        return []

    results = []
    for c in containers:
        c.reload()
        info = {
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "<none>",
        }

        # 检查健康状态
        health = c.attrs.get("State", {}).get("Health")
        if health:
            info["health"] = health["Status"]
            if health["Status"] == "unhealthy":
                # 自动重启
                logger.warning(f"容器 {c.name} 不健康，尝试重启")
                try:
                    c.restart(timeout=10)
                    info["action"] = "已重启"
                except Exception as e:
                    info["action"] = f"重启失败: {e}"

                alerter.send(f"container-{c['name']}",
                    f"容器 {c.name} 不健康，已自动重启")

        results.append(info)

    return results

# --------------------------------------------------
# 7. 主巡检函数
# --------------------------------------------------

def run_full_check():
    """执行完整巡检"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"=== 开始巡检 {now} ===")

    # 1. API 健康检查
    api_results = check_api_health(CONFIG["services"])
    for r in api_results:
        logger.info(f"  API {r['name']}: {r['status']}")

    # 2. GPU 状态检查
    gpus = check_gpu_status(CONFIG["alert"]["gpu_temp_threshold"])
    for gpu in gpus:
        logger.info(f"  GPU #{gpu['index']}: 利用率 {gpu['utilization']}%, "
                    f"温度 {gpu['temperature']}°C, "
                    f"显存 {gpu['memory_used']}/{gpu['memory_total']}GB")

    # 3. 容器状态检查
    containers = check_containers()
    for c in containers:
        action = c.get("action", "")
        logger.info(f"  容器 {c['name']}: {c['status']} {action}")

    logger.info(f"=== 巡检完成 ===\n")

# --------------------------------------------------
# 8. 启动监控
# --------------------------------------------------

def main():
    print("=" * 50)
    print("  轻量级模型服务监控系统")
    print(f"  启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print(f"监控服务: {len(CONFIG['services'])} 个")
    print(f"GPU 温度阈值: {CONFIG['alert']['gpu_temp_threshold']}°C")
    print(f"日志文件: {CONFIG['log_file']}")
    print(f"按 Ctrl+C 停止")
    print()

    # 第一次立即执行
    run_full_check()

    if HAS_SCHEDULE:
        # 用 schedule 定时执行
        interval = CONFIG["interval"]["health_check"]
        schedule.every(interval).seconds.do(run_full_check)
        logger.info(f"定时巡检已设置: 每 {interval} 秒")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("监控已停止")
    else:
        # 简单循环
        try:
            while True:
                time.sleep(CONFIG["interval"]["health_check"])
                run_full_check()
        except KeyboardInterrupt:
            logger.info("监控已停止")

if __name__ == "__main__":
    main()

# --------------------------------------------------
# 小练习：扩展监控系统
# --------------------------------------------------

# 练习1：给监控系统添加远程 SSH 巡检功能
# 参考 Day 14-15 的 paramiko 代码
# 提示：在 CONFIG 里添加 servers 列表，在 run_full_check 里加入 SSH 巡检

# 练习2：给监控系统添加 Web 界面
# 用 Flask 提供一个简单的状态页面
# 提示：app.route("/") 返回巡检结果的 JSON

# 练习3：给监控系统添加历史数据记录
# 把每次巡检结果写入 SQLite 或 JSON 文件
# 提示：每次 run_full_check 把 results 追加到文件里
