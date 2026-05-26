# ============================================================
# Day 15: requests 基础 — 调 vLLM/SGLang API
# 目标：会用 requests 库调本地大模型 API
# 用法：python day15.py 逐段运行，改一改，看看结果变不变
# ============================================================

import requests
import json

# --------------------------------------------------
# 1. 安装和第一个请求
# --------------------------------------------------
# pip install requests
# 最常用的 HTTP 库，调 API 必备

# 检查本地 vLLM 服务是否活着（最简单的 GET 请求）
# 如果你有本地部署的 vLLM/SGLang，取消下面的注释运行
# response = requests.get("http://localhost:8000/health")
# print(response.status_code)  # 200 表示正常
# print(response.text)         # 响应内容

# 没有服务也不要紧，先学语法
# 模拟一个请求（用公开测试 API）
try:
    resp = requests.get("https://httpbin.org/get", timeout=5)
    print(f"状态码: {resp.status_code}")
    print(f"响应类型: {type(resp.text)}")
    print(f"响应长度: {len(resp.text)} 字符")
except requests.exceptions.ConnectionError:
    print("网络不可用，没关系，看下面的代码学语法就行")

# --------------------------------------------------
# 2. 请求本地大模型 API
# --------------------------------------------------
# vLLM 和 SGLang 都兼容 OpenAI 接口
# 核心接口: POST /v1/chat/completions

# 请求体结构（这就是你每天用的 ChatGPT 背后发生的事）
chat_request = {
    "model": "qwen-72b",              # 模型名
    "messages": [                      # 对话历史
        {"role": "system", "content": "你是一个运维助手"},
        {"role": "user", "content": "GPU 温度过高怎么办？"}
    ],
    "temperature": 0.7,               # 0=确定，1=随机，推荐 0.7
    "max_tokens": 256,                # 最多生成多少 token
}

print("\n请求体示例:")
print(json.dumps(chat_request, ensure_ascii=False, indent=2))

# 实际发送请求（取消注释运行）
# url = "http://localhost:8000/v1/chat/completions"
# response = requests.post(url, json=chat_request)
# result = response.json()
# print(result["choices"][0]["message"]["content"])

# --------------------------------------------------
# 3. GET vs POST
# --------------------------------------------------
# GET：查询数据，不发送 body
# POST：提交数据，body 里带 JSON

# GET 示例 — 查询已加载的模型列表
# resp = requests.get("http://localhost:8000/v1/models")
# models = resp.json()
# for m in models["data"]:
#     print(m["id"])

# POST 示例 — 发送聊天请求
# headers = {"Content-Type": "application/json"}
# resp = requests.post(
#     "http://localhost:8000/v1/chat/completions",
#     json=chat_request,
#     headers=headers,
# )

# 简单记忆：
# GET  = "给我看看"（查数据）
# POST = "帮我处理"（提交数据）

# --------------------------------------------------
# 4. JSON 处理
# --------------------------------------------------
# API 返回的都是 JSON，必须会解析

# 模拟一个 API 响应
mock_response = {
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "model": "qwen-72b",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "GPU 温度过高时建议：1. 检查风扇转速 2. 降低推理并发 3. 检查环境温度"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 30,
        "total_tokens": 45
    }
}

# 从响应中提取内容（这是最常用的操作）
content = mock_response["choices"][0]["message"]["content"]
print(f"\n模型回复: {content}")

# 提取 token 用量
usage = mock_response["usage"]
print(f"Token 用量: 输入{usage['prompt_tokens']} + 输出{usage['completion_tokens']} = {usage['total_tokens']}")

# --------------------------------------------------
# 5. 实际场景：检查模型服务状态
# --------------------------------------------------
# 运维最常做的事：检查服务是否正常、加载了哪些模型

def check_model_service(base_url="http://localhost:8000"):
    """检查模型服务状态"""
    try:
        # 检查健康状态
        health = requests.get(f"{base_url}/health", timeout=3)
        print(f"服务状态: {'正常' if health.status_code == 200 else '异常'}")

        # 获取模型列表
        models_resp = requests.get(f"{base_url}/v1/models", timeout=3)
        models = models_resp.json()

        print(f"已加载模型: {len(models['data'])} 个")
        for m in models["data"]:
            print(f"  - {m['id']}")

    except requests.exceptions.ConnectionError:
        print(f"无法连接 {base_url}，服务可能未启动")
    except requests.exceptions.Timeout:
        print(f"连接 {base_url} 超时")
    except Exception as e:
        print(f"检查失败: {e}")

# 取消注释运行（需要本地有 vLLM/SGLang 服务）
# check_model_service("http://localhost:8000")

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：调本地 API 获取模型列表
# 用 requests.get() 调 http://localhost:8000/v1/models
# 打印所有模型 ID
# 提示：response.json()["data"] 里有模型列表

# ====== 在这里写你的代码 ======




# 练习2：发送一个聊天请求
# 用 requests.post() 调 http://localhost:8000/v1/chat/completions
# 发送 "你好" 消息，打印模型回复
# 提示：请求体需要 model 和 messages 字段

# ====== 在这里写你的代码 ======




# 练习3：批量检查多个服务状态
# 给定服务列表，逐个检查 /health，输出每个服务状态
# urls = ["http://gpu-01:8000", "http://gpu-02:8000", "http://gpu-03:8000"]

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import requests
#
# try:
#     resp = requests.get("http://localhost:8000/v1/models", timeout=5)
#     data = resp.json()
#     print("已加载的模型:")
#     for m in data["data"]:
#         print(f"  - {m['id']}")
# except requests.exceptions.ConnectionError:
#     print("无法连接服务，请确认 vLLM/SGLang 是否启动")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import requests
#
# url = "http://localhost:8000/v1/chat/completions"
# data = {
#     "model": "qwen",
#     "messages": [
#         {"role": "user", "content": "你好"}
#     ]
# }
#
# try:
#     resp = requests.post(url, json=data, timeout=30)
#     result = resp.json()
#     content = result["choices"][0]["message"]["content"]
#     print(f"模型回复: {content}")
# except requests.exceptions.ConnectionError:
#     print("无法连接服务")

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import requests
#
# urls = ["http://gpu-01:8000", "http://gpu-02:8000", "http://gpu-03:8000"]
#
# for url in urls:
#     try:
#         resp = requests.get(f"{url}/health", timeout=3)
#         status = "正常" if resp.status_code == 200 else f"异常({resp.status_code})"
#         print(f"{url}: {status}")
#     except requests.exceptions.ConnectionError:
#         print(f"{url}: 无法连接")
#     except requests.exceptions.Timeout:
#         print(f"{url}: 响应超时")
