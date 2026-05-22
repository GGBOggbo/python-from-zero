# ============================================================
# Day 17: docker-py 进阶 — 日志/监控/自动重启
# 目标：能用 Python 监控容器状态、分析日志、自动处理异常
# 用法：python day17.py 逐段运行，改一改，看看结果变不变
# ============================================================

import docker
import time
from datetime import datetime

# --------------------------------------------------
# 1. 容器日志
# --------------------------------------------------

client = docker.from_env()

# 获取容器日志
# container = client.containers.get("vllm-qwen")

# 最近 50 行日志
# logs = container.logs(tail=50)
# print(logs.decode("utf-8"))

# 最近 1 小时的日志
# from datetime import datetime, timedelta
# since = datetime.now() - timedelta(hours=1)
# logs = container.logs(since=since, tail=100)

# 实时跟踪日志（类似 docker logs -f）
# for line in container.logs(stream=True, follow=True):
#     print(line.decode("utf-8").strip())

# --------------------------------------------------
# 2. 资源监控
# --------------------------------------------------

def get_container_stats(container_name):
    """获取容器资源使用情况"""
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)  # 获取一次快照

        # CPU 使用率计算
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                       stats["precpu_stats"]["system_cpu_usage"]
        cpu_count = stats["cpu_stats"]["online_cpus"]

        if system_delta > 0 and cpu_delta > 0:
            cpu_pct = (cpu_delta / system_delta) * cpu_count * 100
        else:
            cpu_pct = 0

        # 内存使用
        mem_used = stats["memory_stats"]["usage"] / (1024**3)  # GB
        mem_limit = stats["memory_stats"]["limit"] / (1024**3)
        mem_pct = (mem_used / mem_limit) * 100

        # 网络 IO
        net_rx = sum(v["rx_bytes"] for v in stats["networks"].values()) / (1024**2)
        net_tx = sum(v["tx_bytes"] for v in stats["networks"].values()) / (1024**2)

        return {
            "cpu_pct": round(cpu_pct, 1),
            "mem_used_gb": round(mem_used, 2),
            "mem_limit_gb": round(mem_limit, 2),
            "mem_pct": round(mem_pct, 1),
            "net_rx_mb": round(net_rx, 2),
            "net_tx_mb": round(net_tx, 2),
        }
    except docker.errors.NotFound:
        return {"error": f"容器不存在: {container_name}"}
    except Exception as e:
        return {"error": str(e)}

# stats = get_container_stats("vllm-qwen")
# if "error" not in stats:
#     print(f"CPU: {stats['cpu_pct']}%, 内存: {stats['mem_used_gb']}/{stats['mem_limit_gb']}GB ({stats['mem_pct']}%)")
#     print(f"网络: 接收 {stats['net_rx_mb']}MB, 发送 {stats['net_tx_mb']}MB")

# --------------------------------------------------
# 3. 健康检查
# --------------------------------------------------

def check_container_health(container_name):
    """检查容器健康状态"""
    try:
        container = client.containers.get(container_name)
        container.reload()  # 刷新最新状态

        # 检查是否有健康检查配置
        health = container.attrs.get("State", {}).get("Health")

        if health is None:
            return {"status": "no_healthcheck", "healthy": None}

        status = health["Status"]  # starting, healthy, unhealthy
        failing_streak = health.get("FailingStreak", 0)
        last_log = health.get("Log", [{}])[-1].get("Output", "")[:200]

        return {
            "status": status,
            "healthy": status == "healthy",
            "failing_streak": failing_streak,
            "last_log": last_log,
        }
    except docker.errors.NotFound:
        return {"status": "not_found", "healthy": False}

# result = check_container_health("vllm-qwen")
# print(f"健康状态: {result['status']}")

# --------------------------------------------------
# 4. 自动重启策略
# --------------------------------------------------

def get_restart_policy(container_name):
    """查看容器重启策略"""
    try:
        container = client.containers.get(container_name)
        policy = container.attrs["HostConfig"]["RestartPolicy"]["Name"]
        return policy
    except Exception:
        return None

# 常见重启策略：
# "no"            → 不自动重启（默认）
# "always"        → 总是重启
# "unless-stopped" → 除非手动停止，否则总是重启
# "on-failure"    → 仅在非零退出码时重启

def auto_restart_unhealthy(max_retries=2):
    """检测并重启不健康的容器"""
    containers = client.containers.list(filters={"status": "running"})
    restarted = []

    for c in containers:
        health = check_container_health(c.name)

        if health.get("status") == "unhealthy":
            print(f"[告警] {c.name} 不健康 (连续失败 {health['failing_streak']} 次)")

            if health["failing_streak"] <= max_retries:
                print(f"  重启 {c.name}...")
                c.restart(timeout=10)
                restarted.append(c.name)
                print(f"  已重启")
            else:
                print(f"  超过最大重试次数，跳过（需要人工介入）")

    return restarted

