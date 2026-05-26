# ============================================================
# Day 23: LangChain 基础
# 目标：能连上本地 vLLM，用 PromptTemplate 构建提示词
# 用法：python day23.py
# ============================================================

# pip install langchain langchain-openai

# --------------------------------------------------
# 1. LangChain 是什么
# --------------------------------------------------
# LangChain 是一个框架，帮你把"大模型 + 外部数据 + 工具"串起来
# 核心概念：Model(模型) + Prompt(提示词) + Chain(链)

# --------------------------------------------------
# 2. 连接本地模型
# --------------------------------------------------
from langchain_openai import ChatOpenAI

# 连接本地 vLLM/SGLang（OpenAI 兼容接口）
llm = ChatOpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",  # 本地不需要 key
    model="qwen",
    temperature=0.7,
)

# 最简单的调用
# response = llm.invoke("GPU温度过高怎么办？")
# print(response.content)

# 没有本地模型也能学语法，用模拟数据
class MockResponse:
    def __init__(self, text):
        self.content = text

def mock_llm(prompt):
    return MockResponse(f"[模拟回复] 收到: {prompt[:50]}...")

resp = mock_llm("GPU温度过高怎么办？")
print(resp.content)

# --------------------------------------------------
# 3. PromptTemplate — 提示词模板
# --------------------------------------------------
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个GPU运维专家，回答简洁专业"),
    ("user", "{question}")
])

# 格式化提示词
formatted = prompt.format(question="GPU利用率100%怎么排查")
print(f"\n格式化后的提示词:\n{formatted}")

# --------------------------------------------------
# 4. Chain — 把提示词和模型串起来
# --------------------------------------------------
# chain = prompt | llm
# result = chain.invoke({"question": "GPU温度过高怎么办"})
# print(result.content)

# 模拟 chain
def mock_chain(question):
    formatted = prompt.format(question=question)
    return mock_llm(formatted)

result = mock_chain("GPU显存不够怎么办")
print(f"\nChain结果: {result.content}")

# --------------------------------------------------
# 5. 输出解析器
# --------------------------------------------------
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
# chain = prompt | llm | parser
# result = chain.invoke({"question": "hello"})
# print(result)  # 直接是字符串，不是对象

# --------------------------------------------------
# 6. 小练习
# --------------------------------------------------

# 练习1：写一个运维助手 PromptTemplate
# system: "你是运维专家"
# user: 包含 {server_name} 和 {error_msg}

# 练习2：构建一个完整的 chain
# prompt | llm | parser

# 练习3：批量提问
# 用 chain.batch() 同时问多个问题

# 练习1 参考答案
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是GPU服务器运维专家"),
#     ("user", "服务器 {server_name} 报错: {error_msg}，请分析原因")
# ])
# print(prompt.format(server_name="gpu-01", error_msg="GPU OOM"))

# 练习2 参考答案
# chain = prompt | llm | StrOutputParser()
# result = chain.invoke({"question": "如何监控GPU温度"})
# print(result)

# 练习3 参考答案
# questions = [{"question": q} for q in ["GPU温度", "显存不足", "推理超时"]]
# results = chain.batch(questions)
# for r in results: print(r)
