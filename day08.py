# ============================================================
# Day 08: 文件读写
# 目标：能读取日志文件、写入配置、处理 CSV/TXT
# 用法：python day08.py（会自动创建测试文件）
# ============================================================

import os

# --------------------------------------------------
# 1. 写入文件
# --------------------------------------------------

# 写文本文件（覆盖已有内容）
with open("test_log.txt", "w") as f:
    f.write("2024-01-15 10:23:01 INFO  Service started\n")
    f.write("2024-01-15 10:25:30 WARN  Request timeout\n")
    f.write("2024-01-15 10:26:02 ERROR GPU OOM\n")
    f.write("2024-01-15 10:26:30 INFO  Service recovered\n")

print("文件已写入: test_log.txt")

# 追加内容（不覆盖）
with open("test_log.txt", "a") as f:
    f.write("2024-01-15 10:30:00 ERROR GPU overheat\n")

print("已追加内容")

# --------------------------------------------------
# 2. 读取文件
# --------------------------------------------------

# 方式1：read() 读取全部内容为一个大字符串
with open("test_log.txt", "r") as f:
    content = f.read()
print("--- read() ---")
print(content)

# 方式2：readlines() 读取所有行为列表
with open("test_log.txt", "r") as f:
    lines = f.readlines()
print("--- readlines() ---")
print(f"共 {len(lines)} 行")
print(lines[0].strip())        # strip() 去掉末尾的 \n

# 方式3：逐行遍历（推荐！内存友好，适合大文件）
print("--- 逐行遍历 ---")
with open("test_log.txt", "r") as f:
    for line in f:
        print(line.strip())

# --------------------------------------------------
# 3. with 语句（重点！）
# --------------------------------------------------
# with 会自动关闭文件，即使出错了也会关
# 永远用 with，不要手动 open/close

# 错误示范（不要这么写）
# f = open("test.txt")
# content = f.read()
# f.close()     # 忘了关就完了

# 正确写法（永远这么写）
# with open("test.txt") as f:
#     content = f.read()
# 出了 with 块，文件自动关了

# --------------------------------------------------
# 4. 文件模式
# --------------------------------------------------
# "r"  读（默认）
# "w"  写（覆盖）
# "a"  追加
# "x"  创建新文件（已存在会报错）
# "rb" / "wb"  二进制读写（图片、压缩包等）

# 创建一个不存在的文件，避免意外覆盖
try:
    with open("test_log.txt", "x") as f:
        f.write("不会执行，因为文件已存在")
except FileExistsError:
    print("文件已存在，跳过创建")

# --------------------------------------------------
# 5. 写入配置文件
# --------------------------------------------------

# 写 JSON 配置
import json

config = {
    "model": "qwen-72b",
    "port": 8000,
    "gpu_count": 4,
    "max_tokens": 2048,
    "servers": ["gpu-01", "gpu-02", "gpu-03"]
}

# 写 JSON
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)      # indent=2 让输出有缩进，好看
print("配置已写入: config.json")

# 读 JSON
with open("config.json", "r") as f:
    loaded_config = json.load(f)
print(f"读取配置: {loaded_config['model']}")

# --------------------------------------------------
# 6. 处理 CSV 文件
# --------------------------------------------------

# 写 CSV
import csv

logs_data = [
    ["timestamp", "level", "server", "message"],
    ["2024-01-15 10:23:01", "INFO", "gpu-01", "Service started"],
    ["2024-01-15 10:25:30", "WARN", "gpu-01", "Request timeout"],
    ["2024-01-15 10:26:02", "ERROR", "gpu-02", "GPU OOM"],
    ["2024-01-15 10:30:00", "ERROR", "gpu-02", "GPU overheat"],
]

