# ============================================================
# Day 22: FastAPI 实战 — 模型代理 API 服务
# 目标：写一个完整的模型代理服务，包含路由、鉴权、流式
# 用法：uvicorn day22:app --reload --port 8000
# ============================================================

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="模型代理API", version="1.0.0")

# --------------------------------------------------
# 1. 配置
# --------------------------------------------------
API_KEY = "sk-demo-key"
UPSTREAM_URL = "http://localhost:8000"  # vLLM/SGLang 地址

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# 2. 数据模型
# --------------------------------------------------
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "qwen"
    messages: List[Message]
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, gt=0, le=4096)
    stream: bool = False

class ChatResponse(BaseModel):
    id: str
    model: str
    answer: str
    tokens_used: int
    latency_ms: float

# --------------------------------------------------
# 3. 鉴权
# --------------------------------------------------
async def verify_key(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or auth[7:] != API_KEY:
        raise HTTPException(401, "无效API密钥")

# --------------------------------------------------
# 4. 日志中间件
# --------------------------------------------------
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} {response.status_code} {elapsed:.0f}ms")
    return response

# --------------------------------------------------
# 5. 接口
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "upstream": UPSTREAM_URL}

@app.get("/v1/models")
def list_models(auth=Depends(verify_key)):
    return {"data": [
        {"id": "qwen-72b", "object": "model"},
        {"id": "llama-70b", "object": "model"},
    ]}

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest, auth=Depends(verify_key)):
    if req.stream:
        return StreamingResponse(
            mock_stream(req),
            media_type="text/event-stream"
        )
    start = time.time()
    answer = f"模拟回复: {req.messages[-1].content}"
    return ChatResponse(
        id=f"chatcmpl-{int(time.time())}",
        model=req.model,
        answer=answer,
        tokens_used=len(answer),
        latency_ms=(time.time() - start) * 1000
    )

async def mock_stream(req: ChatRequest):
    answer = f"收到: {req.messages[-1].content}。这是模拟流式回复。"
    for char in answer:
        chunk = {"choices": [{"delta": {"content": char}}]}
        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.02)
    yield "data: [DONE]\n\n"

# --------------------------------------------------
# 6. 启动
# --------------------------------------------------
# uvicorn day22:app --reload --port 8000
# 测试：
# curl http://localhost:8000/health
# curl -H "Authorization: Bearer sk-demo-key" http://localhost:8000/v1/models
# curl -X POST -H "Authorization: Bearer sk-demo-key" -H "Content-Type: application/json" \
#   -d '{"model":"qwen","messages":[{"role":"user","content":"hello"}]}' \
#   http://localhost:8000/v1/chat/completions

# --------------------------------------------------
# 7. 小练习
# --------------------------------------------------

# 练习1：添加 usage 统计接口
# GET /stats → 返回总请求数、平均延迟

# 练习2：添加请求日志存储
# 把每次请求记录到内存列表，提供查询接口

# 练习3：Docker 打包
# 写 Dockerfile 打包这个服务

# 练习1 参考答案
# request_count = 0
# total_latency = 0
# @app.get("/stats")
# def stats():
#     return {"requests": request_count, "avg_latency_ms": total_latency/max(request_count,1)}

# 练习2 参考答案
# request_log = []
# @app.middleware("http")
# async def log_and_store(request: Request, call_next):
#     start = time.time()
#     response = await call_next(request)
#     request_log.append({"path": str(request.url), "status": response.status_code,
#                         "time": time.time()-start})
#     return response
# @app.get("/logs")
# def get_logs(): return request_log[-100:]

# 练习3 参考答案
# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY day22.py app.py
# EXPOSE 8000
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
