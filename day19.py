# ============================================================
# Day 19: FastAPI 请求体
# 目标：会用 Pydantic 定义请求体，处理路径参数+查询参数
# 用法：python day19.py
# ============================================================

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

app = FastAPI()

# --------------------------------------------------
# 1. Pydantic 请求体
# --------------------------------------------------
class CreateServerRequest(BaseModel):
    name: str = Field(min_length=1, description="服务器名称")
    ip: str = Field(description="IP 地址")
    port: int = Field(ge=1024, le=65535, description="端口")
    gpu_count: int = Field(default=4, ge=1, le=16)
    tags: List[str] = Field(default_factory=list)

@app.post("/servers")
def create_server(req: CreateServerRequest):
    return {"message": f"创建 {req.name} 成功", "data": req.model_dump()}

# --------------------------------------------------
# 2. 路径参数 + 请求体
# --------------------------------------------------
@app.put("/servers/{server_id}")
def update_server(server_id: int, req: CreateServerRequest):
    return {"id": server_id, "updated": req.model_dump()}

# PUT /servers/1 → server_id=1, body=请求体

# --------------------------------------------------
# 3. 查询参数验证
# --------------------------------------------------
@app.get("/servers")
def list_servers(
    status: Optional[str] = Query(None, description="按状态过滤"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
):
    return {"status": status, "page": page, "size": size, "data": []}

# GET /servers?status=running&page=2&size=20

# --------------------------------------------------
# 4. 嵌套模型
# --------------------------------------------------
class GPUConfig(BaseModel):
    index: int
    memory_gb: float

class ServerSetup(BaseModel):
    name: str
    gpus: List[GPUConfig]
    model_path: str
    auto_start: bool = True

@app.post("/servers/setup")
def setup_server(req: ServerSetup):
    return {
        "server": req.name,
        "gpu_count": len(req.gpus),
        "model": req.model_path,
        "auto_start": req.auto_start
    }

# --------------------------------------------------
# 5. 响应模型
# --------------------------------------------------
class ServerResponse(BaseModel):
    id: int
    name: str
    status: str

@app.get("/servers/{server_id}", response_model=ServerResponse)
def get_server(server_id: int = Path(ge=1)):
    return {"id": server_id, "name": f"gpu-{server_id:02d}", "status": "running"}

# --------------------------------------------------
# 6. 小练习
# --------------------------------------------------

# 练习1：定义模型部署请求体
# 包含 model_name, port, gpu_ids(List[int]), auto_reload(bool)

# 练习2：写一个带路径参数和查询参数的接口
# GET /models/{model_name}/status?verbose=true

# 练习3：定义嵌套请求体
# ChatRequest 包含 model(str), messages(List[dict]), config(子模型)

# 练习1 参考答案
# class DeployRequest(BaseModel):
#     model_name: str
#     port: int = Field(ge=1024, le=65535)
#     gpu_ids: List[int]
#     auto_reload: bool = False
# @app.post("/deploy")
# def deploy(req: DeployRequest):
#     return {"deployed": req.model_name, "gpus": req.gpu_ids}

# 练习2 参考答案
# @app.get("/models/{model_name}/status")
# def model_status(model_name: str, verbose: bool = False):
#     info = {"name": model_name, "status": "running"}
#     if verbose: info["details"] = {"gpu": 4, "uptime": "2h"}
#     return info

# 练习3 参考答案
# class ChatConfig(BaseModel):
#     temperature: float = 0.7
#     max_tokens: int = 512
# class ChatRequest(BaseModel):
#     model: str
#     messages: List[dict]
#     config: ChatConfig = ChatConfig()