with open("logs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(logs_data)
print("CSV 已写入: logs.csv")

# 读 CSV
with open("logs.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)              # 先读表头
    print(f"表头: {header}")
    for row in reader:
        print(f"  {row}")

# 用字典方式读 CSV（更方便）
with open("logs.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["level"] == "ERROR":
            print(f"ERROR: {row['server']} - {row['message']}")

# --------------------------------------------------
# 7. os 模块 —— 文件和目录操作
# --------------------------------------------------

# 获取文件信息
print(f"文件存在: {os.path.exists('test_log.txt')}")
print(f"文件大小: {os.path.getsize('test_log.txt')} 字节")

# 目录操作
os.makedirs("output", exist_ok=True)   # 创建目录（已存在不报错）
print(f"output 目录已创建")

# 列出目录内容
for item in os.listdir("."):
    if item.endswith(".py"):
        print(f"  Python 文件: {item}")

# 路径拼接（推荐用 os.path.join，不要手动拼 /）
log_dir = "output"
log_file = "service.log"
full_path = os.path.join(log_dir, log_file)
print(f"完整路径: {full_path}")

# --------------------------------------------------
# 8. 实战：日志分析器
# --------------------------------------------------

# 创建一个测试日志文件
test_logs = """2024-01-15 10:23:01 INFO  [qwen-72b] Service started on port 8000
2024-01-15 10:23:15 INFO  [qwen-72b] Model loaded, GPU: 4
2024-01-15 10:25:30 WARN  [qwen-72b] Request timeout, client=10.0.1.100
2024-01-15 10:26:02 ERROR [qwen-72b] GPU OOM, used=79.2GB/80GB
2024-01-15 10:26:05 WARN  [qwen-72b] Auto restart triggered
2024-01-15 10:26:30 INFO  [qwen-72b] Service recovered
2024-01-15 10:28:00 INFO  [llama-70b] Service started on port 8001
2024-01-15 10:30:00 ERROR [llama-70b] GPU overheat, temp=92°C
2024-01-15 10:30:15 INFO  [llama-70b] Cooling down, temp=85°C
2024-01-15 10:32:00 INFO  [llama-70b] Service normal
"""

with open("service.log", "w") as f:
    f.write(test_logs)

# 分析日志
print("=== 日志分析器 ===")
stats = {"INFO": 0, "WARN": 0, "ERROR": 0}
error_lines = []

with open("service.log", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        for level in stats:
            if f" {level} " in line:
                stats[level] += 1
                if level == "ERROR":
                    error_lines.append(line)
                break

print(f"\n统计结果:")
for level, count in stats.items():
    print(f"  {level}: {count}")
print(f"  总计: {sum(stats.values())}")

print(f"\nERROR 详情:")
for line in error_lines:
    # 提取时间和消息
    parts = line.split(" ", 3)
    time_str = f"{parts[0]} {parts[1]}"
    msg = parts[3]
    print(f"  [{time_str}] {msg}")

# 把分析结果写入报告
with open("output/report.txt", "w") as f:
    f.write("日志分析报告\n")
    f.write("=" * 40 + "\n")
    f.write(f"生成时间: 2024-01-15 10:35:00\n\n")
    for level, count in stats.items():
        f.write(f"{level}: {count} 次\n")
    f.write(f"\nERROR 详情:\n")
    for line in error_lines:
        f.write(f"  {line}\n")

print("\n分析报告已保存: output/report.txt")

# --------------------------------------------------
# 9. 清理测试文件（运行完可以删掉，留着也行）
# --------------------------------------------------
# import os
# os.remove("test_log.txt")
# os.remove("config.json")
# os.remove("logs.csv")
# os.remove("service.log")
# os.rmdir("output")

# --------------------------------------------------
# 10. 练习
# --------------------------------------------------

# 练习1：写一个函数，统计文件行数
# 输入: 文件路径
# 返回: 行数
# 提示: 用 with open + sum(1 for line in f)

# ====== 在这里写你的代码 ======



# 练习2：写一个函数，把字典列表保存为 CSV
# 输入: 文件路径, 字典列表
# 例: save_csv("servers.csv", [{"name": "gpu-01", "ip": "10.0.0.1"}, ...])

# ====== 在这里写你的代码 ======



# 练习3（挑战）：日志过滤工具
# 函数名: filter_logs(input_file, output_file, level="ERROR")
# 功能: 从输入文件中过滤出指定级别的日志，写入输出文件

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# def count_lines(filepath):
#     with open(filepath, "r") as f:
#         return sum(1 for line in f)
# print(f"行数: {count_lines('test_log.txt')}")

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# def save_csv(filepath, data):
#     if not data:
#         return
#     with open(filepath, "w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=data[0].keys())
#         writer.writeheader()
#         writer.writerows(data)
# test_data = [{"name": "gpu-01", "ip": "10.0.0.1"}, {"name": "gpu-02", "ip": "10.0.0.2"}]
# save_csv("test_servers.csv", test_data)

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# def filter_logs(input_file, output_file, level="ERROR"):
#     with open(input_file, "r") as fin:
#         with open(output_file, "w") as fout:
#             for line in fin:
#                 if f" {level} " in line:
#                     fout.write(line)
# filter_logs("service.log", "output/errors.log", "ERROR")
