# ============================================================
# Day 20: FastAPI 流式输出
# 目标：实现大模型打字机效果的流式响应
# 用法：python day20.py
# ============================================================

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json

app = FastAPI()

# --------------------------------------------------
# 1. StreamingResponse 基础
# --------------------------------------------------
# 普通接口一次性返回全部数据
# StreamingResponse 可以逐块返回，实现"打字机"效果

async def generate_numbers():
    """简单的流式生成器"""
    for i in range(5):
        yield f"data: {i}\n\n"
        await asyncio.sleep(0.5)

@app.get("/stream")
def stream():
    return StreamingResponse(
        generate_numbers(),
        media_type="text/event-stream"
    )

# --------------------------------------------------
# 2. 模拟大模型流式输出
# --------------------------------------------------
async def mock_model_stream(question: str):
    """模拟模型逐字生成"""
    answer = f"收到问题「{question}」，以下是模拟回复：GPU温度管理需要注意散热、监控和自动降频。"
    for char in answer:
        chunk = {"choices": [{"delta": {"content": char}}]}
        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.02)  # 模拟生成延迟
    yield "data: [DONE]\n\n"

class StreamRequest(BaseModel):
    question: str
    model: str = "qwen"

@app.post("/chat/stream")
async def chat_stream(req: StreamRequest):
    return StreamingResponse(
        mock_model_stream(req.question),
        media_type="text/event-stream"
    )

# --------------------------------------------------
# 3. 对比：普通响应 vs 流式响应
# --------------------------------------------------
# 普通响应（等全部生成完才返回）
@app.post("/chat")
async def chat_normal(req: StreamRequest):
    await asyncio.sleep(2)  # 模拟2秒推理
    return {"answer": "这是完整回复，需要等全部生成完", "model": req.model}

# 流式响应（边生成边返回）
# 用户体验：像 ChatGPT 一样一个字一个字出来

# --------------------------------------------------
# 4. 实际调用 vLLM 流式接口
# --------------------------------------------------
import httpx

async def call_vllm_stream(question: str, base_url="http://localhost:8000"):
    """调用真实 vLLM 流式接口"""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{base_url}/v1/chat/completions",
            json={
                "model": "qwen",
                "messages": [{"role": "user", "content": question}],
                "stream": True
            },
            timeout=120
        ) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    yield line + "\n\n"

# pip install httpx

# --------------------------------------------------
# 5. 小练习
# --------------------------------------------------

# 练习1：写一个流式时间接口
# GET /time/stream → 每秒返回当前时间，持续10秒

# 练习2：写一个模拟聊天流式接口
# POST /chat/stream → 逐字返回响应

# 练习3：写一个流式日志接口
# GET /logs/stream → 逐行返回模拟日志

# 练习1 参考答案
# @app.get("/time/stream")
# async def time_stream():
#     async def gen():
#         from datetime import datetime
#         for _ in range(10):
#             yield f"data: {datetime.now().strftime('%H:%M:%S')}\n\n"
#             await asyncio.sleep(1)
#     return StreamingResponse(gen(), media_type="text/event-stream")

# 练习2 参考答案
# async def slow_answer(text):
#     for word in text.split():
#         chunk = {"content": word + " "}
#         yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
#         await asyncio.sleep(0.1)
#     yield "data: [DONE]\n\n"
# @app.post("/chat/stream2")
# async def chat2(req: StreamRequest):
#     return StreamingResponse(slow_answer("模型推理中 GPU 温度正常"), media_type="text/event-stream")

# 练习3 参考答案
# import random
# @app.get("/logs/stream")
# async def log_stream():
#     async def gen():
#         levels = ["INFO", "WARN", "ERROR"]
#         for i in range(20):
#             level = random.choice(levels)
#             yield f"data: [{level}] log entry {i}\n\n"
#             await asyncio.sleep(0.3)
#     return StreamingResponse(gen(), media_type="text/event-stream")
