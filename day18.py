# ============================================================
# Day 18: schedule + 整合 — 定时任务框架
# 目标：能用 Python 写定时任务，整合之前学的所有模块
# 用法：python day18.py 逐段运行，改一改，看看结果变不变
# ============================================================

import schedule
import time
import logging
import subprocess
import requests
from datetime import datetime

# --------------------------------------------------
# 1. schedule 库基础
# --------------------------------------------------
# pip install schedule
# 最简单的定时任务库

# 定义一个任务函数
def job_hello():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Hello!")

# 注册定时任务
schedule.every(10).seconds.do(job_hello)       # 每10秒
# schedule.every(1).minutes.do(job_hello)       # 每1分钟
# schedule.every(1).hours.do(job_hello)         # 每1小时
# schedule.every().day.at("09:00").do(job_hello) # 每天早上9点
# schedule.every().monday.do(job_hello)          # 每周一

# 运行调度器（阻塞式）
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# 演示：运行5次后取消
print("schedule 基础演示:")
counter = 0
while counter < 5:
    schedule.run_pending()
    time.sleep(1)
    counter += 1
schedule.clear()  # 清除所有任务
print("演示结束\n")

# --------------------------------------------------
# 2. 定时检查服务健康
# --------------------------------------------------

def check_health():
    """检查本地 API 健康状态"""
    try:
        resp = requests.get("http://localhost:8000/health", timeout=3)
        status = "正常" if resp.status_code == 200 else f"异常({resp.status_code})"
    except requests.exceptions.ConnectionError:
        status = "无法连接"
    except requests.exceptions.Timeout:
        status = "超时"

    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] API 状态: {status}")
    return status

# 注册定时健康检查
# schedule.every(30).seconds.do(check_health)

# --------------------------------------------------
# 3. 整合之前所学
# --------------------------------------------------

def run_cmd(cmd):
    """执行系统命令"""
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip()
    except Exception:
        return False, ""

def check_gpu_subprocess():
    """用 subprocess 检查 GPU"""
    ok, out = run_cmd("nvidia-smi --query-gpu=index,utilization.gpu,temperature.gpu --format=csv,noheader")
    if ok:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] GPU 信息:")
        for line in out.split("\n"):
            print(f"  {line}")
    else:
        print("GPU 信息获取失败")

def check_api_service():
    """用 requests 检查 API"""
    try:
        resp = requests.get("http://localhost:8000/v1/models", timeout=5)
        data = resp.json()
        model_count = len(data.get("data", []))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] API 正常, {model_count} 个模型")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] API 异常: {e}")

# --------------------------------------------------
# 4. 日志记录
# --------------------------------------------------

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("monitor.log"),           # 写文件
        logging.StreamHandler(),                       # 也打印到屏幕
    ]
)
logger = logging.getLogger(__name__)

def logged_health_check():
    """带日志的健康检查"""
    try:
        resp = requests.get("http://localhost:8000/health", timeout=3)
        if resp.status_code == 200:
            logger.info("API 状态正常")
        else:
            logger.warning(f"API 返回异常状态码: {resp.status_code}")
    except Exception as e:
        logger.error(f"API 检查失败: {e}")

# 按天滚动日志（推荐生产用法）
# from logging.handlers import TimedRotatingFileHandler
# handler = TimedRotatingFileHandler("monitor.log", when="midnight", backupCount=7)
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

# --------------------------------------------------
# 5. 实际场景：综合定时巡检
# --------------------------------------------------

def setup_monitor_schedule():
    """配置综合巡检定时任务"""

    # 每分钟检查 API
    schedule.every(1).minutes.do(logged_health_check)

    # 每5分钟检查 GPU
    schedule.every(5).minutes.do(check_gpu_subprocess)

    # 每小时检查容器状态
    # schedule.every(1).hours.do(check_containers)

    print("定时巡检已配置:")
    for job in schedule.get_jobs():
        print(f"  {job}")

# setup_monitor_schedule()

# 运行主循环
def run_monitor(duration_seconds=60):
    """运行巡检指定时间"""
    print(f"开始巡检，持续 {duration_seconds} 秒...")
    start = time.time()

    while time.time() - start < duration_seconds:
        schedule.run_pending()
        time.sleep(1)

    print("巡检结束")

# run_monitor(60)

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：定时 API 健康检查
# 每30秒检查一次服务，连续检查5次后退出

# ====== 在这里写你的代码 ======




# 练习2：综合巡检任务
# 结合 subprocess + requests，定时采集系统和服务信息

# ====== 在这里写你的代码 ======




# 练习3：可配置的定时任务框架
# 从配置列表读取任务，动态注册 schedule 任务

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import schedule
# import time
# import requests
#
# check_count = 0
#
# def check_health():
#     global check_count
#     check_count += 1
#     try:
#         resp = requests.get("http://localhost:8000/health", timeout=3)
#         status = f"正常 ({resp.status_code})"
#     except Exception as e:
#         status = f"异常 ({e})"
#     print(f"[第{check_count}次] {status}")
#     if check_count >= 5:
#         return schedule.CancelJob
#
# schedule.every(30).seconds.do(check_health)
# while len(schedule.get_jobs()) > 0:
#     schedule.run_pending()
#     time.sleep(1)
# print("检查完成")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import schedule
# import time
# import subprocess
# import requests
# import logging
#
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
# logger = logging.getLogger()
#
# def system_check():
#     result = subprocess.run(["uptime"], capture_output=True, text=True)
#     logger.info(f"系统: {result.stdout.strip()}")
#
# def service_check():
#     try:
#         resp = requests.get("http://localhost:8000/health", timeout=3)
#         logger.info(f"API: {resp.status_code}")
#     except Exception as e:
#         logger.warning(f"API: {e}")
#
# schedule.every(30).seconds.do(service_check)
# schedule.every(1).minutes.do(system_check)
#
# for _ in range(60):
#     schedule.run_pending()
#     time.sleep(1)

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import schedule
# import time
#
# def check_health():
#     print("健康检查执行")
#
# def check_gpu():
#     print("GPU 检查执行")
#
# TASKS_CONFIG = [
#     {"name": "health_check", "interval": 30, "unit": "seconds", "func": check_health},
#     {"name": "gpu_monitor", "interval": 5, "unit": "minutes", "func": check_gpu},
# ]
#
# def load_tasks(config):
#     for task in config:
#         unit_map = {"seconds": "seconds", "minutes": "minutes", "hours": "hours"}
#         unit = unit_map.get(task["unit"], "seconds")
#         job = getattr(schedule.every(task["interval"]), unit)
#         job.do(task["func"])
#         print(f"注册任务: {task['name']} (每 {task['interval']} {unit})")
#
# load_tasks(TASKS_CONFIG)
# for _ in range(120):
#     schedule.run_pending()
#     time.sleep(1)