# auto_restart_unhealthy()

# --------------------------------------------------
# 5. 实际场景：模型服务监控脚本
# --------------------------------------------------

def monitor_inference_services():
    """监控所有推理服务容器"""
    all_c = client.containers.list(all=True)
    services = [c for c in all_c if "vllm" in c.name or "sglang" in c.name]

    if not services:
        print("没有找到推理服务容器")
        return

    print(f"\n{'='*60}")
    print(f"  推理服务监控 - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    print(f"{'名称':<20} {'状态':<12} {'CPU':<8} {'内存':<15} {'健康'}")
    print(f"{'-'*60}")

    for c in services:
        c.reload()
        status = c.status
        health = check_container_health(c.name)
        health_status = health.get("status", "N/A")

        if status == "running":
            stats = get_container_stats(c.name)
            if "error" not in stats:
                cpu = f"{stats['cpu_pct']}%"
                mem = f"{stats['mem_used_gb']}/{stats['mem_limit_gb']}GB"
            else:
                cpu = "N/A"
                mem = "N/A"
        else:
            cpu = "-"
            mem = "-"

        print(f"{c.name:<20} {status:<12} {cpu:<8} {mem:<15} {health_status}")

    print(f"{'='*60}")

# monitor_inference_services()

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：日志分析函数
# 获取容器最近 N 行日志，统计 ERROR 出现次数

# ====== 在这里写你的代码 ======




# 练习2：容器资源监控
# 获取容器 CPU/内存使用率，格式化输出

# ====== 在这里写你的代码 ======




# 练习3：自动重启异常容器
# 检测状态异常的容器，自动重启，记录操作日志

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import docker
#
# def analyze_logs(container_name, tail=100):
#     client = docker.from_env()
#     try:
#         container = client.containers.get(container_name)
#         logs = container.logs(tail=tail).decode("utf-8")
#         lines = logs.strip().split("\n")
#         errors = [l for l in lines if "ERROR" in l.upper()]
#         warnings = [l for l in lines if "WARNING" in l.upper()]
#         print(f"日志统计 ({tail} 行):")
#         print(f"  总行数: {len(lines)}")
#         print(f"  ERROR: {len(errors)} 次")
#         print(f"  WARNING: {len(warnings)} 次")
#         if errors:
#             print(f"\n最近 ERROR:")
#             for e in errors[-3:]:
#                 print(f"  {e[:150]}")
#     except docker.errors.NotFound:
#         print(f"容器不存在: {container_name}")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import docker
#
# def get_container_stats(container_name):
#     client = docker.from_env()
#     try:
#         container = client.containers.get(container_name)
#         stats = container.stats(stream=False)
#         cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
#                     stats["precpu_stats"]["cpu_usage"]["total_usage"]
#         system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
#                        stats["precpu_stats"]["system_cpu_usage"]
#         cpu_count = stats["cpu_stats"]["online_cpus"]
#         cpu_pct = (cpu_delta / system_delta) * cpu_count * 100 if system_delta > 0 else 0
#         mem_used = stats["memory_stats"]["usage"] / (1024**3)
#         mem_limit = stats["memory_stats"]["limit"] / (1024**3)
#         print(f"{container_name}: CPU {cpu_pct:.1f}%, 内存 {mem_used:.1f}/{mem_limit:.1f}GB")
#     except Exception as e:
#         print(f"获取失败: {e}")

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import docker
# import time
# from datetime import datetime
#
# def auto_restart_unhealthy():
#     client = docker.from_env()
#     containers = client.containers.list(filters={"status": "running"})
#     log_lines = []
#     for c in containers:
#         c.reload()
#         health = c.attrs.get("State", {}).get("Health")
#         if health and health["Status"] == "unhealthy":
#             msg = f"[{datetime.now().strftime('%H:%M:%S')}] {c.name} 不健康，正在重启"
#             log_lines.append(msg)
#             print(msg)
#             c.restart(timeout=10)
#             msg2 = f"[{datetime.now().strftime('%H:%M:%S')}] {c.name} 重启完成"
#             log_lines.append(msg2)
#             print(msg2)
#     # 写入日志文件
#     if log_lines:
#         with open("restart.log", "a") as f:
#             for line in log_lines:
#                 f.write(line + "\n")
#     return log_lines
