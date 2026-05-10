# ============================================================
# Day 02: 字符串操作
# 目标：能处理日志文本，提取你需要的信息
# 用法：python day02.py
# ============================================================

# --------------------------------------------------
# 1. 字符串基础：单引号、双引号、三引号
# --------------------------------------------------
# 单引号和双引号没区别，选一个用就行

host1 = 'gpu-01'
host2 = "gpu-02"

# 字符串里本身有引号时，外面用另一种
msg = "服务 'gpu-01' 已启动"       # 外面双引号，里面单引号
msg2 = '他说"部署完成"'            # 外面单引号，里面双引号

# 三引号：多行文本
config_text = """
[model]
name=qwen-72b
port=8000
gpu=4
"""
print(config_text)

# --------------------------------------------------
# 2. 索引和切片 —— 取字符串的一部分
# --------------------------------------------------
#        索引:  0 1 2 3 4 5 6 7 8 9
log = "ERROR: GPU-01 OOM"

# 取单个字符（从0开始数）
print(log[0])              # E（第1个字符）
print(log[7])              # G（第8个字符）

# 负数索引：从末尾往前数
print(log[-1])             # M（最后1个字符）
print(log[-4])             # 1（倒数第4个）

# 切片：[起:止] 取起到止之前（不包含止那个位置）
print(log[0:5])            # ERROR（第1到第5个字符）
print(log[7:13])           # GPU-01
print(log[:5])             # ERROR（省略起=从头开始）
print(log[7:])             # GPU-01 OOM（省略止=取到末尾）

# --------------------------------------------------
# 3. 常用方法（最实用的几个，必须记住）
# --------------------------------------------------

log_line = "  ERROR: gpu-01 out of memory  "

# --- 去空白 ---
print(log_line.strip())           # 去掉首尾空白
print(log_line.lstrip())          # 只去左边
print(log_line.rstrip())          # 只去右边

# --- 大小写 ---
print(log_line.upper())           # 全变大写
print(log_line.lower())           # 全变小写
print("qwen-72b".title())        # 首字母大写 → Qwen-72B

# --- 查找 ---
log_clean = "ERROR: gpu-01 out of memory"

print(log_clean.find("gpu"))      # 找位置 → 7（从第7位开始）
print(log_clean.find("xxx"))      # 找不到 → -1
print("gpu" in log_clean)         # 是否包含 → True

print(log_clean.startswith("ERROR"))   # 是否以ERROR开头 → True
print(log_clean.endswith("memory"))    # 是否以memory结尾 → True

print(log_clean.count("o"))       # o出现了几次 → 3

# --- 替换 ---
print(log_clean.replace("ERROR", "WARN"))          # 替换文字
print(log_clean.replace("gpu-01", "gpu-02"))       # 替换服务器名
print(log_clean.replace(" ", ""))                  # 删掉所有空格（替换为空）

# --------------------------------------------------
# 4. split 和 join —— 拆分与合并（超高频使用！）
# --------------------------------------------------

# split：按分隔符拆成列表
log_entry = "2024-01-15 10:30:00 ERROR gpu-01 out of memory"

parts = log_entry.split(" ")      # 按空格拆分
print(parts)
# → ['2024-01-15', '10:30:00', 'ERROR', 'gpu-01', 'out', 'of', 'memory']

# 拆完可以按位置取值
date = parts[0]                   # 2024-01-15
time = parts[1]                   # 10:30:00
level = parts[2]                  # ERROR
server = parts[3]                 # gpu-01

print(f"日期: {date}, 时间: {time}, 级别: {level}, 服务器: {server}")

# 指定拆分次数（只拆前面几个）
csv_line = "qwen-72b,8000,running,4,80.5"
result = csv_line.split(",", 2)   # 只拆2次，后面不拆
print(result)
# → ['qwen-72b', '8000', 'running,4,80.5']

# join：把列表合并成字符串（split 的反操作）
servers = ["gpu-01", "gpu-02", "gpu-03"]
print(",".join(servers))          # gpu-01,gpu-02,gpu-03
print(" -> ".join(servers))       # gpu-01 -> gpu-02 -> gpu-03
print("\n".join(servers))         # 每个服务器一行

# --------------------------------------------------
# 5. f-string 进阶（昨天学了基础，今天加几个技巧）
# --------------------------------------------------

gpu_temp = 87.3456
request_count = 1024
ratio = 0.8567

# 控制小数位数
print(f"温度: {gpu_temp:.1f}°C")          # 保留1位 → 87.3°C
print(f"温度: {gpu_temp:.2f}°C")          # 保留2位 → 87.35°C

# 格式化数字（千位分隔符、补零）
print(f"请求数: {request_count:,}")        # 1,024
print(f"编号: {42:04d}")                   # 0042（补零到4位）

