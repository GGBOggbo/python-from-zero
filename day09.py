# ============================================================
# Day 09: 异常处理 (try/except)
# 目标：让脚本遇到错误不崩溃，能优雅处理
# 用法：python day09.py
# ============================================================

# --------------------------------------------------
# 1. 为什么要处理异常？
# --------------------------------------------------
# 没有异常处理：脚本一遇到错误就整个崩溃退出
# 有了异常处理：跳过错误继续运行，或者给出友好提示

# 这行会崩溃：
# result = 10 / 0               # ZeroDivisionError

# --------------------------------------------------
# 2. 基础 try/except
# --------------------------------------------------

try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零！")

print("脚本继续运行...")        # 没有崩溃，继续往下走

# 捕获不同类型的异常
try:
    number = int("hello")
except ValueError:
    print("这不是一个有效的数字")

try:
    items = [1, 2, 3]
    print(items[10])
except IndexError:
    print("下标越界了")

try:
    info = {"name": "gpu-01"}
    print(info["port"])
except KeyError:
    print("key 不存在")

# --------------------------------------------------
# 3. 捕获多种异常
# --------------------------------------------------

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("错误: 除数不能为0")
        return None
    except TypeError:
        print("错误: 参数类型不对")
        return None

print(safe_divide(10, 3))       # 3.3333
print(safe_divide(10, 0))       # 错误提示 + None
print(safe_divide("10", 3))     # 错误提示 + None

# 一个 except 捕获多种异常
try:
    result = int("abc")
except (ValueError, TypeError) as e:
    print(f"转换失败: {e}")

# --------------------------------------------------
# 4. try/except/else/finally 完整结构
# --------------------------------------------------

def read_config(filepath):
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"配置文件不存在: {filepath}")
        return None
    except PermissionError:
        print(f"没有权限读取: {filepath}")
        return None
    else:
        # 没有异常时执行
        print(f"成功读取配置文件: {len(content)} 字节")
        return content
    finally:
        # 无论如何都会执行（清理资源、关闭连接等）
        print("读取操作完成")

# 测试
print("--- 读取存在的文件 ---")
read_config("config.json")     # 前一天创建的

print("\n--- 读取不存在的文件 ---")
read_config("not_exist.json")

# --------------------------------------------------
# 5. 获取异常信息
# --------------------------------------------------

try:
    result = 1 / 0
except Exception as e:
    print(f"异常类型: {type(e).__name__}")     # ZeroDivisionError
    print(f"异常信息: {e}")                      # division by zero

# 使用 traceback 获取完整的错误栈
import traceback

try:
    result = int("abc")
except Exception:
    print("发生错误:")
    traceback.print_exc()      # 打印完整的错误栈（调试时很有用）

# --------------------------------------------------
# 6. 主动抛出异常
# --------------------------------------------------

def check_port(port):
    if not isinstance(port, int):
        raise TypeError("端口必须是整数")
    if port < 0 or port > 65535:
        raise ValueError(f"无效端口号: {port}（范围 0-65535）")
    return True

# 测试
try:
    check_port(8000)
    print("端口 8000 有效")
    check_port(-1)
except ValueError as e:
    print(f"端口检查失败: {e}")

try:
    check_port("8000")
except TypeError as e:
    print(f"类型检查失败: {e}")

# --------------------------------------------------
# 7. 自定义异常
# --------------------------------------------------

class ServiceError(Exception):
    """服务相关异常"""
    pass

class GPUOverheatError(ServiceError):
    """GPU 过热异常"""
    def __init__(self, server, temperature):
        self.server = server
        self.temperature = temperature
        super().__init__(f"{server} GPU 过热: {temperature}°C")

class OOMError(ServiceError):
    """显存溢出异常"""
    pass

def monitor_gpu(server, temp, memory_used, memory_total):
    """监控 GPU，异常时抛出自定义异常"""
    if temp > 85:
        raise GPUOverheatError(server, temp)
    if memory_used > memory_total * 0.95:
        raise OOMError(f"{server} 显存不足: {memory_used}/{memory_total} GB")
    return f"{server} 正常: {temp}°C, 显存 {memory_used}/{memory_total} GB"

# 测试
test_cases = [
    ("gpu-01", 72, 40, 80),
    ("gpu-02", 92, 45, 80),
    ("gpu-03", 70, 78, 80),
]

