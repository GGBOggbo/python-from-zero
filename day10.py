# ============================================================
# Day 10: 模块和 import
# 目标：能用标准库和第三方库，能组织自己的代码
# 用法：python day10.py
# ============================================================

# --------------------------------------------------
# 1. 什么是模块？
# --------------------------------------------------
# 模块就是一个 .py 文件
# 你写的 day01.py 就是一个模块
# import 就是把别的模块里的功能拿过来用

# --------------------------------------------------
# 2. 导入方式
# --------------------------------------------------

# 方式1：导入整个模块
import os
print(os.getcwd())              # 当前工作目录

# 方式2：导入模块并起别名
import json as j
print(type(j))                  # <class 'module'>

# 方式3：从模块中导入特定的功能
from datetime import datetime, timedelta
print(datetime.now())           # 当前时间

# 方式4：导入所有（不推荐，容易命名冲突）
# from os.path import *

# --------------------------------------------------
# 3. os 模块 —— 操作系统交互
# --------------------------------------------------

import os

# 路径操作
print(f"当前目录: {os.getcwd()}")
print(f"文件存在: {os.path.exists('day01.py')}")
print(f"是文件: {os.path.isfile('day01.py')}")
print(f"是目录: {os.path.isdir('.')}")

# 路径拼接（跨平台安全）
config_path = os.path.join("config", "model", "qwen.json")
print(f"拼接路径: {config_path}")

# 文件名拆分
filepath = "/data/python/day10.py"
print(f"目录: {os.path.dirname(filepath)}")
print(f"文件名: {os.path.basename(filepath)}")
print(f"扩展名: {os.path.splitext(filepath)}")

# 环境变量
print(f"HOME: {os.environ.get('HOME', '未设置')}")
print(f"PATH: {os.environ.get('PATH', '')[:50]}...")

# 创建和删除
os.makedirs("test_dir/sub", exist_ok=True)
print(f"目录已创建: test_dir/sub")

# 执行系统命令
result = os.popen("echo hello").read()
print(f"命令输出: {result.strip()}")

# --------------------------------------------------
# 4. sys 模块 —— Python 系统相关
# --------------------------------------------------

import sys

print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")
print(f"平台: {sys.platform}")
print(f"搜索路径: {sys.path[:3]}")  # 模块搜索路径

# 命令行参数
print(f"脚本名: {sys.argv[0]}")

# --------------------------------------------------
# 5. subprocess —— 执行系统命令（比 os.popen 更好）
# --------------------------------------------------

import subprocess

# 执行命令并获取输出
result = subprocess.run(
    ["echo", "Hello from subprocess"],
    capture_output=True,
    text=True
)
print(f"输出: {result.stdout.strip()}")
print(f"返回码: {result.returncode}")