# 百分比
print(f"成功率: {ratio:.1%}")              # 85.7%

# 对齐（生成表格输出时有用）
print(f"{'服务器':<10} {'状态':^8} {'GPU':>4}")
print(f"{'gpu-01':<10} {'running':^8} {4:>4}")
print(f"{'gpu-02':<10} {'stopped':^8} {0:>4}")
# <10 左对齐宽10   ^8 居中宽8   >4 右对齐宽4

# --------------------------------------------------
# 6. 字符串不可变 —— 每次操作都返回新字符串
# --------------------------------------------------

name = "gpu-01"
# name[0] = "G"   # 这行会报错！字符串不能直接改某个字符

# 要"改"只能生成新的
name = "G" + name[1:]
print(name)        # Gpu-01（新字符串）

# --------------------------------------------------
# 7. 实战：从日志中提取关键信息
# --------------------------------------------------
# 模拟一段模型服务日志

logs = """
[2024-01-15 10:23:01] INFO  Service started on port 8000
[2024-01-15 10:23:15] INFO  Model qwen-72b loaded, GPU: 4
[2024-01-15 10:25:30] WARN  Request timeout, client=192.168.1.100
[2024-01-15 10:26:02] ERROR GPU-01 OOM, used=79.2GB/80GB
[2024-01-15 10:26:05] WARN  Auto restart triggered
[2024-01-15 10:26:30] INFO  Service recovered
[2024-01-15 10:30:00] ERROR GPU-02 OOM, used=78.8GB/80GB
"""

print("=== 日志分析 ===")
print()

# 按行拆分
lines = logs.strip().split("\n")
print(f"总日志行数: {len(lines)}")

# 统计各级别出现次数
error_count = 0
warn_count = 0
info_count = 0
error_lines = []

for line in lines:
    if "ERROR" in line:
        error_count += 1
        error_lines.append(line)
    elif "WARN" in line:
        warn_count += 1
    elif "INFO" in line:
        info_count += 1

print(f"ERROR: {error_count} 次")
print(f"WARN:  {warn_count} 次")
print(f"INFO:  {info_count} 次")
print()

# 提取所有 ERROR 行的详情
print("=== ERROR 详情 ===")
for line in error_lines:
    # 提取时间：找 ] 之前的，去掉 [
    time_str = line.split("]")[0].replace("[", "")
    # 提取服务器名
    parts = line.split()
    for part in parts:
        if part.startswith("GPU-"):
            server = part.replace(",", "")
    print(f"时间: {time_str}, 服务器: {server}")

# --------------------------------------------------
# 8. 练习
# --------------------------------------------------

# 练习1：从下面的配置字符串中提取出模型名和端口号
config_str = "model=qwen-72b;port=8000;gpu=4"
# 提示：用 split 拆分，再取值
# 期望输出: 模型名: qwen-72b, 端口: 8000

# ====== 在这里写你的代码 ======



# 练习2：把服务器列表格式化成逗号分隔的字符串，再转回来
server_list = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]


# 步骤1：用 join 把列表变成 "10.0.0.1,10.0.0.2,10.0.0.3"
# 步骤2：用 split 把字符串变回列表
# 步骤3：print 验证

# ====== 在这里写你的代码 ======



# 练习3（挑战）：解析下面的 URL，提取协议、域名、端口、路径
url = "http://gpu-cluster.internal:8080/api/v1/models"
# 期望输出:
# 协议: http
# 域名: gpu-cluster.internal
# 端口: 8080
# 路径: /api/v1/models
# 提示：用 split 多次拆分

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# config_str = "model=qwen-72b;port=8000;gpu=4"
# items = config_str.split(";")
# model = items[0].split("=")[1]    # qwen-72b
# port = items[1].split("=")[1]     # 8000
# print(f"模型名: {model}, 端口: {port}")

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# server_list = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
# joined = ",".join(server_list)
# print(f"合并后: {joined}")
# back = joined.split(",")
# print(f"拆回来: {back}")
# print(f"类型: {type(back)}")

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# url = "http://gpu-cluster.internal:8080/api/v1/models"
# protocol = url.split("://")[0]                          # http
# rest = url.split("://")[1]                              # gpu-cluster.internal:8080/api/v1/models
# domain_port = rest.split("/")[0]                         # gpu-cluster.internal:8080
# path = "/" + "/".join(rest.split("/")[1:])              # /api/v1/models
# domain = domain_port.split(":")[0]                       # gpu-cluster.internal
# port = domain_port.split(":")[1]                         # 8080
# print(f"协议: {protocol}")
# print(f"域名: {domain}")
# print(f"端口: {port}")
# print(f"路径: {path}")
