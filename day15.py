# ============================================================
# Day 15: paramiko 批量 — 多机巡检
# 目标：能同时管理多台服务器，并发执行命令
# 用法：python day15.py 逐段运行，改一改，看看结果变不变
# ============================================================

import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json

# --------------------------------------------------
# 1. 服务器列表管理
# --------------------------------------------------
# 用字典列表管理多台服务器信息

# 服务器清单
servers = [
    {"host": "gpu-01", "ip": "10.0.0.1", "username": "root", "role": "inference"},
    {"host": "gpu-02", "ip": "10.0.0.2", "username": "root", "role": "inference"},
    {"host": "gpu-03", "ip": "10.0.0.3", "username": "root", "role": "training"},
]

# 也可以从 JSON 文件读取
config = {
    "servers": servers,
    "ssh_key": "~/.ssh/id_rsa",
    "timeout": 10,
}
print("服务器清单:")
print(json.dumps(config, ensure_ascii=False, indent=2))

# 从文件读取的写法
# with open("servers.json") as f:
#     config = json.load(f)
#     servers = config["servers"]

# --------------------------------------------------
# 2. 批量执行命令（串行）
# --------------------------------------------------
# 最简单的批量：循环遍历

def batch_exec_serial(servers, command, key_file="~/.ssh/id_rsa"):
    """串行批量执行命令"""
    results = {}

    for srv in servers:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                srv["ip"], username=srv["username"],
                key_filename=key_file, timeout=10
            )
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode("utf-8").strip()
            results[srv["host"]] = {"success": True, "output": output}
            print(f"{srv['host']}: OK")
        except Exception as e:
            results[srv["host"]] = {"success": False, "output": str(e)}
            print(f"{srv['host']}: 失败 - {e}")
        finally:
            client.close()

    return results

# results = batch_exec_serial(servers, "uptime")

# --------------------------------------------------
# 3. 并发执行（线程池）
# --------------------------------------------------
# 串行太慢！10台机器每台等3秒就要30秒
# 用线程池并发执行，10台同时跑只要3秒

def ssh_exec_one(srv, command, key_file="~/.ssh/id_rsa"):
    """SSH 到一台机器执行命令"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            srv["ip"], username=srv["username"],
            key_filename=key_file, timeout=10
        )
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode("utf-8").strip()
        return srv["host"], {"success": True, "output": output}
    except Exception as e:
        return srv["host"], {"success": False, "output": str(e)}
    finally:
        client.close()

def batch_exec_parallel(servers, command, max_workers=5, key_file="~/.ssh/id_rsa"):
    """并发批量执行命令"""
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(ssh_exec_one, srv, command, key_file): srv["host"]
            for srv in servers
        }

        for future in as_completed(futures):
            host, result = future.result()
            results[host] = result
            status = "OK" if result["success"] else "失败"
            print(f"  {host}: {status}")

    return results

# results = batch_exec_parallel(servers, "uptime", max_workers=3)

# --------------------------------------------------
# 4. 结果汇总和格式化
# --------------------------------------------------

def format_results(results, title="巡检结果"):
    """格式化输出巡检结果"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

    success_count = sum(1 for r in results.values() if r["success"])
    print(f"总数: {len(results)}, 成功: {success_count}, 失败: {len(results) - success_count}")
    print(f"{'-'*50}")

    for host, result in results.items():
        status = "成功" if result["success"] else "失败"
        output = result["output"][:100]  # 截断过长的输出
        print(f"  {host:<15} [{status}] {output}")

    print(f"{'='*50}")

# format_results(results, "Uptime 巡检")

# --------------------------------------------------
# 5. 实际场景：多机 GPU 巡检
# --------------------------------------------------

