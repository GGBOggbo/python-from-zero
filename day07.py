# ============================================================
# Day 07: 函数 (def)
# 目标：能把重复代码封装成函数，提高复用性
# 用法：python day07.py
# ============================================================

# --------------------------------------------------
# 1. 定义和调用函数
# --------------------------------------------------

def greet():
    """简单的无参数函数"""
    print("Hello, 运维工程师！")

greet()        # 调用函数
greet()        # 可以反复调用

# --------------------------------------------------
# 2. 带参数的函数
# --------------------------------------------------

def check_server(name, status):
    """带参数的函数"""
    if status == "running":
        print(f"{name}: 正常运行")
    else:
        print(f"{name}: 异常 ({status})")

check_server("gpu-01", "running")
check_server("gpu-02", "stopped")

# --------------------------------------------------
# 3. 返回值 —— 函数的结果
# --------------------------------------------------

def get_status_code(level):
    """根据日志级别返回状态码"""
    if level == "ERROR":
        return 2
    elif level == "WARN":
        return 1
    else:
        return 0

code = get_status_code("ERROR")
print(f"状态码: {code}")       # 2

# 返回多个值（实际返回的是元组）
def get_server_info(name):
    """返回服务器的多个信息"""
    return name, 8000, "running"

server, port, status = get_server_info("gpu-01")
print(f"{server}:{port} {status}")

# --------------------------------------------------
# 4. 默认参数
# --------------------------------------------------

def check_health(url, timeout=5, retries=3):
    """带默认值的参数，调用时可以省略"""
    print(f"检查 {url}, 超时={timeout}s, 重试={retries}次")

check_health("http://gpu-01:8000")                    # 用默认值
check_health("http://gpu-01:8000", timeout=10)        # 覆盖 timeout
check_health("http://gpu-01:8000", retries=5, timeout=10)  # 命名参数，顺序随意

# --------------------------------------------------
# 5. 关键字参数（kwargs）
# --------------------------------------------------

def create_service(name, port, gpu=1, max_tokens=2048, **kwargs):
    """**kwargs 接收任意额外的关键字参数"""
    config = {
        "name": name,
        "port": port,
        "gpu": gpu,
        "max_tokens": max_tokens,
    }
    config.update(kwargs)       # 把额外的参数都加进去
    return config

svc = create_service(
    "qwen-72b", 8000,
    gpu=4, max_tokens=4096,
    temperature=0.7,            # 额外参数，会被 kwargs 接收
    top_p=0.9
)
print(svc)

# --------------------------------------------------
# 6. 文档字符串（docstring）
# --------------------------------------------------

def calculate_gpu_memory(total_gb, used_gb, safety_margin=0.1):
    """
    计算可用的 GPU 显存

    参数:
        total_gb: 总显存 (GB)
        used_gb: 已用显存 (GB)
        safety_margin: 安全余量比例，默认 10%

    返回:
        可用显存 (GB)
    """
    available = (total_gb - used_gb) * (1 - safety_margin)
    return round(available, 2)

result = calculate_gpu_memory(80, 45)
print(f"可用显存: {result} GB")

# --------------------------------------------------
# 7. 变量作用域
# --------------------------------------------------

global_var = "我是全局变量"

def test_scope():
    local_var = "我是局部变量"
    print(global_var)           # 能访问全局变量
    print(local_var)            # 能访问局部变量

test_scope()
# print(local_var)             # 报错！函数外访问不到局部变量

# 修改全局变量需要 global 关键字
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(f"计数: {counter}")       # 2

# 但更好的做法是：通过参数传入，通过返回值传出（避免用 global）
def increment_better(n):
    return n + 1

counter = 0
counter = increment_better(counter)
counter = increment_better(counter)
print(f"计数: {counter}")       # 2

# --------------------------------------------------
# 8. lambda（匿名函数，简短的一行函数）
# --------------------------------------------------

# 普通函数
def get_port(service):
    return service["port"]

