# ============================================================
# Day 13: 装饰器 + async/await
# 目标：能看懂装饰器和异步代码，为学 FastAPI 做准备
# 用法：python day13.py 逐段运行，改一改，看看结果变不变
# ============================================================

import time
import asyncio

# --------------------------------------------------
# 1. 装饰器：@xxx 就是给函数"包一层"
# --------------------------------------------------
# 你不需要理解装饰器的原理
# 只需要知道：@xxx 写在函数上面，会给函数增加功能

# FastAPI 里你会看到这样的代码：
# @app.get("/chat")
# async def chat(question: str):
#     return {"answer": "hello"}

# @app.get("/chat") 就是一个装饰器
# 它把普通函数变成了一个 API 接口

# --------------------------------------------------
# 2. 写一个简单装饰器（了解即可）
# --------------------------------------------------
def timer(func):
    """计算函数执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  耗时: {elapsed:.3f}秒")
        return result
    return wrapper

@timer
def slow_task():
    """被装饰的函数"""
    time.sleep(0.1)
    print("任务完成")

slow_task()  # 自动打印耗时

# 等价于：
# slow_task = timer(slow_task)

# --------------------------------------------------
# 3. 常见装饰器
# --------------------------------------------------

# @property — 把方法变成属性
class Server:
    def __init__(self, name, gpu_count):
        self.name = name
        self.gpu_count = gpu_count

    @property
    def info(self):
        return f"{self.name} ({self.gpu_count} GPUs)"

s = Server("gpu-01", 8)
print(s.info)  # 注意：不用加括号

# @staticmethod — 不需要 self 的方法
class Math:
    @staticmethod
    def add(a, b):
        return a + b

print(Math.add(1, 2))

# --------------------------------------------------
# 4. async/await 基础
# --------------------------------------------------
# async def 定义异步函数
# await 等待异步操作完成
# 好处：等待的时候不阻塞其他请求

# 同步版本（一个一个等）
def sync_call(name, seconds):
    print(f"  开始: {name}")
    time.sleep(seconds)
    print(f"  完成: {name}")

# 异步版本（等待时可以干别的）
async def async_call(name, seconds):
    print(f"  开始: {name}")
    await asyncio.sleep(seconds)  # 非阻塞等待
    print(f"  完成: {name}")

# --------------------------------------------------
# 5. asyncio.gather — 同时做多个事
# --------------------------------------------------
async def main():
    # 同时发3个请求，总时间 = 最慢的那个
    print("=== 并发执行 ===")
    await asyncio.gather(
        async_call("请求A", 0.3),
        async_call("请求B", 0.2),
        async_call("请求C", 0.1),
    )

asyncio.run(main())

# 对比同步执行（串行）
print("\n=== 串行执行 ===")
start = time.time()
sync_call("请求A", 0.3)
sync_call("请求B", 0.2)
sync_call("请求C", 0.1)
print(f"串行总耗时: {time.time()-start:.1f}秒")

# --------------------------------------------------
# 6. 为什么要学这个？因为 FastAPI！
# --------------------------------------------------
# FastAPI 的每个接口都长这样：
#
# from fastapi import FastAPI
# app = FastAPI()
#
# @app.get("/chat")              # ← 装饰器
# async def chat(question: str): # ← 异步函数
#     result = await call_model(question)  # ← await
#     return result
#
# 不懂装饰器和 async，FastAPI 代码你一行都看不懂

# 模拟 FastAPI 风格
async def call_model(question):
    await asyncio.sleep(0.1)  # 模拟模型推理
    return f"回答: {question}"

async def chat(question: str):
    result = await call_model(question)
    return result

answer = asyncio.run(chat("GPU温度过高怎么办"))
print(f"\n{answer}")

# --------------------------------------------------
# 7. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：写一个计时装饰器
# 给任意函数加执行时间打印

# ====== 在这里写你的代码 ======




# 练习2：异步请求函数
# 用 async def + asyncio.sleep 模拟异步 API 调用

# ====== 在这里写你的代码 ======




# 练习3：asyncio.gather 并发请求
# 同时发 5 个模拟请求，打印总耗时

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import time
# def timer(func):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         result = func(*args, **kwargs)
#         print(f"{func.__name__} 耗时: {time.time()-start:.3f}秒")
#         return result
#     return wrapper
# @timer
# def my_func():
#     time.sleep(0.1)
# my_func()

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import asyncio
# async def call_api(url):
#     print(f"请求: {url}")
#     await asyncio.sleep(0.5)
#     return f"{url} 的响应"
# result = asyncio.run(call_api("http://localhost:8000/health"))
# print(result)

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import asyncio, time
# async def request(i):
#     await asyncio.sleep(0.1)
#     return f"结果{i}"
# async def main():
#     start = time.time()
#     results = await asyncio.gather(*[request(i) for i in range(5)])
#     print(f"结果: {results}")
#     print(f"总耗时: {time.time()-start:.2f}秒")
# asyncio.run(main())
