# ============================================================
# Day 29: Docker + K8s 部署
# 目标：能把 Python 项目打包成 Docker 镜像并部署
# 用法：python day29.py（阅读为主，实际操作需要 Docker 环境）
# ============================================================

# --------------------------------------------------
# 1. Docker 基础
# --------------------------------------------------
# Docker = 把应用 + 依赖 + 配置 打包成一个"容器"
# 一次构建，到处运行

# Dockerfile 示例（写在实际项目根目录）
dockerfile_content = """
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
print("Dockerfile 内容:")
print(dockerfile_content)

# --------------------------------------------------
# 2. 构建和运行
# --------------------------------------------------
# 构建镜像
# docker build -t my-rag-api:latest .

# 运行容器
# docker run -d -p 8000:8000 --gpus all my-rag-api:latest

# 常用命令
# docker ps                   # 查看运行中的容器
# docker logs <容器ID>        # 查看日志
# docker stop <容器ID>        # 停止
# docker exec -it <ID> bash   # 进入容器

# --------------------------------------------------
# 3. docker-compose 多服务编排
# --------------------------------------------------
compose_content = """
version: '3.8'

services:
  # RAG API 服务
  rag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_URL=http://vllm:8000
    depends_on:
      - vllm
    restart: unless-stopped

  # vLLM 推理服务
  vllm:
    image: vllm/vllm-openai:latest
    command: --model qwen/Qwen2.5-72B --tensor-parallel-size 4
    ports:
      - "8001:8000"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 4
              capabilities: [gpu]
    restart: unless-stopped

  # ChromaDB 向量数据库
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8002:8000"
    volumes:
      - chroma_data:/chroma/chroma
    restart: unless-stopped

volumes:
  chroma_data:
"""
print("\ndocker-compose.yml 内容:")
print(compose_content)

# 使用：
# docker-compose up -d       # 启动所有服务
# docker-compose logs -f      # 查看日志
# docker-compose down         # 停止所有服务

# --------------------------------------------------
# 4. Kubernetes 部署（了解即可）
# --------------------------------------------------
k8s_deployment = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rag-api
  template:
    metadata:
      labels:
        app: rag-api
    spec:
      containers:
      - name: rag-api
        image: my-rag-api:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
---
apiVersion: v1
kind: Service
metadata:
  name: rag-api-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: rag-api
"""
print("\nK8s Deployment:")
print(k8s_deployment)

# kubectl apply -f deployment.yaml
# kubectl get pods
# kubectl logs <pod-name>
# kubectl port-forward svc/rag-api-service 8000:80

# --------------------------------------------------
# 5. 环境变量管理
# --------------------------------------------------
# 用 .env 文件管理配置
env_content = """
MODEL_URL=http://vllm:8000
API_KEY=sk-your-key
CHROMA_URL=http://chromadb:8000
LOG_LEVEL=INFO
MAX_WORKERS=4
"""
print("\n.env 文件:")
print(env_content)

# Python 中读取
# from dotenv import load_dotenv
# import os
# load_dotenv()
# model_url = os.getenv("MODEL_URL", "http://localhost:8000")

# --------------------------------------------------
# 6. 小练习
# --------------------------------------------------

# 练习1：给你的 RAG 项目写一个 Dockerfile

# 练习2：写一个 docker-compose.yml 编排 3 个服务

# 练习3：写一个部署文档 README

# 练习1 参考答案
# FROM python:3.11-slim
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .
# EXPOSE 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 练习2 参考答案
# version: '3.8'
# services:
#   api:
#     build: .
#     ports: ["8000:8000"]
#     depends_on: [db]
#   db:
#     image: chromadb/chroma:latest
#     ports: ["8001:8000"]

# 练习3 参考答案
# # 部署指南
# 1. 构建镜像: docker build -t rag-api .
# 2. 启动服务: docker-compose up -d
# 3. 验证: curl http://localhost:8000/health
# 4. 查看日志: docker-compose logs -f
