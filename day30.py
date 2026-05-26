# ============================================================
# Day 30: GitHub + CSDN 博客 — 输出成果
# 目标：把你的项目发布到 GitHub，写一篇技术博客
# 用法：python day30.py（阅读为主）
# ============================================================

# --------------------------------------------------
# 1. 项目 README 撰写
# --------------------------------------------------
# README 是项目的门面，必须写好

readme_template = """
# RAG 模型服务 API

基于 FastAPI + LangChain + ChromaDB 构建的 RAG 问答系统。

## 功能
- 文档上传和自动切割
- 向量检索 + 大模型生成
- 流式输出（打字机效果）
- API 鉴权
- Docker 一键部署

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --port 8000

# Docker 启动
docker-compose up -d
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /health | GET | 健康检查 |
| /ask | POST | 问答接口 |
| /chat/stream | POST | 流式问答 |
| /documents | POST | 上传文档 |

## 技术栈
- FastAPI + Uvicorn
- LangChain + ChromaDB
- vLLM / SGLang
- Docker + docker-compose
"""

print("README 模板:")
print(readme_template)

# --------------------------------------------------
# 2. GitHub 发布
# --------------------------------------------------
# git 命令回顾

git_commands = """
# 初始化仓库
git init
git remote add origin https://github.com/yourname/your-repo.git

# 日常操作
git add .
git commit -m "feat: 添加 RAG 问答功能"
git push origin main

# .gitignore（重要！不要上传敏感信息）
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "chroma_data/" >> .gitignore
"""
print("\nGit 命令:")
print(git_commands)

# --------------------------------------------------
# 3. 技术博客写作
# --------------------------------------------------
# CSDN / 掘金 / 知乎 发技术博客

blog_outline = """
# 博客大纲

## 标题
《30天从零搭建 RAG 知识库问答系统 — 运维工程师的 Python 进阶之路》

## 结构
1. 背景和动机
   - 为什么运维工程师需要学 Python
   - 为什么选择 RAG 作为学习项目

2. 技术选型
   - FastAPI vs Flask
   - ChromaDB vs Milvus
   - vLLM vs SGLang

3. 核心实现
   - 文档加载和切割
   - 向量检索
   - Prompt 工程
   - 流式输出

4. 踩坑记录（最有价值！）
   - GPU 显存不够怎么办
   - 检索结果不准怎么优化
   - Docker 部署遇到的坑

5. 效果展示
   - 截图/GIF
   - 性能数据

6. 总结和展望
"""
print("\n博客大纲:")
print(blog_outline)

# --------------------------------------------------
# 4. 博客写作技巧
# --------------------------------------------------
tips = """
技术博客写作要点：

1. 标题要具体（不要"我的学习笔记"，要"30天搭建RAG系统"）
2. 开头说清"这篇写给谁看""能学到什么"
3. 代码要能跑，加上注释
4. 踩坑比成功更有价值，一定要写
5. 截图/GIF 比文字更有说服力
6. 结尾总结收获，别只说"学到了很多"
"""
print(tips)

# --------------------------------------------------
# 5. 30天回顾
# --------------------------------------------------
summary = """
30天学习路线回顾：

基础阶段 (Day 1-5)
  变量、字符串、列表、字典、JSON

核心阶段 (Day 6-11)
  if/else、循环、函数、文件读写、异常处理、模块

进阶阶段 (Day 12-14)
  class、装饰器+async、Pydantic

实战阶段 (Day 15-17)
  requests、subprocess

FastAPI阶段 (Day 18-22)
  路由、请求体、流式输出、中间件、实战项目

RAG阶段 (Day 23-28)
  LangChain、向量数据库、文档切割、RAG Chain、API集成、流式

项目收尾 (Day 29-30)
  Docker部署、博客发布

恭喜完成30天学习！
"""
print(summary)

# --------------------------------------------------
# 6. 小练习
# --------------------------------------------------

# 练习1：为你的项目写一个 README.md

# 练习2：写一篇技术博客（500字以上）

# 练习3：把项目推送到 GitHub，确保 README 正常显示