# 等价的 lambda
get_port_lambda = lambda svc: svc["port"]

services = [
    {"name": "qwen-72b", "port": 8000},
    {"name": "llama-70b", "port": 8001},
    {"name": "mistral-7b", "port": 8002},
]

# 常和 sorted / max / min / map 配合使用
sorted_by_port = sorted(services, key=lambda s: s["port"])
print([s["name"] for s in sorted_by_port])

# map: 对每个元素执行操作
names = list(map(lambda s: s["name"], services))
print(names)                   # ['qwen-72b', 'llama-70b', 'mistral-7b']

# filter: 过滤
running = list(filter(lambda s: s["port"] >= 8001, services))
print([s["name"] for s in running])

# --------------------------------------------------
# 9. 实战：运维常用工具函数
# --------------------------------------------------

def parse_log_line(line):
    """解析一行日志，返回结构化数据"""
    try:
        parts = line.strip().split()
        return {
            "timestamp": f"{parts[0]} {parts[1]}",
            "level": parts[2],
            "message": " ".join(parts[3:])
        }
    except (IndexError, AttributeError):
        return None

def is_alert_level(level, threshold="WARN"):
    """判断日志级别是否达到告警阈值"""
    levels = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}
    return levels.get(level, 0) >= levels.get(threshold, 2)

def format_bytes(size_gb):
    """格式化存储大小"""
    if size_gb >= 1024:
        return f"{size_gb / 1024:.1f} TB"
    else:
        return f"{size_gb:.1f} GB"

def check_resource(name, usage, threshold=90):
    """检查资源使用率并返回状态"""
    if usage > threshold:
        return f"告警: {name} 使用率 {usage}% 超过阈值 {threshold}%"
    elif usage > threshold * 0.8:
        return f"注意: {name} 使用率 {usage}% 接近阈值"
    else:
        return f"正常: {name} 使用率 {usage}%"

# 使用这些函数
print("=== 资源检查 ===")
print(check_resource("CPU", 45))
print(check_resource("内存", 88))
print(check_resource("GPU显存", 95))
print(check_resource("磁盘", 72, threshold=70))

print(f"\n模型大小: {format_bytes(14.3)}")
print(f"数据集大小: {format_bytes(2048)}")

# 解析日志
log = "2024-01-15 10:30:00 ERROR GPU OOM"
parsed = parse_log_line(log)
if parsed and is_alert_level(parsed["level"]):
    print(f"\n告警日志: [{parsed['level']}] {parsed['message']}")

# --------------------------------------------------
# 10. 练习
# --------------------------------------------------

# 练习1：写一个函数，计算 GPU 利用率
# 输入: 总显存(GB), 已用显存(GB)
# 返回: 利用率百分比（保留1位小数）
# 例: gpu_usage(80, 60) → 75.0%

# ====== 在这里写你的代码 ======



# 练习2：写一个函数，批量检查端口是否在合法范围
# 输入: 端口列表
# 返回: 合法的端口列表（1024-65535）
# 例: filter_ports([80, 8000, 99999, 443, 8080]) → [8000, 8080]

# ====== 在这里写你的代码 ======



# 练习3（挑战）：写一个日志统计函数
# 输入: 日志行列表
# 返回: 字典 {"INFO": x, "WARN": y, "ERROR": z, "total": n}

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# def gpu_usage(total, used):
#     return round(used / total * 100, 1)
# print(gpu_usage(80, 60))

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# def filter_ports(ports):
#     return [p for p in ports if 1024 <= p <= 65535]
# print(filter_ports([80, 8000, 99999, 443, 8080]))

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# def count_logs(logs):
#     counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
#     total = 0
#     for log in logs:
#         for level in counts:
#             if level in log:
#                 counts[level] += 1
#                 total += 1
#                 break
#     counts["total"] = total
#     return counts
# test_logs = ["INFO ok", "ERROR fail", "WARN slow", "INFO done", "ERROR crash"]
# print(count_logs(test_logs))
