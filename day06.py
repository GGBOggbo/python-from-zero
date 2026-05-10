# ============================================================
# Day 06: for/while 循环
# 目标：能批量处理服务器、日志、配置等重复性任务
# 用法：python day06.py
# ============================================================

# --------------------------------------------------
# 1. for 循环基础 —— 遍历列表
# --------------------------------------------------

servers = ["gpu-01", "gpu-02", "gpu-03"]

for server in servers:
    print(f"检查 {server} ... 正常")

# 遍历字典
config = {"model": "qwen-72b", "port": 8000, "gpu": 4}
for key, value in config.items():
    print(f"{key} = {value}")

# 遍历字符串
for char in "GPU":
    print(char)

# --------------------------------------------------
# 2. range —— 生成数字序列
# --------------------------------------------------

# range(止) → 0 到 止-1
for i in range(5):
    print(i, end=" ")           # 0 1 2 3 4
print()

# range(起, 止) → 起到 止-1
for i in range(1, 4):
    print(i, end=" ")           # 1 2 3
print()

# range(起, 止, 步长)
for i in range(0, 10, 2):
    print(i, end=" ")           # 0 2 4 6 8
print()

# 实际用途：批量生成服务器名
for i in range(1, 6):
    print(f"gpu-{i:02d}")       # gpu-01 到 gpu-05（:02d 补零）

# range 也能反着数
for i in range(5, 0, -1):
    print(i, end=" ")           # 5 4 3 2 1
print()

# --------------------------------------------------
# 3. enumerate —— 同时拿索引和值
# --------------------------------------------------

servers = ["gpu-01", "gpu-02", "gpu-03"]
for index, name in enumerate(servers):
    print(f"第 {index} 台: {name}")

# 指定起始编号
for index, name in enumerate(servers, start=1):
    print(f"服务器 {index}: {name}")

# --------------------------------------------------
# 4. zip —— 同时遍历多个列表
# --------------------------------------------------

servers = ["gpu-01", "gpu-02", "gpu-03"]
temps = [72, 85, 78]
statuses = ["running", "warning", "running"]

for server, temp, status in zip(servers, temps, statuses):
    print(f"{server}: {temp}°C ({status})")

# 长度不同时，以最短的为准
a = [1, 2, 3, 4, 5]
b = ["a", "b", "c"]
for x, y in zip(a, b):
    print(x, y)                 # 只输出3组

# --------------------------------------------------
# 5. while 循环 —— 条件为 True 就一直跑
# --------------------------------------------------

# 基础：倒计时
count = 5
while count > 0:
    print(f"等待 {count} 秒...")
    count -= 1
print("完成！")

# 实际用途：轮询服务状态（模拟）
import random
retry = 0
max_retry = 3
while retry < max_retry:
    retry += 1
    # 模拟随机成功
    success = random.random() > 0.5
    if success:
        print(f"第 {retry} 次尝试: 成功")
        break                   # 成功了就跳出循环
    else:
        print(f"第 {retry} 次尝试: 失败，重试...")
else:
    # while 的 else: 循环正常结束（没被 break）才执行
    print(f"重试 {max_retry} 次后仍然失败")

# --------------------------------------------------
# 6. break 和 continue
# --------------------------------------------------

# break: 立即跳出整个循环
servers = ["gpu-01", "gpu-02", "ERROR", "gpu-03"]
for server in servers:
    if server == "ERROR":
        print("发现错误，停止检查")
        break
    print(f"检查 {server}: 正常")

# continue: 跳过本次，继续下一次
print()
for server in servers:
    if server == "ERROR":
        print(f"跳过异常项: {server}")
        continue
    print(f"检查 {server}: 正常")

# --------------------------------------------------
# 7. 循环中的列表操作
# --------------------------------------------------

# 筛选：从列表中找出符合条件的
logs = [
    "INFO  Service started",
    "ERROR GPU OOM",
    "WARN  Request timeout",
    "INFO  Model loaded",
    "ERROR GPU overheat",
]

# 只提取 ERROR 日志
errors = []
for log in logs:
    if "ERROR" in log:
        errors.append(log)
print("ERROR日志:", errors)

