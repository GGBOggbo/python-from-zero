# ============================================================
# Day 04: 字典 Dict
# 目标：能用字典存储和操作配置信息、服务状态等键值对数据
# 用法：python day04.py
# ============================================================

# --------------------------------------------------
# 1. 创建字典
# --------------------------------------------------
# 字典用花括号 {}，key:value 形式，key 通常是字符串

config = {
    "model": "qwen-72b",
    "port": 8000,
    "gpu_count": 4,
    "max_tokens": 2048
}

print(config)
print(type(config))          # <class 'dict'>

# 空字典
empty1 = {}
empty2 = dict()

# 从两个列表创建字典
keys = ["name", "port", "status"]
values = ["gpu-01", 8000, "running"]
server = dict(zip(keys, values))
print(server)                # {'name': 'gpu-01', 'port': 8000, 'status': 'running'}

# --------------------------------------------------
# 2. 查 —— 取值（最常用的操作）
# --------------------------------------------------
config = {"model": "qwen-72b", "port": 8000, "gpu_count": 4}

# 方式1：用方括号（key不存在会报 KeyError！）
print(config["model"])       # qwen-72b
# print(config["host"])      # KeyError! 不存在的key直接报错

# 方式2：用 get（推荐！不存在返回 None，不报错）
print(config.get("model"))           # qwen-72b
print(config.get("host"))            # None
print(config.get("host", "localhost"))  # 不存在时返回默认值

# 查看所有 key / value / 键值对
print(config.keys())         # dict_keys(['model', 'port', 'gpu_count'])
print(config.values())       # dict_values(['qwen-72b', 8000, 4])
print(config.items())        # dict_items([('model', 'qwen-72b'), ...])

# 判断 key 是否存在
print("model" in config)     # True
print("host" in config)      # False

# 长度
print(len(config))           # 3

# --------------------------------------------------
# 3. 增 / 改（操作一样！key 不存在就是增，存在就是改）
# --------------------------------------------------
config = {"model": "qwen-72b", "port": 8000}

# 直接赋值
config["temperature"] = 0.7     # key 不存在 → 增
config["port"] = 8080           # key 已存在 → 改
print(config)

# update: 批量增/改
config.update({"port": 9000, "timeout": 30, "gpu_count": 4})
print(config)

# setdefault: 不存在才加，存在就不动
config.setdefault("port", 6006)      # port 已存在，不会改
config.setdefault("log_level", "INFO")  # log_level 不存在，会加上
print(config)

# --------------------------------------------------
# 4. 删
# --------------------------------------------------
config = {"model": "qwen-72b", "port": 8080, "gpu_count": 4, "timeout": 30}

# del: 按key删
del config["timeout"]
print(config)

# pop: 按key删，并返回被删的值
removed = config.pop("gpu_count")
print(f"删掉了: {removed}")       # 4
print(config)

# popitem: 删最后一个（Python 3.7+ 字典是有序的）
last = config.popitem()
print(f"最后插入的: {last}")       # ('port', 8080)

# clear: 清空
backup = config.copy()
config.clear()
print(f"清空后: {config}")
print(f"备份: {backup}")

# --------------------------------------------------
# 5. 遍历字典（超常用！）
# --------------------------------------------------
server = {
    "name": "gpu-01",
    "ip": "10.0.0.1",
    "port": 8000,
    "status": "running"
}

# 遍历 key
for key in server:
    print(key)

# 遍历 value
for value in server.values():
    print(value)

# 遍历 key-value 对（最常用）
for key, value in server.items():
    print(f"{key}: {value}")

# --------------------------------------------------
# 6. 嵌套字典 —— 存储复杂结构
# --------------------------------------------------

# 多个服务器的信息
cluster = {
    "gpu-01": {"ip": "10.0.0.1", "gpu": 4, "status": "running"},
    "gpu-02": {"ip": "10.0.0.2", "gpu": 4, "status": "warning"},
    "gpu-03": {"ip": "10.0.0.3", "gpu": 2, "status": "offline"}
}

# 取某个服务器的信息
print(cluster["gpu-01"])                    # 整个子字典
print(cluster["gpu-01"]["ip"])              # 10.0.0.1
print(cluster["gpu-02"]["status"])          # warning

# 遍历所有服务器
for name, info in cluster.items():
    print(f"{name} ({info['ip']}): {info['status']}, GPU: {info['gpu']}")

# 修改嵌套值
cluster["gpu-01"]["status"] = "maintenance"
print(cluster["gpu-01"]["status"])

# 添加新服务器
cluster["gpu-04"] = {"ip": "10.0.0.4", "gpu": 8, "status": "running"}
print(f"集群服务器数: {len(cluster)}")

# --------------------------------------------------
# 7. 字典推导式
# --------------------------------------------------