# 检查命令是否存在
def command_exists(cmd):
    try:
        subprocess.run(["which", cmd], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

print(f"python3 存在: {command_exists('python3')}")
print(f"nvidia-smi 存在: {command_exists('nvidia-smi')}")

# --------------------------------------------------
# 6. json 模块 —— JSON 处理
# --------------------------------------------------

import json

# Python 对象 → JSON 字符串
config = {"model": "qwen-72b", "port": 8000, "gpu": [0, 1, 2, 3]}
json_str = json.dumps(config, indent=2)
print(f"JSON 字符串:\n{json_str}")

# JSON 字符串 → Python 对象
parsed = json.loads(json_str)
print(f"解析后: {parsed['model']}")

# 直接读写 JSON 文件
with open("test_config.json", "w") as f:
    json.dump(config, f, indent=2)

with open("test_config.json", "r") as f:
    loaded = json.load(f)
print(f"从文件读取: {loaded}")

# --------------------------------------------------
# 7. datetime 模块 —— 时间处理
# --------------------------------------------------

from datetime import datetime, timedelta

# 当前时间
now = datetime.now()
print(f"现在: {now}")
print(f"格式化: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 时间计算
one_hour_later = now + timedelta(hours=1)
print(f"一小时后: {one_hour_later}")

yesterday = now - timedelta(days=1)
print(f"昨天: {yesterday.strftime('%Y-%m-%d')}")

# 解析时间字符串
log_time = datetime.strptime("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
print(f"解析时间: {log_time}")

# 计算时间差
start = datetime.strptime("2024-01-15 10:00:00", "%Y-%m-%d %H:%M:%S")
end = datetime.strptime("2024-01-15 10:05:30", "%Y-%m-%d %H:%M:%S")
diff = end - start
print(f"耗时: {diff.total_seconds()} 秒")

# --------------------------------------------------
# 8. collections 模块 —— 特殊容器
# --------------------------------------------------

from collections import Counter, defaultdict

# Counter: 计数器（统计日志级别超方便）
logs = ["INFO", "ERROR", "WARN", "INFO", "ERROR", "INFO", "DEBUG", "ERROR"]
counts = Counter(logs)
print(f"日志统计: {counts}")
print(f"最常见的2个: {counts.most_common(2)}")

# defaultdict: 带默认值的字典（避免 KeyError）
server_logs = defaultdict(list)
for i, level in enumerate(logs):
    server_logs[level].append(i)
print(f"ERROR 出现在: {server_logs['ERROR']}")

# --------------------------------------------------
# 9. pathlib 模块 —— 更优雅的路径操作
# --------------------------------------------------

from pathlib import Path

# 创建 Path 对象
p = Path("/data/python")
print(f"路径: {p}")
print(f"是否存在: {p.exists()}")
print(f"是目录: {p.is_dir()}")

# 列出所有 .py 文件
py_files = list(p.glob("*.py"))
print(f"\nPython 文件 ({len(py_files)} 个):")
for f in sorted(py_files):
    size = f.stat().st_size
    print(f"  {f.name} ({size:,} 字节)")

# 拼接路径（比 os.path.join 更直观）
config_file = p / "config" / "model.json"
print(f"\n配置路径: {config_file}")

# --------------------------------------------------
# 10. 第三方库简介
# --------------------------------------------------

# 安装第三方库：pip install 包名
# 常用第三方库：

third_party = {
    "requests": "HTTP 请求（调 API、健康检查）",
    "paramiko": "SSH 远程连接服务器",
    "psutil": "获取系统信息（CPU、内存、磁盘）",
    "pandas": "数据分析（处理日志、CSV）",
    "fastapi": "写 API 接口",
    "docker": "操作 Docker 容器",
}

print("=== 常用第三方库 ===")
for name, desc in third_party.items():
    print(f"  pip install {name:<12} # {desc}")

# 以 requests 为例（如果没有安装，pip install requests）
try:
    import requests
    print("\nrequests 已安装")

    # 示例：调用模型 API
    # response = requests.post(
    #     "http://localhost:8000/v1/chat/completions",
    #     json={"model": "qwen-72b", "messages": [{"role": "user", "content": "你好"}]},
    #     timeout=5
    # )
    # print(response.json())
except ImportError:
    print("\nrequests 未安装，运行: pip install requests")

# --------------------------------------------------
# 11. 实战：综合工具脚本
# --------------------------------------------------

def system_info():
    """收集系统信息"""
    info = {
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Python版本": sys.version.split()[0],
        "平台": sys.platform,
        "当前目录": os.getcwd(),
    }

    # 统计项目文件
    project_dir = Path(".")
    py_count = len(list(project_dir.glob("day*.py")))
    info["练习文件数"] = py_count

    return info

def print_report(info):
    """格式化打印报告"""
    print("\n=== 系统信息 ===")
    for key, value in info.items():
        print(f"  {key}: {value}")

info = system_info()
print_report(info)

# --------------------------------------------------
# 12. 练习
# --------------------------------------------------

# 练习1：写一个函数，获取目录下所有 .log 文件
# 输入: 目录路径
# 返回: 文件路径列表
# 提示: 用 pathlib.Path.glob()

# ====== 在这里写你的代码 ======



# 练习2：写一个函数，统计文件中每个单词出现的次数
# 输入: 文件路径
# 返回: Counter 对象
# 提示: 用 Counter + split()

# ====== 在这里写你的代码 ======



# 练习3（挑战）：写一个简单的配置管理器
# 功能: 读取 JSON 配置、更新配置、保存配置
# 要求: 异常处理、文件不存在时使用默认配置

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# def find_log_files(directory):
#     return sorted(Path(directory).glob("*.log"))
# for f in find_log_files("."):
#     print(f.name)

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# def word_count(filepath):
#     try:
#         with open(filepath, "r") as f:
#             words = f.read().split()
#             return Counter(words)
#     except FileNotFoundError:
#         print(f"文件不存在: {filepath}")
#         return Counter()

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# class ConfigManager:
#     def __init__(self, filepath, default=None):
#         self.filepath = filepath
#         self.config = default or {}
#         self.load()
#     def load(self):
#         try:
#             with open(self.filepath, "r") as f:
#                 self.config = json.load(f)
#         except (FileNotFoundError, json.JSONDecodeError):
#             pass
#     def get(self, key, default=None):
#         return self.config.get(key, default)
#     def set(self, key, value):
#         self.config[key] = value
#     def save(self):
#         with open(self.filepath, "w") as f:
#             json.dump(self.config, f, indent=2)
#     def __str__(self):
#         return json.dumps(self.config, indent=2, ensure_ascii=False)
