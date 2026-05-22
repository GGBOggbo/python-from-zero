# ============================================================
# Day 16: docker-py 基础 — 列出/启停容器
# 目标：能用 Python 管理 Docker 容器
# 用法：python day16.py 逐段运行，改一改，看看结果变不变
# ============================================================

import docker

# --------------------------------------------------
# 1. 安装和连接 Docker
# --------------------------------------------------
# pip install docker
# 前提：Docker 守护进程在运行

# 连接本地 Docker
try:
    client = docker.from_env()
    # 测试连接
    client.ping()
    print("Docker 连接成功")
except docker.errors.DockerException:
    print("Docker 未运行或权限不足")
    print("解决：sudo usermod -aG docker $user && 重新登录")
except Exception as e:
    print(f"连接失败: {e}")

# 连接远程 Docker
# client = docker.DockerClient(base_url="tcp://gpu-01:2375")

# --------------------------------------------------
# 2. 列出容器
# --------------------------------------------------

# 列出运行中的容器
containers = client.containers.list()
print(f"\n运行中容器: {len(containers)} 个")
for c in containers:
    print(f"  - {c.name}: {c.status} ({c.image.tags})")

# 列出所有容器（包括停止的）
all_containers = client.containers.list(all=True)
print(f"\n所有容器: {len(all_containers)} 个")
for c in all_containers:
    print(f"  - {c.name}: {c.status}")

# 过滤容器（按名称、状态等）
# inference_containers = client.containers.list(filters={"name": "vllm"})
# running = client.containers.list(filters={"status": "running"})

# 容器属性
# c.name          → 容器名称
# c.status        → 状态 (running, exited, paused...)
# c.image.tags    → 镜像标签
# c.ports         → 端口映射
# c.attrs         → 完整配置（字典）

# --------------------------------------------------
# 3. 容器生命周期
# --------------------------------------------------

def safe_restart(container_name):
    """安全重启容器"""
    try:
        container = client.containers.get(container_name)
        print(f"重启 {container_name} (当前状态: {container.status})")
        container.restart(timeout=10)  # 给 10 秒优雅关闭
        container.reload()  # 刷新状态
        print(f"重启完成 (新状态: {container.status})")
        return True
    except docker.errors.NotFound:
        print(f"容器不存在: {container_name}")
        return False
    except docker.errors.APIError as e:
        print(f"操作失败: {e}")
        return False

# safe_restart("vllm-qwen")

# 其他生命周期操作
# container.start()    → 启动
# container.stop()     → 停止
# container.restart()  → 重启
# container.pause()    → 暂停
# container.unpause()  → 恢复
# container.remove()   → 删除（需先 stop）
# container.kill()     → 强制停止

# --------------------------------------------------
# 4. 镜像管理
# --------------------------------------------------

# 列出镜像
images = client.images.list()
print(f"\n本地镜像: {len(images)} 个")
for img in images:
    tags = ", ".join(img.tags) if img.tags else "<none>"
    size_gb = img.attrs["Size"] / (1024**3)
    print(f"  - {tags} ({size_gb:.1f} GB)")

# 拉取镜像
# image = client.images.pull("vllm/vllm-openai:latest")
# print(f"拉取成功: {image.tags}")

# 删除镜像
# client.images.remove("vllm/vllm-openai:old-version")

# --------------------------------------------------
# 5. 实际场景：管理模型推理容器
# --------------------------------------------------

def list_inference_containers():
    """列出所有推理服务容器"""
    all_c = client.containers.list(all=True)
    inference = [c for c in all_c if "vllm" in c.name or "sglang" in c.name or "triton" in c.name]

    print(f"\n推理服务容器: {len(inference)} 个")
    print(f"{'名称':<25} {'状态':<15} {'镜像'}")
    print("-" * 65)
    for c in inference:
        tags = ", ".join(c.image.tags[:1]) if c.image.tags else "<none>"
        print(f"{c.name:<25} {c.status:<15} {tags}")

    return inference

# list_inference_containers()

def restart_stopped_services():
    """重启所有已停止的推理服务"""
    all_c = client.containers.list(all=True)
    restarted = []

    for c in all_c:
        if c.status == "exited" and ("vllm" in c.name or "sglang" in c.name):
            print(f"重启 {c.name}...")
            c.start()
            restarted.append(c.name)

    if restarted:
        print(f"已重启 {len(restarted)} 个服务: {restarted}")
    else:
        print("没有需要重启的服务")

# restart_stopped_services()

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：列出所有容器及状态
# 连接 Docker，列出所有容器，打印名称、镜像、状态、端口

# ====== 在这里写你的代码 ======




# 练习2：按名称过滤并重启容器
# 找到名称包含 "vllm" 的容器，重启状态异常的

# ====== 在这里写你的代码 ======




# 练习3：批量启停服务
# 按列表启停指定容器，等待状态变化

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import docker
#
# def list_containers():
#     client = docker.from_env()
#     containers = client.containers.list(all=True)
#     print(f"{'名称':<25} {'镜像':<30} {'状态':<15} {'端口'}")
#     print("-" * 80)
#     for c in containers:
#         tags = ", ".join(c.image.tags[:1]) if c.image.tags else "<none>"
#         ports = ", ".join([f"{p}" for p in c.ports.values()]) if c.ports else ""
#         print(f"{c.name:<25} {tags:<30} {c.status:<15} {ports}")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import docker
#
# def restart_service_containers(keyword="vllm"):
#     client = docker.from_env()
#     all_c = client.containers.list(all=True)
#     for c in all_c:
#         if keyword in c.name and c.status != "running":
#             print(f"重启 {c.name} (状态: {c.status})")
#             c.start()
#         elif keyword in c.name:
#             print(f"{c.name} 已在运行中")

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import docker
# import time
#
# def manage_containers(names, action="start"):
#     client = docker.from_env()
#     for name in names:
#         try:
#             c = client.containers.get(name)
#             getattr(c, action)()
#             print(f"{action} {name}: 执行中...")
#             time.sleep(2)
#             c.reload()
#             print(f"  当前状态: {c.status}")
#         except docker.errors.NotFound:
#             print(f"容器不存在: {name}")