# 用列表推导式（更简洁）
errors2 = [log for log in logs if "ERROR" in log]
print("ERROR日志:", errors2)

# 计数
log_levels = {"INFO": 0, "WARN": 0, "ERROR": 0, "DEBUG": 0}
for log in logs:
    for level in log_levels:
        if log.startswith(level):
            log_levels[level] += 1
            break
print("日志统计:", log_levels)

# --------------------------------------------------
# 8. 嵌套循环
# --------------------------------------------------

# 检查每台服务器的每个 GPU
cluster = {
    "gpu-01": [72, 74, 71, 73],
    "gpu-02": [85, 88, 82, 90],
}

for server, temps in cluster.items():
    print(f"\n{server}:")
    for i, temp in enumerate(temps):
        status = "告警" if temp > 80 else "正常"
        print(f"  GPU{i}: {temp}°C {status}")

# --------------------------------------------------
# 9. 实战：批量服务检查
# --------------------------------------------------

services = [
    {"name": "qwen-72b", "port": 8000, "status": "running", "requests": 1500},
    {"name": "llama-70b", "port": 8001, "status": "running", "requests": 890},
    {"name": "mistral-7b", "port": 8002, "status": "stopped", "requests": 0},
    {"name": "glm-4", "port": 8003, "status": "running", "requests": 2300},
    {"name": "qwen-7b", "port": 8004, "status": "error", "requests": 0},
]

print("=== 批量服务检查 ===")
print(f"{'服务名':<15} {'端口':<8} {'状态':<10} {'请求数':>8}")
print("-" * 45)

total_requests = 0
running_count = 0
error_servers = []

for svc in services:
    total_requests += svc["requests"]
    if svc["status"] == "running":
        running_count += 1
    elif svc["status"] == "error":
        error_servers.append(svc["name"])

    print(f"{svc['name']:<15} {svc['port']:<8} {svc['status']:<10} {svc['requests']:>8,}")

print("-" * 45)
print(f"总计: {len(services)} 个服务, {running_count} 个运行中, 总请求 {total_requests:,}")
if error_servers:
    print(f"异常服务: {', '.join(error_servers)}")

# 找出请求数最多的服务
busiest = max(services, key=lambda s: s["requests"])
print(f"最繁忙: {busiest['name']} ({busiest['requests']:,} 请求)")

# --------------------------------------------------
# 10. 练习
# --------------------------------------------------

# 练习1：批量生成服务器配置
# 生成 5 台服务器的基础配置
# 期望输出:
# gpu-01: port=8001, ip=10.0.1.1
# gpu-02: port=8002, ip=10.0.1.2
# ... 以此类推

# ====== 在这里写你的代码 ======



# 练习2：找出温度异常的 GPU
temps = {"gpu-01": [72, 74, 71, 73], "gpu-02": [82, 88, 75, 91], "gpu-03": [70, 68, 72, 69]}
# 期望输出所有超过 80°C 的记录:
# gpu-02 GPU0: 82°C
# gpu-02 GPU1: 88°C
# gpu-02 GPU3: 91°C

# ====== 在这里写你的代码 ======



# 练习3（挑战）：模拟服务重启（最多重试3次）
# 模拟一个不靠谱的服务，每次启动有 70% 概率失败
# 用 while 循环，最多重试 3 次
# 成功就 print "启动成功" 并停止
# 3 次都失败就 print "启动失败，需要人工介入"

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# for i in range(1, 6):
#     port = 8000 + i
#     ip = f"10.0.1.{i}"
#     print(f"gpu-{i:02d}: port={port}, ip={ip}")

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# for server, gpu_temps in temps.items():
#     for i, temp in enumerate(gpu_temps):
#         if temp > 80:
#             print(f"{server} GPU{i}: {temp}°C")

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# import random
# retry = 0
# max_retry = 3
# while retry < max_retry:
#     retry += 1
#     success = random.random() > 0.7
#     if success:
#         print(f"第 {retry} 次尝试: 启动成功")
#         break
#     else:
#         print(f"第 {retry} 次尝试: 启动失败")
# else:
#     print("启动失败，需要人工介入")
