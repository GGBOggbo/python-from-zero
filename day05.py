# ============================================================
# Day 05: if/else 条件判断
# 目标：能让程序根据不同条件做不同的事
# 用法：python day05.py
# ============================================================

# --------------------------------------------------
# 1. 基础 if/else
# --------------------------------------------------

gpu_temp = 85

if gpu_temp >= 80:
    print("告警：GPU 温度过高！")
else:
    print("温度正常")

# 改变温度值试试
gpu_temp = 72
if gpu_temp >= 80:
    print("告警：GPU 温度过高！")
else:
    print("温度正常")

# --------------------------------------------------
# 2. if/elif/else —— 多个条件
# --------------------------------------------------

status_code = 503

if status_code == 200:
    print("服务正常")
elif status_code == 404:
    print("接口不存在")
elif status_code == 500:
    print("服务器内部错误")
elif status_code == 503:
    print("服务不可用")
else:
    print(f"未知状态: {status_code}")

# --------------------------------------------------
# 3. 比较运算符
# --------------------------------------------------

cpu_usage = 87.5
threshold = 90

# 大于 / 小于
print(cpu_usage > threshold)     # False
print(cpu_usage < threshold)     # True
print(cpu_usage >= 87.5)         # True（大于等于）
print(cpu_usage <= 90)           # True（小于等于）

# 等于 / 不等于（注意：比较相等用 ==，不是 =）
port = 8000
print(port == 8000)              # True
print(port != 8080)              # True（不等于）

# --------------------------------------------------
# 4. 逻辑运算符：and / or / not
# --------------------------------------------------

cpu = 85
memory = 90
disk = 60

# and: 两个条件都满足
if cpu > 80 and memory > 80:
    print("CPU 和内存都高！")

# or: 满足其中一个
if cpu > 90 or memory > 90 or disk > 90:
    print("至少一项资源告警！")

# not: 取反
is_healthy = False
if not is_healthy:
    print("服务不健康")

# 实际例子：判断是否需要告警
if cpu > 80 or memory > 85 or disk > 90:
    print("资源告警！请检查")
else:
    print("资源正常")

# --------------------------------------------------
# 5. in 判断
# --------------------------------------------------

status = "running"
valid_statuses = ["running", "stopped", "error"]

if status in valid_statuses:
    print(f"状态有效: {status}")
else:
    print(f"无效状态: {status}")

# 字符串也可以用 in
log = "ERROR: GPU OOM"
if "ERROR" in log:
    print("发现错误日志")
elif "WARN" in log:
    print("发现警告日志")

# not in
if "DEBUG" not in log:
    print("非调试日志")

# --------------------------------------------------
# 6. 嵌套 if
# --------------------------------------------------

service = {
    "name": "qwen-72b",
    "status": "running",
    "gpu_temp": 82,
    "memory_usage": 75
}

# 嵌套判断（尽量避免太深，2层就够）
if service["status"] == "running":
    if service["gpu_temp"] > 80:
        print(f"{service['name']} 运行中但温度过高！")
    else:
        print(f"{service['name']} 一切正常")
else:
    print(f"{service['name']} 未运行")

# 更清晰的写法：用 and 合并
if service["status"] == "running" and service["gpu_temp"] > 80:
    print(f"{service['name']} 温度过高告警")

# --------------------------------------------------
# 7. 三元表达式（一行 if/else）
# --------------------------------------------------
# 之前 Day01 学过的：值A if 条件 else 值B

gpu_temp = 78
alert = "告警" if gpu_temp >= 80 else "正常"
print(f"GPU 温度: {gpu_temp}°C → {alert}")

# 用在 f-string 里
port = 8000
print(f"端口: {port} ({'开放' if port == 8000 else '异常'})")

# --------------------------------------------------
# 8. 真值和假值
# --------------------------------------------------
# 以下值在 if 中被视为 False（假值）:
#   None, False, 0, 0.0, "", [], {}, set()

# 常见用法：检查变量是否有值
log = ""
if log:
    print(f"日志内容: {log}")
