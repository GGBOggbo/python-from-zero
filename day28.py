# ============================================================
# Day 28: RAG 流式输出 + 优化
# 目标：给 RAG 服务加上流式输出，优化检索质量
# 用法：uvicorn day28:app --reload --port 8000
# ============================================================

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import asyncio
import json
import chromadb

app = FastAPI(title="RAG 流式服务")

# --------------------------------------------------
# 1. 初始化
# --------------------------------------------------
client = chromadb.Client()
collection = client.create_collection("rag_docs")

docs = [
    "vLLM 是高性能推理引擎，支持 PagedAttention 和连续批处理",
    "SGLang 是另一个推理框架，通过 RadixAttention 优化前缀缓存",
    "GPU 温度管理：nvidia-smi 监控，超过85°C 触发告警",
    "模型量化技术：GPTQ、AWQ、FP8 可减少显存占用50%以上",
    "RAG 系统优化：文档切割大小、检索 top_k、重排序都能影响效果",
]
collection.add(documents=docs, ids=[f"d_{i}" for i in range(len(docs))])

# --------------------------------------------------
# 2. 流式 RAG 接口
# --------------------------------------------------
class StreamQuestion(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)
    stream: bool = True

async def stream_rag_response(question: str, sources: list):
    """流式生成 RAG 回答"""
    context = "\n".join(f"- {s}" for s in sources)
    answer = f"根据 {len(sources)} 条资料回答「{question}」："
    answer += " ".join(sources[:2])

    # 逐字发送
    for char in answer:
        chunk = {"choices": [{"delta": {"content": char}}]}
        yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.01)
    yield "data: [DONE]\n\n"

@app.post("/chat/stream")
async def chat_stream(req: StreamQuestion):
    results = collection.query(query_texts=[req.question], n_results=req.top_k)
    sources = results["documents"][0]

    if req.stream:
        return StreamingResponse(
            stream_rag_response(req.question, sources),
            media_type="text/event-stream"
        )
    else:
        context = "\n".join(f"- {s}" for s in sources)
        return {
            "question": req.question,
            "answer": f"根据资料: {sources[0] if sources else '无'}",
            "sources": sources
        }

# --------------------------------------------------
# 3. 检索优化：查询重写
# --------------------------------------------------
def rewrite_query(query: str) -> str:
    """简单查询重写，提高检索质量"""
    # 去掉无意义词
    stop_words = ["怎么", "如何", "什么", "吗", "呢", "的", "是"]
    words = query
    for w in stop_words:
        words = words.replace(w, "")
    return words.strip() if words.strip() else query

original = "GPU温度过高怎么处理？"
rewritten = rewrite_query(original)
print(f"原查询: {original}")
print(f"重写后: {rewritten}")

# --------------------------------------------------
# 4. 检索优化：结果去重
# --------------------------------------------------
def deduplicate_results(docs: list, threshold: float = 0.9) -> list:
    """去除过于相似的检索结果"""
    if not docs:
        return docs
    unique = [docs[0]]
    for doc in docs[1:]:
        # 简单去重：如果和已有结果重叠字数超过阈值则跳过
        overlap = sum(1 for u in unique if len(set(doc) & set(u)) / max(len(set(doc)), 1) > threshold)
        if overlap == 0:
            unique.append(doc)
    return unique

# --------------------------------------------------
# 5. 小练习
# --------------------------------------------------

# 练习1：给流式接口添加来源信息
# 在流式输出结束后，附上检索来源

# 练习2：实现查询重写
# 把用户的口语化问题重写为更适合检索的关键词

# 练习3：添加评估接口
# GET /eval → 返回一组测试问答的结果

# 练习1 参考答案
# async def stream_with_sources(question, sources):
#     # 先流式输出答案
#     for char in "模拟答案":
#         yield f"data: {json.dumps({'content': char})}\n\n"
#         await asyncio.sleep(0.01)
#     # 最后发来源
#     yield f"data: {json.dumps({'sources': sources})}\n\n"
#     yield "data: [DONE]\n\n"

# 练习2 参考答案
# def rewrite_query(query):
#     replacements = {"怎么": "方法", "如何": "方案", "为什么": "原因"}
#     for old, new in replacements.items():
#         query = query.replace(old, new)
#     return query

# 练习3 参考答案
# test_cases = [
#     {"q": "GPU温度", "expected": "散热"},
#     {"q": "推理慢", "expected": "并发"},
# ]
# @app.get("/eval")
# def evaluate():
#     results = []
#     for tc in test_cases:
#         r = collection.query(query_texts=[tc["q"]], n_results=1)
#         hit = tc["expected"] in r["documents"][0][0]
#         results.append({"q": tc["q"], "hit": hit})
#     return {"accuracy": sum(r["hit"] for r in results) / len(results), "details": results}
