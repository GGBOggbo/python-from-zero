# ============================================================
# Day 5: JSON 处理
# 目标：能读写 JSON 文件，解析 API 返回的嵌套 JSON
# 用法：python day05.py 逐段运行，改一改，看看结果变不变
# ============================================================

import json

# --------------------------------------------------
# 1. JSON 是什么
# --------------------------------------------------
# JSON = JavaScript Object Notation
# 互联网上最通用的数据格式
# API 返回的数据、配置文件，基本都是 JSON

data = {"name": "gpu-01", "gpu": 4, "online": True}
json_str = json.dumps(data)
print(f"Python → JSON: {json_str}")

# --------------------------------------------------
# 2. json.loads — JSON 字符串转 Python
# --------------------------------------------------
api_response = '{"model": "qwen-72b", "status": "running", "port": 8000}'
result = json.loads(api_response)
print(f"\n模型: {result['model']}, 端口: {result['port']}")

# 类型映射：
# JSON {} → dict, [] → list, true/false → True/False, null → None

# --------------------------------------------------
# 3. json.dumps — Python 转 JSON 字符串
# --------------------------------------------------
config = {
    "server": "gpu-01",
    "port": 8000,
    "models": ["qwen-72b", "llama-70b"],
    "gpu_count": 4,
}

# 好看的格式（调试必用）
print(json.dumps(config, indent=2, ensure_ascii=False))

# ensure_ascii=False 让中文正常显示
print(json.dumps({"服务": "模型推理"}, ensure_ascii=False))

# --------------------------------------------------
# 4. 读写 JSON 文件
# --------------------------------------------------
# json.dump() → 写入文件（没有 s）
# json.load() → 从文件读取（没有 s）

# 写入
with open("test_config.json", "w") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print("\n已写入 test_config.json")

# 读取
with open("test_config.json", "r") as f:
    loaded = json.load(f)
print(f"读取: {loaded}")

import os
os.remove("test_config.json")

# --------------------------------------------------
# 5. 嵌套 JSON 解析
# --------------------------------------------------
api_result = {
    "status": "success",
    "data": {
        "models": [
            {"id": "qwen-72b", "status": "loaded"},
            {"id": "llama-70b", "status": "loading"},
        ],
        "gpu_info": {"total": 8, "used": 6}
    },
    "usage": {"prompt_tokens": 100, "completion_tokens": 50}
}

# 逐层取值
print(f"\n模型数: {len(api_result['data']['models'])}")
print(f"第一个模型: {api_result['data']['models'][0]['id']}")
print(f"GPU: {api_result['data']['gpu_info']['used']}/{api_result['data']['gpu_info']['total']}")

# 安全取值（避免 KeyError）
print(f"版本: {api_result.get('version', '未知')}")

# --------------------------------------------------
# 6. 实际场景：解析 API 响应
# --------------------------------------------------
chat_response = {
    "model": "qwen-72b",
    "choices": [{"message": {"content": "GPU温度过高建议检查散热"}}],
    "usage": {"prompt_tokens": 15, "completion_tokens": 12, "total_tokens": 27}
}

answer = chat_response["choices"][0]["message"]["content"]
tokens = chat_response["usage"]["total_tokens"]
print(f"\n回复: {answer}")
print(f"Token用量: {tokens}")

# --------------------------------------------------
# 7. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：解析模型列表 JSON
# json_str = '{"data": [{"id": "qwen"}, {"id": "llama"}, {"id": "deepseek"}]}'
# 打印所有模型 ID

# ====== 在这里写你的代码 ======




# 练习2：读写配置文件
# 创建字典 → 写入 JSON 文件 → 读回来打印

# ====== 在这里写你的代码 ======




# 练习3：解析嵌套监控数据
# monitor_data = {"servers": [{"name": "gpu-01", "gpus": [{"id": 0, "temp": 72}, {"id": 1, "temp": 85}]}]}
# 找出最高温度

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import json
# json_str = '{"data": [{"id": "qwen"}, {"id": "llama"}, {"id": "deepseek"}]}'
# for model in json.loads(json_str)["data"]:
#     print(f"模型: {model['id']}")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# import json
# config = {"host": "gpu-01", "port": 8000, "models": ["qwen"]}
# with open("my_config.json", "w") as f:
#     json.dump(config, f, indent=2, ensure_ascii=False)
# with open("my_config.json", "r") as f:
#     print(json.load(f))

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# monitor_data = {"servers": [{"name": "gpu-01", "gpus": [{"id": 0, "temp": 72}, {"id": 1, "temp": 85}]}]}
# max_temp = 0
# for server in monitor_data["servers"]:
#     for gpu in server["gpus"]:
#         if gpu["temp"] > max_temp:
#             max_temp = gpu["temp"]
#             print(f"最高: {server['name']}-GPU#{gpu['id']} = {gpu['temp']}°C")
