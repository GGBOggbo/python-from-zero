# ============================================================
# Day 21: FastAPI 中间件
# 目标：理解 CORS、日志、鉴权中间件
# 用法：python day21.py
# ============================================================

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

app = FastAPI()

# --------------------------------------------------
# 1. CORS 跨域中间件
# --------------------------------------------------
# 前端(localhost:3000)调后端(localhost:8000)会被浏览器拦截
# CORS 中间件解决跨域问题

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许哪些域名（* = 全部）
    allow_methods=["*"],        # 允许哪些方法
    allow_headers=["*"],        # 允许哪些请求头
)

# --------------------------------------------------
# 2. 请求日志中间件
# --------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    print(f"{request.method} {request.url.path} → {response.status_code} ({elapsed:.3f}s)")
    return response

# --------------------------------------------------
# 3. 简单鉴权
# --------------------------------------------------
API_KEY = "sk-your-secret-key"

async def verify_api_key(request: Request):
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="无效的API密钥")
    return True

# 需要鉴权的接口
@app.get("/protected")
async def protected(auth=Depends(verify_api_key)):
    return {"message": "验证通过，这是受保护的数据"}

# 不需要鉴权的接口
@app.get("/public")
async def public():
    return {"message": "这是公开数据"}

# --------------------------------------------------
# 4. 全局异常处理
# --------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"未处理异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "服务器内部错误", "detail": str(exc)}
    )

# --------------------------------------------------
# 5. 小练习
# --------------------------------------------------

# 练习1：添加计时中间件
# 在响应头里加入 X-Process-Time

# 练习2：添加简单 Token 鉴权
# 检查请求头中的 Authorization: Bearer xxx

# 练习3：添加请求限流
# 限制每秒最多 N 个请求（简单版）

# 练习1 参考答案
# @app.middleware("http")
# async def add_process_time(request: Request, call_next):
#     start = time.time()
#     response = await call_next(request)
#     response.headers["X-Process-Time"] = f"{time.time()-start:.3f}s"
#     return response

# 练习2 参考答案
# async def check_token(request: Request):
#     token = request.headers.get("X-Token", "")
#     if token != "my-secret":
#         raise HTTPException(401, "Token无效")
# @app.get("/secure")
# async def secure(auth=Depends(check_token)):
#     return {"data": "机密信息"}

# 练习3 参考答案
# from collections import defaultdict
# request_counts = defaultdict(list)
# @app.middleware("http")
# async def rate_limit(request: Request, call_next):
#     import time
#     now = time.time()
#     ip = request.client.host
#     request_counts[ip] = [t for t in request_counts[ip] if now - t < 1]
#     if len(request_counts[ip]) >= 10:
#         return JSONResponse(status_code=429, content={"error": "请求太频繁"})
#     request_counts[ip].append(now)
#     return await call_next(request)
