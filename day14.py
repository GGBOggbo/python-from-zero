# ============================================================
# Day 14: paramiko 基础 — SSH 连单台机器
# 目标：能用 Python SSH 到远程服务器执行命令
# 用法：python day14.py 逐段运行，改一改，看看结果变不变
# ============================================================

import paramiko
import os

# --------------------------------------------------
# 1. 安装和连接
# --------------------------------------------------
# pip install paramiko
# SSH 连接三要素：地址、用户名、密码或密钥

# 创建 SSH 客户端
client = paramiko.SSHClient()

# 自动接受未知的主机密钥（开发环境用，生产环境不建议）
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接示例（取消注释运行）
# client.connect(
#     hostname="gpu-01",       # 服务器地址
#     port=22,                 # SSH 端口，默认 22
#     username="root",         # 用户名
#     password="your-password", # 密码（二选一）
#     # key_filename="~/.ssh/id_rsa",  # 密钥文件（二选一）
#     timeout=10,              # 连接超时
# )

# 用完一定要关闭
# client.close()

# 更安全的写法：用 with 自动关闭
# with paramiko.SSHClient() as client:
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect("gpu-01", username="root", password="xxx")
#     # 执行命令...

# --------------------------------------------------
# 2. 执行远程命令
# --------------------------------------------------
# exec_command() 返回 (stdin, stdout, stderr)

def ssh_exec_demo():
    """演示 SSH 执行命令"""
    # 模拟连接（实际环境取消注释）
    # client.connect("gpu-01", username="root", key_filename="~/.ssh/id_rsa")

    # 执行命令
    # stdin, stdout, stderr = client.exec_command("nvidia-smi --query-gpu=index,temperature.gpu --format=csv,noheader")

    # 读取输出
    # output = stdout.read().decode("utf-8")
    # error = stderr.read().decode("utf-8")
    # exit_code = stdout.channel.recv_exit_status()

    # print(f"输出: {output}")
    # print(f"错误: {error}")
    # print(f"退出码: {exit_code}")
    pass

# 实际场景：远程查看 GPU 温度
def check_remote_gpu(host, username="root", key_file=None):
    """SSH 到远程服务器查看 GPU 状态"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接
        if key_file:
            client.connect(host, username=username, key_filename=key_file, timeout=10)
        else:
            print("需要密钥或密码")

        # 执行 nvidia-smi
        stdin, stdout, stderr = client.exec_command(
            "nvidia-smi --query-gpu=index,utilization.gpu,temperature.gpu,memory.used --format=csv,noheader"
        )
        output = stdout.read().decode("utf-8")

        print(f"\n{host} GPU 状态:")
        for line in output.strip().split("\n"):
            print(f"  GPU {line}")

    except paramiko.AuthenticationException:
        print(f"认证失败: {host}")
    except paramiko.SSHException as e:
        print(f"SSH 错误: {e}")
    except Exception as e:
        print(f"连接失败: {e}")
    finally:
        client.close()

# check_remote_gpu("gpu-01", key_file="~/.ssh/id_rsa")

# --------------------------------------------------
# 3. SSH Key 认证
# --------------------------------------------------
# 密码认证不安全，推荐用 SSH Key

# 方式1：默认密钥路径
# client.connect("gpu-01", username="root")

# 方式2：指定密钥文件
# client.connect("gpu-01", username="root", key_filename="/home/user/.ssh/id_rsa")

# 方式3：用密码解密密钥
# private_key = paramiko.RSAKey.from_private_key_file(
#     "/home/user/.ssh/id_rsa",
#     password="key-passphrase"
# )
# client.connect("gpu-01", username="root", pkey=private_key)

# --------------------------------------------------
# 4. 文件传输 (SFTP)
# --------------------------------------------------
# 除了执行命令，还能传文件

def upload_file(host, local_path, remote_path, username="root", key_file=None):
    """通过 SFTP 上传文件"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        connect_kwargs = {"username": username, "timeout": 10}
        if key_file:
            connect_kwargs["key_filename"] = os.path.expanduser(key_file)

        client.connect(host, **connect_kwargs)

        # 打开 SFTP
        sftp = client.open_sftp()
        sftp.put(local_path, remote_path)
        print(f"上传成功: {local_path} → {host}:{remote_path}")
        sftp.close()

    except Exception as e:
        print(f"上传失败: {e}")
    finally:
        client.close()

def download_file(host, remote_path, local_path, username="root", key_file=None):
    """通过 SFTP 下载文件"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        connect_kwargs = {"username": username, "timeout": 10}
        if key_file:
            connect_kwargs["key_filename"] = os.path.expanduser(key_file)

        client.connect(host, **connect_kwargs)

        sftp = client.open_sftp()
        sftp.get(remote_path, local_path)
        print(f"下载成功: {host}:{remote_path} → {local_path}")
        sftp.close()

    except Exception as e:
        print(f"下载失败: {e}")
    finally:
        client.close()

# upload_file("gpu-01", "config.yaml", "/etc/vllm/config.yaml", key_file="~/.ssh/id_rsa")
# download_file("gpu-01", "/var/log/vllm.log", "./vllm.log", key_file="~/.ssh/id_rsa")

# --------------------------------------------------
# 5. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：封装 SSH 执行函数
# 写一个函数 ssh_exec(host, cmd, username="root", key_file=None)
# 返回命令输出字符串

# ====== 在这里写你的代码 ======




# 练习2：远程检查服务状态
# SSH 到远程服务器，执行 systemctl status vllm，判断服务是否运行

# ====== 在这里写你的代码 ======




# 练习3：上传配置文件到远程服务器
# 用 SFTP 将本地配置文件上传到远程服务器

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import paramiko
#
# def ssh_exec(host, cmd, username="root", password=None, key_file=None):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         kwargs = {"hostname": host, "username": username, "timeout": 10}
#         if key_file:
#             kwargs["key_filename"] = key_file]
#         elif password:
#             kwargs["password"] = password
#         client.connect(**kwargs)
#         stdin, stdout, stderr = client.exec_command(cmd)
#         output = stdout.read().decode("utf-8")
#         return output
#     except Exception as e:
#         return f"错误: {e}"
#     finally:
#         client.close()

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import paramiko
#
# def check_remote_service(host, service_name="vllm"):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         client.connect(host, username="root", key_filename="~/.ssh/id_rsa", timeout=10)
#         stdin, stdout, stderr = client.exec_command(f"systemctl is-active {service_name}")
#         status = stdout.read().decode("utf-8").strip()
#         if status == "active":
#             print(f"{host}: {service_name} 运行中")
#         else:
#             print(f"{host}: {service_name} 未运行 (状态: {status})")
#         return status == "active"
#     except Exception as e:
#         print(f"{host}: 检查失败 - {e}")
#         return False
#     finally:
#         client.close()

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import paramiko
# import os
#
# def upload_config(host, local_path, remote_path):
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         client.connect(host, username="root", key_filename="~/.ssh/id_rsa", timeout=10)
#         sftp = client.open_sftp()
#         sftp.put(local_path, remote_path)
#         print(f"上传成功: {local_path} → {host}:{remote_path}")
#         sftp.close()
#     except FileNotFoundError:
#         print(f"本地文件不存在: {local_path}")
#     except Exception as e:
#         print(f"上传失败: {e}")
#     finally:
#         client.close()
