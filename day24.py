# ============================================================
# Day 24: 向量数据库
# 目标：理解 Embedding 和向量检索，会用 Chroma 存取文档
# 用法：python day24.py
# ============================================================

# pip install chromadb sentence-transformers

# --------------------------------------------------
# 1. 什么是 Embedding（向量化）
# --------------------------------------------------
# 把文本变成一组数字（向量），语义相近的文本向量也相近
# 比如 "GPU过热" 和 "显卡温度高" 的向量很接近
# 这样就能通过数学计算找到"意思相近"的文本

# 模拟 Embedding（实际用 sentence-transformers）
def mock_embed(text):
    """模拟：把文本变成固定长度的向量"""
    import hashlib
    h = hashlib.md5(text.encode()).hexdigest()
    return [int(h[i:i+2], 16) / 255 for i in range(0, 32, 2)]

vec = mock_embed("GPU温度过高")
print(f"向量维度: {len(vec)}, 示例: {vec[:3]}")

# --------------------------------------------------
# 2. 向量相似度
# --------------------------------------------------
def cosine_sim(a, b):
    """余弦相似度（越接近1越相似）"""
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = sum(x**2 for x in a)**0.5
    norm_b = sum(x**2 for x in b)**0.5
    return dot / (norm_a * norm_b)

v1 = mock_embed("GPU温度过高")
v2 = mock_embed("显卡温度很高")
v3 = mock_embed("今天天气不错")

print(f"\nGPU温度 vs 显卡温度: {cosine_sim(v1, v2):.3f}")
print(f"GPU温度 vs 天气: {cosine_sim(v1, v3):.3f}")

# --------------------------------------------------
# 3. Chroma 向量数据库
# --------------------------------------------------
import chromadb

# 创建内存数据库
client = chromadb.Client()

# 创建集合
collection = client.create_collection("docs")

# 添加文档
docs = [
    "GPU温度超过85度需要检查散热系统",
    "显存不足时可以降低batch_size或使用量化",
    "模型推理超时可能是并发请求过多",
    "nvidia-smi可以查看GPU使用率和温度",
    "Docker容器GPU直通需要安装nvidia-container-toolkit",
]
ids = [f"doc_{i}" for i in range(len(docs))]

collection.add(documents=docs, ids=ids)
print(f"\n已添加 {len(docs)} 个文档到 Chroma")

# --------------------------------------------------
# 4. 向量检索（最核心的操作）
# --------------------------------------------------
results = collection.query(
    query_texts=["GPU温度高怎么办"],
    n_results=3  # 返回最相似的3个
)
print("\n查询: GPU温度高怎么办")
for doc, score in zip(results["documents"][0], results["distances"][0]):
    print(f"  [{score:.3f}] {doc}")

# --------------------------------------------------
# 5. 实际场景：知识库检索
# --------------------------------------------------
def build_knowledge_base(documents):
    """从文档列表构建知识库"""
    client = chromadb.Client()
    col = client.create_collection("knowledge")
    col.add(
        documents=documents,
        ids=[f"k_{i}" for i in range(len(documents))]
    )
    return col

def search_kb(collection, query, top_k=3):
    """检索知识库"""
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0]

# 模拟运维知识库
kb_docs = [
    "vLLM启动命令: python -m vllm.entrypoints.openai.api_server --model qwen --port 8000",
    "SGLang默认端口8000，可通过--port参数修改",
    "OOM错误：减少max_model_len或增加GPU数量",
    "推理速度慢：检查GPU利用率，考虑增加tensor_parallel_size",
    "流式输出：设置stream=True参数",
]
kb = build_knowledge_base(kb_docs)
print("\n知识库查询:")
for r in search_kb(kb, "推理太慢怎么优化"):
    print(f"  → {r}")

# --------------------------------------------------
# 6. 小练习
# --------------------------------------------------

# 练习1：构建自己的文档库并检索
# 添加5条关于Docker的文档，查询"Docker容器怎么查看日志"

# 练习2：对比不同查询的检索结果
# 用3个不同的查询词，看返回结果的区别

# 练习3：结合 LangChain 使用 Chroma
# 用 Chroma.as_retriever() 构建检索器

# 练习1 参考答案
# client = chromadb.Client()
# col = client.create_collection("docker_docs")
# col.add(documents=[
#     "docker logs <容器名> 查看容器日志",
#     "docker ps 查看运行中容器",
#     "docker exec -it <容器名> bash 进入容器",
#     "docker-compose up -d 启动所有服务",
#     "docker stats 查看容器资源使用",
# ], ids=[f"d_{i}" for i in range(5)])
# print(col.query(query_texts=["查看日志"], n_results=2))

# 练习2 参考答案
# queries = ["GPU温度", "显存不足", "启动服务"]
# for q in queries:
#     print(f"\n查询: {q}")
#     for r in search_kb(kb, q, top_k=2):
#         print(f"  → {r}")

# 练习3 参考答案
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# vectorstore = Chroma.from_texts(kb_docs, embeddings)
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
# docs = retriever.invoke("推理慢")
# for d in docs: print(d.page_content)
