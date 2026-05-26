# ============================================================
# Day 12: class 基础认识
# 目标：能看懂别人代码里的 class，能写简单的类
# 用法：python day12.py 逐段运行，改一改，看看结果变不变
# ============================================================

# --------------------------------------------------
# 1. 什么是类（class）
# --------------------------------------------------
# 类 = 模板/图纸，用来创建对象
# 比如 "服务器" 是一个类，gpu-01、gpu-02 是具体的对象（实例）

# 定义一个最简单的类
class Server:
    def __init__(self, name, ip):
        # __init__ 是初始化方法，创建对象时自动调用
        # self 指的是"这个对象本身"
        self.name = name    # 实例属性
        self.ip = ip        # 实例属性

# 创建对象（实例化）
s1 = Server("gpu-01", "10.0.0.1")
s2 = Server("gpu-02", "10.0.0.2")

print(s1.name)  # gpu-01
print(s2.ip)    # 10.0.0.2

# --------------------------------------------------
# 2. 实例方法
# --------------------------------------------------
class GPUServer:
    def __init__(self, name, gpu_count=4):
        self.name = name
        self.gpu_count = gpu_count
        self.status = "offline"  # 默认离线

    def start(self):
        self.status = "running"
        print(f"{self.name} 已启动，{self.gpu_count} 张 GPU")

    def stop(self):
        self.status = "stopped"
        print(f"{self.name} 已停止")

    def info(self):
        print(f"名称: {self.name}, GPU: {self.gpu_count}, 状态: {self.status}")

server = GPUServer("gpu-01", gpu_count=8)
server.start()
server.info()

# --------------------------------------------------
# 3. 不用精通 OOP，能看懂就行
# --------------------------------------------------
# 你在别人代码里会看到这样的东西：
#
# class ModelClient:
#     def __init__(self, base_url, model_name):
#         self.base_url = base_url
#         self.model = model_name
#
#     def chat(self, question):
#         resp = requests.post(f"{self.base_url}/v1/chat/completions", ...)
#         return resp.json()
#
# client = ModelClient("http://localhost:8000", "qwen")
# answer = client.chat("你好")

# 你只需要知道：
# 1. __init__ 是初始化，self.xxx 是属性
# 2. def xxx(self) 是方法，用 对象.方法名() 调用
# 3. 不需要理解继承、多态这些高级概念

# --------------------------------------------------
# 4. 实际场景：定义模型服务类
# --------------------------------------------------
class ModelService:
    def __init__(self, name, port, model_path):
        self.name = name
        self.port = port
        self.model_path = model_path
        self.is_running = False

    def start(self):
        self.is_running = True
        print(f"启动 {self.name}，模型: {self.model_path}，端口: {self.port}")

    def stop(self):
        self.is_running = False
        print(f"停止 {self.name}")

    def check(self):
        status = "运行中" if self.is_running else "已停止"
        print(f"{self.name} ({self.model_path}): {status}")

# 创建多个服务
services = [
    ModelService("vllm-qwen", 8000, "/models/qwen-72b"),
    ModelService("vllm-llama", 8001, "/models/llama-70b"),
    ModelService("sglang-deepseek", 8002, "/models/deepseek-v3"),
]

services[0].start()
services[1].start()

for s in services:
    s.check()

# --------------------------------------------------
# 5. 继承（简单认识）
# --------------------------------------------------
# 继承 = 子类复用父类的代码
# 你可能在 FastAPI/Pydantic 代码里看到：

class BaseService:
    def __init__(self, name):
        self.name = name

    def log(self, msg):
        print(f"[{self.name}] {msg}")

class GPUService(BaseService):  # 继承 BaseService
    def __init__(self, name, gpu_count):
        super().__init__(name)  # 调用父类的 __init__
        self.gpu_count = gpu_count

svc = GPUService("gpu-01", 8)
svc.log(f"有 {svc.gpu_count} 张 GPU")  # 继承来的 log 方法

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：定义 GPU 信息类
# 属性：index, name, temperature, utilization
# 方法：is_overheating() 温度>85返回True

# ====== 在这里写你的代码 ======




# 练习2：定义服务配置类
# 属性：name, port, model, status
# 方法：start(), stop(), __str__ 返回配置字符串

# ====== 在这里写你的代码 ======




# 练习3：用类管理多个服务
# 创建 3 个 ModelService 对象，存入列表，批量启动并检查状态

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# class GPU:
#     def __init__(self, index, name, temperature, utilization):
#         self.index = index
#         self.name = name
#         self.temperature = temperature
#         self.utilization = utilization
#     def is_overheating(self):
#         return self.temperature > 85
# g = GPU(0, "A100", 92, 85)
# print(f"过热: {g.is_overheating()}")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# class ServiceConfig:
#     def __init__(self, name, port, model):
#         self.name = name
#         self.port = port
#         self.model = model
#         self.status = "stopped"
#     def start(self):
#         self.status = "running"
#     def stop(self):
#         self.status = "stopped"
#     def __str__(self):
#         return f"{self.name} ({self.model}) port={self.port} [{self.status}]"
# s = ServiceConfig("vllm", 8000, "qwen")
# s.start()
# print(s)

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# class ModelService:
#     def __init__(self, name, port):
#         self.name = name
#         self.port = port
#         self.status = "stopped"
#     def start(self):
#         self.status = "running"
#         print(f"{self.name} 已启动")
#     def check(self):
#         print(f"{self.name}: {self.status}")
# services = [ModelService("qwen", 8000), ModelService("llama", 8001), ModelService("deepseek", 8002)]
# for s in services:
#     s.start()
# for s in services:
#     s.check()
