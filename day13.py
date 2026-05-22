# ============================================================
# Day 13: subprocess — 在 Python 里跑系统命令
# 目标：能用 Python 调 nvidia-smi、docker 等运维命令
# 用法：python day13.py 逐段运行，改一改，看看结果变不变
# ============================================================

import subprocess

# --------------------------------------------------
# 1. subprocess.run 基础
# --------------------------------------------------
# 最常用的方式，执行一条命令并等待结果

result = subprocess.run(["echo", "hello from subprocess"], capture_output=True, text=True)
print(f"标准输出: {result.stdout.strip()}")
print(f"返回码: {result.returncode}")  # 0 表示成功

# 关键参数：
# capture_output=True  → 捕获 stdout 和 stderr
# text=True            → 输出是字符串（不是 bytes）
# check=True           → 返回码非 0 时直接抛异常

# --------------------------------------------------
# 2. 获取命令输出
# --------------------------------------------------
# 运维最常用：获取命令输出并解析

# 获取当前 Python 版本
result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
print(f"Python 版本: {result.stdout.strip()}")

# 获取磁盘使用情况
result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
print(f"磁盘信息:\n{result.stdout}")

# 模拟解析 nvidia-smi（实际环境取消注释）
# result = subprocess.run(
#     ["nvidia-smi", "--query-gpu=index,name,utilization.gpu,temperature.gpu,memory.used,memory.total",
#      "--format=csv,noheader,nounits"],
#     capture_output=True, text=True
# )
# for line in result.stdout.strip().split("\n"):
#     parts = line.split(", ")
#     print(f"GPU {parts[0]}: {parts[1]}, 利用率 {parts[2]}%, 温度 {parts[3]}°C")

# 解析 docker ps 输出
# result = subprocess.run(
#     ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
#     capture_output=True, text=True
# )
# print(result.stdout)

# --------------------------------------------------
# 3. 封装常用函数
# --------------------------------------------------
# 每次都写 subprocess.run 太长，封装一下

def run_cmd(cmd, check=False):
    """执行命令，返回 (成功, 标准输出, 错误输出)"""
    try:
        if isinstance(cmd, str):
            cmd = cmd.split()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if check and result.returncode != 0:
            print(f"命令失败: {' '.join(cmd)}")
            print(f"错误: {result.stderr}")
        return result.returncode == 0, result.stdout, result.stderr
    except FileNotFoundError:
        return False, "", f"命令不存在: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return False, "", "命令执行超时"

# 使用封装函数
ok, out, err = run_cmd("python3 --version")
print(f"成功: {ok}, 输出: {out.strip()}")

# --------------------------------------------------
# 4. 管道和 shell=True
# --------------------------------------------------
# 有时需要管道 | 或 shell 特性，用 shell=True
# 但 shell=True 有注入风险，尽量不用

# 不推荐：shell=True（有安全风险）
# subprocess.run("ls -la | grep py", shell=True)

# 推荐：用列表传参（安全）
subprocess.run(["ls", "-la"], capture_output=True, text=True)

# 如果必须用管道，用 Popen 连接
# p1 = subprocess.Popen(["nvidia-smi"], stdout=subprocess.PIPE)
# p2 = subprocess.Popen(["grep", "python"], stdin=p1.stdout, stdout=subprocess.PIPE)
# output = p2.communicate()[0].decode()

# --------------------------------------------------
# 5. 实际场景：GPU 状态巡检脚本
# --------------------------------------------------

def get_gpu_info():
    """获取 GPU 信息（需要 nvidia-smi）"""
    ok, out, err = run_cmd([
        "nvidia-smi",
        "--query-gpu=index,name,utilization.gpu,temperature.gpu,memory.used,memory.total",
        "--format=csv,noheader,nounits"
    ])

    if not ok:
        print(f"获取 GPU 信息失败: {err}")
        return []

    gpus = []
    for line in out.strip().split("\n"):
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        gpu = {
            "index": int(parts[0]),
            "name": parts[1],
            "utilization": float(parts[2]),
            "temperature": float(parts[3]),
            "memory_used": float(parts[4]),
            "memory_total": float(parts[5]),
        }
        gpus.append(gpu)
    return gpus

# 模拟巡检输出（实际环境取消注释 get_gpu_info 调用）
# gpus = get_gpu_info()
# print(f"{'GPU':<6} {'名称':<20} {'利用率':<10} {'温度':<10} {'显存':<15}")
# print("-" * 65)
# for g in gpus:
#     mem_pct = g['memory_used'] / g['memory_total'] * 100
#     print(f"{g['index']:<6} {g['name']:<20} {g['utilization']:.0f}%{'':<6} "
#           f"{g['temperature']:.0f}°C{'':<5} {g['memory_used']}/{g['memory_total']}GB ({mem_pct:.0f}%)")

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：封装 run_cmd 函数
# 接收命令字符串或列表，返回 (success, stdout, stderr)，处理异常

# ====== 在这里写你的代码 ======




# 练习2：GPU 信息采集脚本
# 调用 nvidia-smi，解析输出，打印每张 GPU 的使用率和温度

# ====== 在这里写你的代码 ======




# 练习3：Docker 容器状态检查
# 调 docker ps -a，输出每个容器的名称、状态、端口映射

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import subprocess
#
# def run_cmd(cmd, check=False):
#     try:
#         if isinstance(cmd, str):
#             cmd = cmd.split()
#         result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
#         return result.returncode == 0, result.stdout, result.stderr
#     except FileNotFoundError:
#         return False, "", f"命令不存在: {cmd[0]}"
#     except subprocess.TimeoutExpired:
#         return False, "", "命令执行超时"
#     except Exception as e:
#         return False, "", str(e)
#
# # 测试
# ok, out, err = run_cmd("python3 --version")
# print(f"成功: {ok}, 输出: {out.strip()}")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import subprocess
#
# def get_gpu_info():
#     result = subprocess.run(
#         ["nvidia-smi", "--query-gpu=index,utilization.gpu,temperature.gpu,memory.used,memory.total",
#          "--format=csv,noheader,nounits"],
#         capture_output=True, text=True
#     )
#     if result.returncode != 0:
#         print(f"执行失败: {result.stderr}")
#         return
#
#     print(f"{'GPU':<6} {'利用率':<10} {'温度':<10} {'显存使用':<15}")
#     print("-" * 45)
#     for line in result.stdout.strip().split("\n"):
#         parts = [p.strip() for p in line.split(", ")]
#         mem_pct = float(parts[3]) / float(parts[4]) * 100
#         print(f"{parts[0]:<6} {parts[1]}%{'':<6} {parts[2]}°C{'':<5} "
#               f"{parts[3]}/{parts[4]}GB ({mem_pct:.0f}%)")
#
# get_gpu_info()

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import subprocess
#
# def check_containers():
#     result = subprocess.run(
#         ["docker", "ps", "-a", "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"],
#         capture_output=True, text=True
#     )
#     if result.returncode != 0:
#         print(f"执行失败: {result.stderr}")
#         return
#
#     print(f"{'容器名':<25} {'状态':<20} {'端口'}")
#     print("-" * 70)
#     for line in result.stdout.strip().split("\n"):
#         if not line.strip():
#             continue
#         parts = line.split("\t")
#         name = parts[0] if len(parts) > 0 else ""
#         status = parts[1] if len(parts) > 1 else ""
#         ports = parts[2] if len(parts) > 2 else ""
#         print(f"{name:<25} {status:<20} {ports}")
#
# check_containers()