for server, temp, used, total in test_cases:
    try:
        result = monitor_gpu(server, temp, used, total)
        print(result)
    except GPUOverheatError as e:
        print(f"[过热告警] {e}")
    except OOMError as e:
        print(f"[显存告警] {e}")

# --------------------------------------------------
# 8. 实战：健壮的配置文件读取
# --------------------------------------------------

import json

def load_config(filepath, default=None):
    """
    安全读取 JSON 配置文件
    - 文件不存在 → 返回默认值
    - JSON 格式错误 → 返回默认值
    - 读取成功 → 返回配置内容
    """
    if default is None:
        default = {}

    try:
        with open(filepath, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"配置文件不存在: {filepath}，使用默认配置")
        return default
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误: {filepath}")
        print(f"  错误详情: {e}")
        return default
    except Exception as e:
        print(f"读取配置失败: {e}")
        return default

    # 验证必要字段
    required_fields = ["model", "port"]
    for field in required_fields:
        if field not in config:
            print(f"警告: 配置缺少必要字段 '{field}'")

    return config

# 测试
print("\n=== 配置文件读取测试 ===")
config = load_config("config.json")
print(f"模型: {config.get('model', '未知')}")

config2 = load_config("not_exist.json", {"model": "default", "port": 8080})
print(f"默认配置: {config2}")

# --------------------------------------------------
# 9. 常见异常速查
# --------------------------------------------------

common_errors = {
    "ValueError":       "值不对（比如 int('abc')）",
    "TypeError":        "类型不对（比如 '2' + 2）",
    "KeyError":         "字典的 key 不存在",
    "IndexError":       "列表下标越界",
    "FileNotFoundError":"文件不存在",
    "PermissionError":  "没有权限",
    "ZeroDivisionError":"除以零",
    "AttributeError":   "对象没有这个属性/方法",
    "ImportError":      "导入模块失败",
    "json.JSONDecodeError": "JSON 格式错误",
}

print("\=== 常见异常速查 ===")
for name, desc in common_errors.items():
    print(f"  {name:<25} {desc}")

# --------------------------------------------------
# 10. 练习
# --------------------------------------------------

# 练习1：写一个安全的数字输入函数
# safe_int(value, default=0)
# 能转就转，不能转返回默认值
# safe_int("42") → 42
# safe_int("abc") → 0
# safe_int("abc", default=-1) → -1

# ====== 在这里写你的代码 ======



# 练习2：写一个函数，安全获取嵌套字典的值
# safe_get(data, keys, default=None)
# data = {"a": {"b": {"c": 42}}}
# safe_get(data, ["a", "b", "c"]) → 42
# safe_get(data, ["a", "x", "y"]) → None（不报错）
# safe_get(data, ["a", "x", "y"], default=0) → 0

# ====== 在这里写你的代码 ======



# 练习3（挑战）：写一个健壮的日志读取器
# 函数名: safe_read_logs(filepath)
# 要求:
# - 文件不存在 → 返回空列表 + print 提示
# - 每行解析失败 → 跳过该行 + print 警告
# - 成功 → 返回解析后的字典列表

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# def safe_int(value, default=0):
#     try:
#         return int(value)
#     except (ValueError, TypeError):
#         return default
# print(safe_int("42"))
# print(safe_int("abc"))
# print(safe_int("abc", default=-1))

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# def safe_get(data, keys, default=None):
#     try:
#         result = data
#         for key in keys:
#             result = result[key]
#         return result
#     except (KeyError, TypeError, IndexError):
#         return default
# data = {"a": {"b": {"c": 42}}}
# print(safe_get(data, ["a", "b", "c"]))
# print(safe_get(data, ["a", "x", "y"]))

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# def safe_read_logs(filepath):
#     result = []
#     try:
#         with open(filepath, "r") as f:
#             for i, line in enumerate(f, 1):
#                 try:
#                     parts = line.strip().split()
#                     if len(parts) >= 3:
#                         result.append({"time": parts[1], "level": parts[2], "msg": " ".join(parts[3:])})
#                 except Exception:
#                     print(f"警告: 第 {i} 行解析失败，已跳过")
#     except FileNotFoundError:
#         print(f"日志文件不存在: {filepath}")
#     return result
