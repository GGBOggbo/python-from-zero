# ============================================================
# Day 27: RAG + FastAPI 集成
# 目标：把 RAG 系统包装成 API 服务
# 用法：uvicorn day27:app --reload --port 8000
# ============================================================

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Optional
import chromadb

app = FastAPI(title="RAG API 服务")

# --------------------------------------------------
# 1. 初始化向量数据库
# --------------------------------------------------
client = chromadb.Client()
collection = client.create_collection("knowledge_base")

# 预置一些知识
default_docs = [
    "vLLM启动命令: vllm.entrypoints.openai.api_server --model qwen --port 8000",
    "GPU温度告警阈值: 85°C，超过需要检查散热",
    "显存不足解决方案: 减小batch_size或使用GPTQ量化",
    "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader 查温度",
    "推理延迟P99超5秒: 检查并发数和tensor_parallel设置",
]
collection.add(documents=default_docs, ids=[f"d_{i}" for i in range(len(default_docs))])

# --------------------------------------------------
# 2. API 模型
# --------------------------------------------------
class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)

class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    context_used: int

class DocUploadRequest(BaseModel):
    documents: List[str]

# --------------------------------------------------
# 3. 查询接口
# --------------------------------------------------
@app.post("/ask", response_model=AnswerResponse)
def ask(req: QuestionRequest):
    results = collection.query(
        query_texts=[req.question],
        n_results=req.top_k
    )
    sources = results["documents"][0]
    context = "\n".join(f"- {s}" for s in sources)
    answer = f"根据 {len(sources)} 条资料，关于「{req.question}」的回答：{sources[0] if sources else '无相关资料'}"
    return AnswerResponse(
        question=req.question,
        answer=answer,
        sources=sources,
        context_used=len(sources)
    )

# --------------------------------------------------
# 4. 文档管理接口
# --------------------------------------------------
@app.post("/documents")
def add_documents(req: DocUploadRequest):
    start_id = collection.count()
    ids = [f"d_{start_id + i}" for i in range(len(req.documents))]
    collection.add(documents=req.documents, ids=ids)
    return {"added": len(req.documents), "total": collection.count()}

@app.get("/documents/count")
def doc_count():
    return {"total": collection.count()}

@app.delete("/documents")
def clear_documents():
    global collection
    collection = client.create_collection("knowledge_base")
    return {"message": "已清空所有文档"}

# --------------------------------------------------
# 5. 健康检查
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "documents": collection.count()}

# --------------------------------------------------
# 6. 小练习
# --------------------------------------------------

# 练习1：添加一个搜索接口
# GET /search?q=GPU温度&top_k=3 → 返回相关文档列表

# 练习2：添加文件上传接口
# POST /upload → 接收 TXT 文件，自动切割并存入向量库

# 练习3：添加批量问答接口
# POST /ask/batch → 接收多个问题，返回每个答案

# 练习1 参考答案
# @app.get("/search")
# def search(q: str, top_k: int = 3):
#     results = collection.query(query_texts=[q], n_results=top_k)
#     return {"query": q, "results": results["documents"][0]}

# 练习2 参考答案
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     content = await file.read()
#     text = content.decode("utf-8")
#     chunks = [text[i:i+500] for i in range(0, len(text), 450)]
#     start = collection.count()
#     collection.add(documents=chunks, ids=[f"u_{start+i}" for i in range(len(chunks))])
#     return {"filename": file.filename, "chunks": len(chunks)}

# 练习3 参考答案
# class BatchRequest(BaseModel):
#     questions: List[str]
# @app.post("/ask/batch")
# def ask_batch(req: BatchRequest):
#     results = []
#     for q in req.questions:
#         r = collection.query(query_texts=[q], n_results=2)
#         results.append({"question": q, "sources": r["documents"][0]})
#     return {"answers": results}
