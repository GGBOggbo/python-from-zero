# ============================================================
# Day 25: 文档加载 + 切割
# 目标：能把 PDF/TXT/Markdown 加载并切割成文本块
# 用法：python day25.py
# ============================================================

# --------------------------------------------------
# 1. 文档加载概述
# --------------------------------------------------
# RAG 的第一步：把各种格式的文档加载进来
# LangChain 提供了很多 Loader：
# TextLoader, PyPDFLoader, UnstructuredMarkdownLoader 等

# --------------------------------------------------
# 2. 加载 TXT 文件
# --------------------------------------------------
# 最简单的文档加载
sample_text = """GPU服务器运维手册

第一章：日常巡检
1. 每天检查 GPU 温度，超过85°C需要告警
2. 每小时检查显存使用率，超过90%需要关注
3. 每天检查模型推理延迟，P99超过5秒需要优化

第二章：故障处理
1. OOM错误：减少batch_size或增加GPU
2. 推理超时：检查请求队列长度
3. GPU掉卡：重启nvidia驱动

第三章：性能优化
1. 开启Flash Attention加速推理
2. 使用vLLM的PagedAttention管理显存
3. 合理设置max_model_len参数
"""

with open("sample_doc.txt", "w") as f:
    f.write(sample_text)

with open("sample_doc.txt", "r") as f:
    content = f.read()
print(f"文档长度: {len(content)} 字符")
print(f"前100字: {content[:100]}...")

# --------------------------------------------------
# 3. 文本切割（最关键的一步）
# --------------------------------------------------
# 文档太长不能直接塞给模型，需要切成小块
# 关键参数：
#   chunk_size — 每块多大（字符数）
#   chunk_overlap — 相邻块的重叠（防止信息被截断）

def simple_split(text, chunk_size=200, overlap=50):
    """简单的文本切割"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

chunks = simple_split(content, chunk_size=200, overlap=50)
print(f"\n切割结果: {len(chunks)} 块")
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- 块 {i+1} ({len(chunk)} 字符) ---")
    print(chunk[:100] + "...")

# --------------------------------------------------
# 4. LangChain 的文本切割器
# --------------------------------------------------
# RecursiveCharacterTextSplitter — 推荐，按段落/句子智能切割
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,       # 每块500字符
#     chunk_overlap=100,    # 重叠100字符
#     separators=["\n\n", "\n", "。", "，", " "]  # 优先按这些分隔
# )
# chunks = splitter.split_text(content)

# --------------------------------------------------
# 5. 按章节切割（运维文档推荐）
# --------------------------------------------------
def split_by_chapter(text, chapter_marker="第"):
    """按章节标题切割"""
    chapters = []
    current = []
    for line in text.split("\n"):
        if line.strip().startswith(chapter_marker) and "章" in line:
            if current:
                chapters.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        chapters.append("\n".join(current))
    return chapters

chapters = split_by_chapter(content)
print(f"\n按章节切割: {len(chapters)} 章")
for ch in chapters:
    title = ch.split("\n")[0]
    print(f"  {title} ({len(ch)} 字符)")

# --------------------------------------------------
# 6. 加载 PDF 文件（了解即可）
# --------------------------------------------------
# pip install pypdf
# from pypdf import PdfReader
# reader = PdfReader("manual.pdf")
# text = ""
# for page in reader.pages:
#     text += page.extract_text()

# --------------------------------------------------
# 7. 小练习
# --------------------------------------------------

# 练习1：加载一个 TXT 文件并按固定大小切割
# chunk_size=300, overlap=80

# 练习2：按章节切割，输出每章的标题和字数

# 练习3：写一个完整的 文档加载→切割→打印 流程

# 练习1 参考答案
# def load_and_split(filepath, chunk_size=300, overlap=80):
#     with open(filepath) as f:
#         text = f.read()
#     return simple_split(text, chunk_size, overlap)
# for i, chunk in enumerate(load_and_split("sample_doc.txt")):
#     print(f"块{i+1}: {chunk[:50]}...")

# 练习2 参考答案
# chapters = split_by_chapter(content)
# for ch in chapters:
#     title = ch.split("\n")[0]
#     print(f"{title}: {len(ch)} 字符, {len(ch.split())} 词")

# 练习3 参考答案
# def process_document(filepath):
#     with open(filepath) as f:
#         text = f.read()
#     print(f"原文: {len(text)} 字符")
#     chunks = simple_split(text, 300, 80)
#     print(f"切割: {len(chunks)} 块")
#     return chunks
# process_document("sample_doc.txt")

import os
os.remove("sample_doc.txt")
