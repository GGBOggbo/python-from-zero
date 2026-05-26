# ============================================================
# Day 18: FastAPI 入门
# 目标：能跑起来一个 FastAPI 服务，理解路由和请求处理
# 用法：python day18.py 逐段运行
# ============================================================

# pip install fastapi uvicorn

# --------------------------------------------------
# 1. Hello FastAPI
# --------------------------------------------------
# FastAPI 是 Python 最快的 Web 框架
# 几行代码就能启动一个 API 服务

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="模型服务API")

@app.get("/")
def root():
    return {"message": "Hello FastAPI!"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 启动服务（取消注释运行）
# uvicorn.run(app, host="0.0.0.0", port=8000)
# 然后访问 http://localhost:8000
# 自动文档: http://localhost:8000/docs

# --------------------------------------------------
# 2. 路由（Routing）
# --------------------------------------------------
# @app.get("/path")  → GET 请求
# @app.post("/path") → POST 请求

@app.get("/models")
def list_models():
    return {"models": ["qwen-72b", "llama-70b", "deepseek-v3"]}

@app.get("/gpu/{server_name}")
def gpu_info(server_name: str):
    return {"server": server_name, "gpu_count": 8, "status": "running"}

# 路径参数：{server_name} 从 URL 中取值
# /gpu/gpu-01 → server_name = "gpu-01"

# --------------------------------------------------
# 3. 查询参数
# --------------------------------------------------
@app.get("/search")
def search(q: str = "", limit: int = 10):
    return {"query": q, "limit": limit, "results": []}

# /search?q=gpu&limit=5 → q="gpu", limit=5
# /search → q="", limit=10（默认值）

# --------------------------------------------------
# 4. GET vs POST
# --------------------------------------------------
# GET  = 查数据（参数在 URL 里）
# POST = 提交数据（参数在请求体里）

from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    model: str = "qwen"

@app.post("/chat")
def chat(req: ChatRequest):
    # 这里应该调模型，先返回模拟数据
    return {
        "answer": f"模拟回复: {req.question}",
        "model": req.model
    }

# --------------------------------------------------
# 5. 运行服务
# --------------------------------------------------
# 方式1：代码里启动
# uvicorn.run(app, host="0.0.0.0", port=8000)

# 方式2：命令行启动
# uvicorn day18:app --reload --port 8000

# 自动生成的文档：
# http://localhost:8000/docs        → Swagger UI
# http://localhost:8000/redoc       → ReDoc 文档

# --------------------------------------------------
# 6. 小练习
# --------------------------------------------------

# 练习1：写一个返回服务器列表的 GET 接口
# GET /servers → 返回 [{"name": "gpu-01", "status": "running"}, ...]

# ====== 在这里写你的代码 ======




# 练习2：写一个接收模型名称的 POST 接口
# POST /model/info → 接收 model_name，返回模拟信息

# ====== 在这里写你的代码 ======




# 练习3：写一个健康检查接口
# GET /health → 检查"服务"状态，返回健康信息

# ====== 在这里写你的代码 ======




# 练习1 参考答案
# @app.get("/servers")
# def list_servers():
#     return [
#         {"name": "gpu-01", "status": "running"},
#         {"name": "gpu-02", "status": "running"},
#         {"name": "gpu-03", "status": "offline"},
#     ]

# 练习2 参考答案
# class ModelInfoRequest(BaseModel):
#     model_name: str
# @app.post("/model/info")
# def model_info(req: ModelInfoRequest):
#     return {"name": req.model_name, "size": "72B", "status": "loaded"}

# 练习3 参考答案
# @app.get("/health")
# def health_check():
#     return {"status": "healthy", "uptime": "2h30m", "version": "1.0.0"}
