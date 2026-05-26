# ============================================================
# Day 26: RAG Chain 组装
# 目标：把检索+生成串成完整的 RAG 链路
# 用法：python day26.py
# ============================================================

# --------------------------------------------------
# 1. RAG 全流程
# --------------------------------------------------
# RAG = Retrieval Augmented Generation（检索增强生成）
# 流程：用户提问 → 检索相关文档 → 把文档+问题一起给模型 → 生成回答

# 用户问题: "GPU温度过高怎么办"
#   ↓
# 检索知识库，找到相关文档:
#   "GPU温度超过85度需要检查散热"
#   "nvidia-smi可以查看GPU温度"
#   ↓
# 组装 Prompt:
#   "根据以下资料回答问题：
#    资料1: GPU温度超过85度需要检查散热
#    资料2: nvidia-smi可以查看GPU温度
#    问题: GPU温度过高怎么办"
#   ↓
# 模型生成回答

# --------------------------------------------------
# 2. 模拟 RAG 流程
# --------------------------------------------------

knowledge = [
    "vLLM启动: python -m vllm.entrypoints.openai.api_server --model qwen --port 8000",
    "GPU温度超85°C: 检查风扇转速、散热片、环境温度",
    "显存不足: 减小batch_size、开启量化、增加GPU数量",
    "推理超时: 检查并发请求数、增加tensor_parallel",
    "nvidia-smi查看GPU: 温度、利用率、显存、进程",
]

def simple_search(query, docs, top_k=3):
    """简单关键词检索"""
    scored = []
    query_words = set(query.replace("？", "").replace("怎么", "").split())
    for doc in docs:
        score = sum(1 for w in query_words if w in doc)
        scored.append((doc, score))
    scored.sort(key=lambda x: -x[1])
    return [d for d, s in scored[:top_k]]

def build_rag_prompt(question, context_docs):
    """组装 RAG 提示词"""
    context = "\n".join(f"- {doc}" for doc in context_docs)
    return f"""根据以下参考资料回答问题。如果资料中没有相关信息，请说明。

参考资料:
{context}

问题: {question}
回答:"""

# 模拟完整 RAG
question = "GPU温度过高怎么排查"
retrieved = simple_search(question, knowledge, top_k=3)
prompt = build_rag_prompt(question, retrieved)

print(f"问题: {question}")
print(f"\n检索到 {len(retrieved)} 条相关文档:")
for doc in retrieved:
    print(f"  → {doc}")
print(f"\n最终 Prompt:\n{prompt}")

# --------------------------------------------------
# 3. LangChain RAG Chain
# --------------------------------------------------
# 完整的 LangChain RAG 链路：
#
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_community.vectorstores import Chroma
#
# # 1. 加载向量库
# vectorstore = Chroma.from_texts(knowledge, embeddings)
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
#
# # 2. RAG Prompt
# template = """根据以下资料回答:
# {context}
# 问题: {question}"""
# prompt = ChatPromptTemplate.from_template(template)
#
# # 3. 组装 Chain
# def format_docs(docs):
#     return "\n".join(d.page_content for d in docs)
#
# chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt | llm | StrOutputParser()
# )
#
# # 4. 使用
# answer = chain.invoke("GPU温度过高怎么办")

# --------------------------------------------------
# 4. 小练习
# --------------------------------------------------

# 练习1：写一个 simple_search 函数
# 给定查询和文档列表，返回最相关的3个文档

# 练习2：写一个 build_rag_prompt 函数
# 把检索结果和用户问题组装成提示词

# 练习3：完整 RAG 流程
# 加载文档 → 切割 → 存入向量库 → 检索 → 生成

# 练习1 参考答案
# def simple_search(query, docs, top_k=3):
#     scored = [(doc, sum(1 for w in query.split() if w in doc)) for doc in docs]
#     scored.sort(key=lambda x: -x[1])
#     return [d for d, s in scored[:top_k]]

# 练习2 参考答案
# def build_prompt(question, docs):
#     ctx = "\n".join(f"- {d}" for d in docs)
#     return f"资料:\n{ctx}\n\n问题: {question}\n回答:"

# 练习3 参考答案
# def rag(question, knowledge):
#     docs = simple_search(question, knowledge)
#     prompt = build_prompt(question, docs)
#     return mock_llm(prompt)  # 或 chain.invoke(question)