else:
    print("日志为空")

servers = []
if servers:
    print(f"有 {len(servers)} 台服务器")
else:
    print("没有服务器")

error_count = 0
if error_count:
    print(f"有 {error_count} 个错误")
else:
    print("没有错误")

# --------------------------------------------------
# 9. 实战：服务健康检查逻辑
# --------------------------------------------------

def check_service(name, status, cpu, memory, gpu_temp, error_count):
    """检查服务状态，返回健康等级"""
    # 先判断基本状态
    if status != "running":
        return "CRITICAL", f"{name} 未运行"

    # 检查各项指标
    issues = []
    if cpu > 90:
        issues.append(f"CPU {cpu}%")
    if memory > 90:
        issues.append(f"内存 {memory}%")
    if gpu_temp > 85:
        issues.append(f"GPU温度 {gpu_temp}°C")
    if error_count > 100:
        issues.append(f"错误数 {error_count}")

    if len(issues) == 0:
        return "HEALTHY", f"{name} 一切正常"
    elif len(issues) == 1:
        return "WARNING", f"{name} 注意: {'; '.join(issues)}"
    else:
        return "CRITICAL", f"{name} 多项异常: {'; '.join(issues)}"


# 测试不同的服务状态
test_cases = [
    ("qwen-72b", "running", 45, 60, 72, 5),
    ("llama-70b", "running", 92, 88, 70, 10),
    ("mistral-7b", "stopped", 0, 0, 0, 0),
    ("glm-4", "running", 95, 92, 88, 150),
]

print("=== 服务健康检查 ===")
for name, status, cpu, mem, temp, errors in test_cases:
    level, msg = check_service(name, status, cpu, mem, temp, errors)
    print(f"[{level}] {msg}")

# --------------------------------------------------
# 10. 练习
# --------------------------------------------------

# 练习1：端口检查
# 给定一个端口，判断属于哪个范围
# 0-1023: 系统保留端口
# 1024-49151: 注册端口
# 49152-65535: 动态端口
# 其他: 无效端口

port = 8000
# 期望输出: "端口 8000 是注册端口"

# ====== 在这里写你的代码 ======



# 练习2：日志级别判断
# 根据日志级别输出不同的处理方式
# ERROR: 立即通知
# WARN: 记录并关注
# INFO: 正常记录
# DEBUG: 开发环境才显示
# 其他: 未知级别

level = "WARN"
# 期望输出: "WARN → 记录并关注"

# ====== 在这里写你的代码 ======



# 练习3（挑战）：综合判断是否需要扩容
# 条件：同时满足以下任意两项就需要扩容
# - CPU使用率 > 80%
# - 内存使用率 > 85%
# - 请求队列 > 100
# - GPU使用率 > 90%

cpu_usage = 85
memory_usage = 88
request_queue = 50
gpu_usage = 92
# 期望输出: "需要扩容" 或 "暂不需要扩容"

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# port = 8000
# if 0 <= port <= 1023:
#     print(f"端口 {port} 是系统保留端口")
# elif 1024 <= port <= 49151:
#     print(f"端口 {port} 是注册端口")
# elif 49152 <= port <= 65535:
#     print(f"端口 {port} 是动态端口")
# else:
#     print(f"端口 {port} 无效")

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# level = "WARN"
# if level == "ERROR":
#     print("ERROR → 立即通知")
# elif level == "WARN":
#     print("WARN → 记录并关注")
# elif level == "INFO":
#     print("INFO → 正常记录")
# elif level == "DEBUG":
#     print("DEBUG → 开发环境才显示")
# else:
#     print(f"{level} → 未知级别")

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# cpu_usage = 85
# memory_usage = 88
# request_queue = 50
# gpu_usage = 92
# flags = [cpu_usage > 80, memory_usage > 85, request_queue > 100, gpu_usage > 90]
# if sum(flags) >= 2:
#     print("需要扩容")
# else:
#     print("暂不需要扩容")
