# ============================================================
# Day 12: requests 进阶 — 超时/重试/错误处理/流式
# 目标：写生产级 HTTP 请求代码，不怕网络抖动
# 用法：python day12.py 逐段运行，改一改，看看结果变不变
# ============================================================

import requests
import time
import json

# --------------------------------------------------
# 1. 超时设置
# --------------------------------------------------
# 不设超时 = 请求可能永远卡住，这是生产事故的常见原因

# timeout 参数有两种写法
# timeout=5         → 连接+读取共用 5 秒
# timeout=(3, 10)   → 连接超时 3 秒，读取超时 10 秒

# 推荐写法：分别设置
try:
    resp = requests.get("https://httpbin.org/delay/1", timeout=(3, 10))
    print(f"请求成功: {resp.status_code}")
except requests.exceptions.Timeout:
    print("请求超时了！")

# 超时值怎么选？
# 健康检查（/health）: timeout=(2, 3)    # 服务应该秒回
# 普通查询（/v1/models）: timeout=(3, 10)  # 列表查询不急
# 聊天请求（/v1/chat/completions）: timeout=(5, 120)  # 模型推理可能很慢

# --------------------------------------------------
# 2. 错误处理
# --------------------------------------------------
# 网络请求可能出各种错，必须处理

def safe_request_demo():
    """演示各种错误处理"""
    url = "http://localhost:9999/health"  # 假设这个服务不存在

    try:
        resp = requests.get(url, timeout=3)
        resp.raise_for_status()  # 状态码 4xx/5xx 会抛 HTTPError
        return resp.json()
    except requests.exceptions.ConnectionError:
        print("连接失败：服务未启动或地址错误")
    except requests.exceptions.Timeout:
        print("请求超时：服务响应太慢")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误：{e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")

    return None

result = safe_request_demo()
print(f"返回结果: {result}")

# --------------------------------------------------
# 3. 重试机制
# --------------------------------------------------
# 网络偶尔抖动很正常，重试几次就好

def request_with_retry(url, max_retries=3, timeout=5):
    """带重试的请求"""
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            print(f"第 {attempt} 次请求失败: {e}")
            if attempt < max_retries:
                # 指数退避：1秒、2秒、4秒...
                wait = 2 ** (attempt - 1)
                print(f"等待 {wait} 秒后重试...")
                time.sleep(wait)
            else:
                print(f"重试 {max_retries} 次后仍然失败，放弃")
    return None

# 演示（这个 URL 会返回 404，模拟失败）
# resp = request_with_retry("https://httpbin.org/status/404", max_retries=2)

# --------------------------------------------------
# 4. Session 复用连接
# --------------------------------------------------
# 每次 requests.get() 都建新连接，效率低
# 用 Session 复用 TCP 连接，还能统一设置 headers

# 不用 Session（每次都新建连接）
# for i in range(3):
#     requests.get("http://localhost:8000/health")  # 3 次 TCP 握手

# 用 Session（复用连接，快！）
session = requests.Session()
session.headers.update({"Authorization": "Bearer your-token-here"})

# 模拟用 Session 发请求
try:
    resp = session.get("https://httpbin.org/headers", timeout=5)
    print(f"\nSession 请求成功，Headers 里有我们设置的 token")
except Exception:
    pass

# with 语句确保资源释放
with requests.Session() as s:
    s.headers.update({"Content-Type": "application/json"})
    # 所有请求共享这个 header
    # resp = s.get("http://localhost:8000/v1/models")
    # resp = s.post("http://localhost:8000/v1/chat/completions", json=data)
    pass

# --------------------------------------------------
# 5. 流式响应 (Streaming)
# --------------------------------------------------
# 聊天 API 支持 stream=True，逐字返回模型输出
# 就像 ChatGPT 那样一个字一个字蹦出来

def stream_chat(url="http://localhost:8000/v1/chat/completions"):
    """流式请求示例"""
    data = {
        "model": "qwen",
        "messages": [{"role": "user", "content": "用一句话介绍 GPU"}],
        "stream": True,
    }

    try:
        resp = requests.post(url, json=data, stream=True, timeout=120)
        resp.raise_for_status()

        print("模型输出: ", end="")
        for line in resp.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            # SSE 格式: "data: {...}"
            if line.startswith("data: "):
                payload = line[6:]  # 去掉 "data: " 前缀
                if payload == "[DONE]":
                    print("\n[完成]")
                    break
                chunk = json.loads(payload)
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    print(delta["content"], end="", flush=True)
    except Exception as e:
        print(f"流式请求失败: {e}")

# 取消注释运行（需要本地有大模型服务）
# stream_chat()

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：带超时和重试的请求函数
# 写一个函数 safe_get(url, timeout=5, retries=3)
# 实现超时+重试+错误处理，返回 response 或 None

# ====== 在这里写你的代码 ======




# 练习2：批量检查服务状态（健壮版）
# 给定服务列表，用 safe_get 检查每个服务，输出状态表格

# ====== 在这里写你的代码 ======




# 练习3：流式请求示例
# 用 stream=True 调用 /v1/chat/completions，实时打印模型输出

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import requests
# import time
#
# def safe_get(url, timeout=5, retries=3):
#     for attempt in range(1, retries + 1):
#         try:
#             resp = requests.get(url, timeout=timeout)
#             resp.raise_for_status()
#             return resp
#         except requests.exceptions.RequestException as e:
#             print(f"  第 {attempt}/{retries} 次失败: {type(e).__name__}")
#             if attempt < retries:
#                 time.sleep(2 ** (attempt - 1))
#     return None

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# services = [
#     {"name": "vllm-qwen", "url": "http://gpu-01:8000/health"},
#     {"name": "vllm-llama", "url": "http://gpu-02:8000/health"},
#     {"name": "sglang-deepseek", "url": "http://gpu-03:8000/health"},
# ]
#
# print(f"{'服务名':<20} {'状态'}")
# print("-" * 35)
# for svc in services:
#     resp = safe_get(svc["url"], timeout=3, retries=2)
#     status = "正常" if resp else "异常"
#     print(f"{svc['name']:<20} {status}")

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import requests
# import json
#
# url = "http://localhost:8000/v1/chat/completions"
# data = {
#     "model": "qwen",
#     "messages": [{"role": "user", "content": "写一首关于GPU的诗"}],
#     "stream": True,
# }
#
# try:
#     resp = requests.post(url, json=data, stream=True, timeout=120)
#     for line in resp.iter_lines():
#         if not line:
#             continue
#         line = line.decode("utf-8")
#         if line.startswith("data: "):
#             payload = line[6:]
#             if payload == "[DONE]":
#                 break
#             chunk = json.loads(payload)
#             delta = chunk["choices"][0]["delta"]
#             if "content" in delta:
#                 print(delta["content"], end="", flush=True)
#     print()
# except Exception as e:
#     print(f"请求失败: {e}")