# 交换 key 和 value
status_map = {"running": 0, "stopped": 1, "error": 2}
reversed_map = {v: k for k, v in status_map.items()}
print(reversed_map)             # {0: 'running', 1: 'stopped', 2: 'error'}

# 从列表创建字典
servers = ["gpu-01", "gpu-02", "gpu-03"]
status_dict = {s: "running" for s in servers}
print(status_dict)

# 过滤：只保留 running 的
all_status = {"gpu-01": "running", "gpu-02": "offline", "gpu-03": "running"}
running_only = {k: v for k, v in all_status.items() if v == "running"}
print(running_only)

# --------------------------------------------------
# 8. 常用技巧
# --------------------------------------------------

# 合并两个字典（Python 3.9+）
a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}
merged = a | b                 # {"x": 1, "y": 3, "z": 4}（b 覆盖 a 的重复 key）
print(merged)

# 旧版本写法
merged2 = {**a, **b}
print(merged2)

# 安全取值的链式写法（避免 KeyError）
data = {"server": {"gpu": {"temp": 78}}}
# 逐层 get，任何一层不存在都不会报错
temp = data.get("server", {}).get("gpu", {}).get("temp")
print(f"温度: {temp}")

# --------------------------------------------------
# 9. 实战：模型服务配置管理
# --------------------------------------------------

services = {
    "qwen-72b": {
        "port": 8000,
        "gpu": [0, 1, 2, 3],
        "max_tokens": 2048,
        "status": "running",
        "requests": 15823
    },
    "llama-70b": {
        "port": 8001,
        "gpu": [4, 5, 6, 7],
        "max_tokens": 4096,
        "status": "running",
        "requests": 8921
    },
    "mistral-7b": {
        "port": 8002,
        "gpu": [8],
        "max_tokens": 8192,
        "status": "stopped",
        "requests": 0
    }
}

print("=== 模型服务总览 ===")
for name, info in services.items():
    gpu_list = ",".join(str(g) for g in info["gpu"])
    print(f"  {name}")
    print(f"    端口: {info['port']}, GPU: [{gpu_list}], 状态: {info['status']}, 请求数: {info['requests']:,}")

# 统计正在运行的服务
running = [name for name, info in services.items() if info["status"] == "running"]
print(f"\n运行中: {len(running)} 个 → {', '.join(running)}")

# 统计总 GPU 使用
total_gpus = sum(len(info["gpu"]) for info in services.values() if info["status"] == "running")
print(f"占用 GPU: {total_gpus} 张")

# 添加新服务
services["glm-4"] = {
    "port": 8003,
    "gpu": [9],
    "max_tokens": 4096,
    "status": "running",
    "requests": 0
}
print(f"\n添加 glm-4 后，共 {len(services)} 个服务")

# --------------------------------------------------
# 10. 练习
# --------------------------------------------------

# 练习1：服务器配置管理
# 完成以下操作，每步 print 验证
server = {"name": "gpu-01", "ip": "10.0.0.1", "port": 8000}
# 1. 添加 status="running"
# 2. 把 port 改成 8080
# 3. 删除 ip 字段
# 4. 添加 gpu_memory="80GB"
# 期望: {'name': 'gpu-01', 'port': 8080, 'status': 'running', 'gpu_memory': '80GB'}

# ====== 在这里写你的代码 ======



# 练习2：统计每个模型服务的 GPU 数量
models = {
    "qwen-72b": {"gpu": [0, 1, 2, 3], "status": "running"},
    "llama-70b": {"gpu": [4, 5], "status": "running"},
    "mistral-7b": {"gpu": [8], "status": "stopped"}
}
# 期望输出:
# qwen-72b: 4 张 GPU (running)
# llama-70b: 2 张 GPU (running)
# mistral-7b: 1 张 GPU (stopped)
# 总计: 7 张 GPU

# ====== 在这里写你的代码 ======



# 练习3（挑战）：把两个配置合并，重复的 key 以新配置为准
old_config = {"model": "qwen-7b", "port": 8000, "gpu": 1}
new_config = {"model": "qwen-72b", "port": 8080, "timeout": 30}
# 期望: {'model': 'qwen-72b', 'port': 8080, 'gpu': 1, 'timeout': 30}

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# server = {"name": "gpu-01", "ip": "10.0.0.1", "port": 8000}
# server["status"] = "running"
# server["port"] = 8080
# del server["ip"]
# server["gpu_memory"] = "80GB"
# print(server)

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# total = 0
# for name, info in models.items():
#     gpu_count = len(info["gpu"])
#     total += gpu_count
#     print(f"{name}: {gpu_count} 张 GPU ({info['status']})")
# print(f"总计: {total} 张 GPU")

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# merged = old_config | new_config
# print(merged)
