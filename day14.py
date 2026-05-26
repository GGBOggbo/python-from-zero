# ============================================================
# Day 14: Pydantic 数据模型
# 目标：会用 BaseModel 定义数据结构，为 FastAPI 做准备
# 用法：python day14.py 逐段运行，改一改，看看结果变不变
# ============================================================

# pip install pydantic
from pydantic import BaseModel, Field
from typing import List, Optional

# --------------------------------------------------
# 1. 为什么需要 Pydantic
# --------------------------------------------------
# API 接收的数据可能是字符串、JSON、各种类型
# Pydantic 帮你自动校验：类型对不对、必填有没有填、值合不合理
# FastAPI 强依赖 Pydantic 做数据校验

# --------------------------------------------------
# 2. BaseModel 基础
# --------------------------------------------------
class ServerInfo(BaseModel):
    name: str
    ip: str
    port: int
    gpu_count: int = 4  # 默认值

# 正常创建
server = ServerInfo(name="gpu-01", ip="10.0.0.1", port=8000)
print(server)
print(f"名称: {server.name}, 端口: {server.port}")

# 使用默认值
server2 = ServerInfo(name="gpu-02", ip="10.0.0.2", port=8001)
print(f"GPU数: {server2.gpu_count}")  # 4（默认值）

# --------------------------------------------------
# 3. 数据校验
# --------------------------------------------------
# 类型自动转换
server3 = ServerInfo(name="gpu-03", ip="10.0.0.3", port="8002")
print(f"port 自动转int: {server3.port} ({type(server3.port)})")

# 校验失败会报错
try:
    bad = ServerInfo(name=123, ip="10.0.0.1")  # 缺 port
except Exception as e:
    print(f"校验失败: {type(e).__name__}")

# --------------------------------------------------
# 4. Field 验证器
# --------------------------------------------------
class ModelConfig(BaseModel):
    name: str = Field(min_length=1, description="模型名称")
    port: int = Field(ge=1024, le=65535, description="端口号")
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)
    max_tokens: int = Field(gt=0, le=32768, default=512)

# 合法配置
config = ModelConfig(name="qwen-72b", port=8000)
print(f"\n配置: {config.name}, temperature={config.temperature}")

# 非法配置
try:
    bad_config = ModelConfig(name="q", port=80)  # port 太小
except Exception as e:
    print(f"端口校验失败: {type(e).__name__}")

# --------------------------------------------------
# 5. Optional 和嵌套模型
# --------------------------------------------------
class GPUInfo(BaseModel):
    index: int
    temperature: float
    utilization: float

class ServerStatus(BaseModel):
    name: str
    ip: str
    gpus: List[GPUInfo]           # 嵌套模型列表
    status: Optional[str] = None  # 可选字段

status = ServerStatus(
    name="gpu-01",
    ip="10.0.0.1",
    gpus=[
        GPUInfo(index=0, temperature=72.5, utilization=85.0),
        GPUInfo(index=1, temperature=68.0, utilization=45.0),
    ]
)
print(f"\n{status.name}: {len(status.gpus)} 张 GPU")
for gpu in status.gpus:
    print(f"  GPU#{gpu.index}: {gpu.temperature}°C, {gpu.utilization}%")

# --------------------------------------------------
# 6. 实际场景：API 请求/响应模型
# --------------------------------------------------
class ChatRequest(BaseModel):
    question: str = Field(min_length=1, description="用户问题")
    model: str = Field(default="qwen2.5", description="模型名")
    max_tokens: int = Field(gt=0, le=4096, default=512)
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)

class ChatResponse(BaseModel):
    answer: str
    model: str
    tokens_used: int
    latency_ms: Optional[float] = None

# 模拟使用
req = ChatRequest(question="GPU温度过高怎么办")
resp = ChatResponse(
    answer="检查风扇转速和散热",
    model="qwen2.5",
    tokens_used=42,
    latency_ms=150.3
)
print(f"\n请求: {req.question}")
print(f"响应: {resp.answer} ({resp.tokens_used} tokens)")

# model_dump() — 转为字典
print(f"\n转为字典: {resp.model_dump()}")

# JSON 序列化
print(f"JSON: {resp.model_dump_json()}")

# --------------------------------------------------
# 7. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：定义服务器信息模型
# 包含 name(str), ip(str), port(int, 1024-65535), gpu_count(int, 默认4)

# ====== 在这里写你的代码 ======




# 练习2：定义 API 请求响应模型
# ChatRequest: question, model(默认"qwen"), max_tokens(默认512)
# ChatResponse: answer, tokens_used

# ====== 在这里写你的代码 ======




# 练习3：嵌套模型
# 定义 GPU(index, temp, util) 和 Cluster(name, servers: List[GPU])
# 创建一个包含 2 个 GPU 的集群并打印

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# from pydantic import BaseModel, Field
# class Server(BaseModel):
#     name: str
#     ip: str
#     port: int = Field(ge=1024, le=65535)
#     gpu_count: int = 4
# s = Server(name="gpu-01", ip="10.0.0.1", port=8000)
# print(s)

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# from pydantic import BaseModel, Field
# class ChatRequest(BaseModel):
#     question: str
#     model: str = "qwen"
#     max_tokens: int = 512
# class ChatResponse(BaseModel):
#     answer: str
#     tokens_used: int
# req = ChatRequest(question="你好")
# resp = ChatResponse(answer="你好！", tokens_used=10)
# print(f"Q: {req.question} → A: {resp.answer}")

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# from pydantic import BaseModel
# from typing import List
# class GPU(BaseModel):
#     index: int
#     temp: float
#     util: float
# class Cluster(BaseModel):
#     name: str
#     gpus: List[GPU]
# c = Cluster(name="gpu-01", gpus=[GPU(index=0, temp=72, util=85), GPU(index=1, temp=68, util=45)])
# for g in c.gpus:
#     print(f"GPU#{g.index}: {g.temp}°C, {g.util}%")