def gpu_check_one(srv, key_file="~/.ssh/id_rsa"):
    """检查一台机器的 GPU 状态"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            srv["ip"], username=srv["username"],
            key_filename=key_file, timeout=10
        )
        cmd = ("nvidia-smi --query-gpu=index,utilization.gpu,"
               "temperature.gpu,memory.used,memory.total "
               "--format=csv,noheader,nounits")
        stdin, stdout, stderr = client.exec_command(cmd)
        output = stdout.read().decode("utf-8").strip()

        gpus = []
        alerts = []
        for line in output.split("\n"):
            parts = [p.strip() for p in line.split(", ")]
            if len(parts) < 5:
                continue
            gpu = {
                "index": parts[0],
                "util": float(parts[1]),
                "temp": float(parts[2]),
                "mem_used": float(parts[3]),
                "mem_total": float(parts[4]),
            }
            gpus.append(gpu)
            # 温度告警
            if gpu["temp"] >= 85:
                alerts.append(f"GPU {gpu['index']} 温度 {gpu['temp']}°C 过高!")

        return srv["host"], {
            "success": True,
            "gpus": gpus,
            "alerts": alerts,
        }
    except Exception as e:
        return srv["host"], {"success": False, "error": str(e)}
    finally:
        client.close()

def batch_gpu_check(servers, max_workers=5):
    """并发多机 GPU 巡检"""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(gpu_check_one, srv) for srv in servers]
        for future in as_completed(futures):
            host, result = future.result()
            results[host] = result
    return results

# results = batch_gpu_check(servers, max_workers=3)
# for host, r in results.items():
#     if r["success"]:
#         print(f"\n{host}:")
#         for gpu in r["gpus"]:
#             print(f"  GPU {gpu['index']}: 利用率 {gpu['util']}%, 温度 {gpu['temp']}°C")
#         if r["alerts"]:
#             for alert in r["alerts"]:
#                 print(f"  [告警] {alert}")

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：多机命令执行器
# 给定服务器列表和命令，批量执行并返回每台的结果

# ====== 在这里写你的代码 ======




# 练习2：并发 GPU 巡检
# 用 ThreadPoolExecutor 并发检查多台 GPU 服务器，汇总结果

# ====== 在这里写你的代码 ======




# 练习3：生成巡检报告
# 将多机巡检结果写入文件，格式化输出

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import paramiko
#
# def batch_exec(servers, command):
#     results = {}
#     for srv in servers:
#         client = paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         try:
#             client.connect(srv["host"], username=srv.get("username", "root"),
#                          key_filename="~/.ssh/id_rsa", timeout=10)
#             stdin, stdout, stderr = client.exec_command(command)
#             results[srv["host"]] = stdout.read().decode("utf-8").strip()
#         except Exception as e:
#             results[srv["host"]] = f"失败: {e}"
#         finally:
#             client.close()
#     return results

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import paramiko
# from concurrent.futures import ThreadPoolExecutor, as_completed
#
# servers = [
#     {"host": "gpu-01", "username": "root"},
#     {"host": "gpu-02", "username": "root"},
#     {"host": "gpu-03", "username": "root"},
# ]
#
# def check_gpu(srv):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         client.connect(srv["host"], username=srv["username"],
#                      key_filename="~/.ssh/id_rsa", timeout=10)
#         stdin, stdout, stderr = client.exec_command(
#             "nvidia-smi --query-gpu=utilization.gpu,temperature.gpu --format=csv,noheader,nounits"
#         )
#         return srv["host"], stdout.read().decode("utf-8").strip()
#     except Exception as e:
#         return srv["host"], f"失败: {e}"
#     finally:
#         client.close()
#
# with ThreadPoolExecutor(max_workers=3) as pool:
#     futures = [pool.submit(check_gpu, srv) for srv in servers]
#     for future in as_completed(futures):
#         host, output = future.result()
#         print(f"{host}: {output}")

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# def generate_report(results, output_file="gpu_report.txt"):
#     from datetime import datetime
#     with open(output_file, "w") as f:
#         f.write(f"GPU 巡检报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
#         f.write("=" * 50 + "\n")
#         for host, info in results.items():
#             f.write(f"\n{host}:\n")
#             if info.get("success"):
#                 for gpu in info.get("gpus", []):
#                     f.write(f"  GPU {gpu['index']}: 利用率 {gpu['util']}%, "
#                            f"温度 {gpu['temp']}°C\n")
#                 for alert in info.get("alerts", []):
#                     f.write(f"  [告警] {alert}\n")
#             else:
#                 f.write(f"  检查失败: {info.get('error', '未知')}\n")
#     print(f"报告已写入: {output_file}")
