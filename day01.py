# ============================================================
# Day 01: 变量、数据类型、print
# 目标：能读懂这整个文件，能自己写类似的代码
# 用法：python day01.py 逐段运行，改一改，看看结果变不变
# ============================================================

# --------------------------------------------------
# 1. print —— 让程序"说话"
# --------------------------------------------------
# 代码不会自己说话，print 就是让它在屏幕上输出东西

print("hello world")  # 最经典的入门，每个程序员都写过这一行
print(42)             # 也能输出数字
print()               # 空的 print 输出一个空行，用来分隔内容

# --------------------------------------------------
# 2. 变量 —— 给数据起个名字
# --------------------------------------------------
# 变量就像一个盒子，你往里面放东西，以后用名字就能找到它
# Python 里不用声明类型，直接赋值就行

server_name = "gpu-01"        # 给变量 server_name 赋一个字符串
gpu_count = 8                 # 给变量 gpu_count 赋一个整数
gpu_memory_gb = 80.0          # 给变量赋一个浮点数（小数）
is_running = True             # 给变量赋一个布尔值（True/False）

print(server_name)            # 输出: gpu-01
print(gpu_count)              # 输出: 8
print(gpu_memory_gb)          # 输出: 80.0
print(is_running)             # 输出: True

# 变量可以重新赋值，新的值会覆盖旧的
server_name = "gpu-02"
print(server_name)            # 输出: gpu-02（变了！）

# --------------------------------------------------
# 3. 四种基本数据类型
# --------------------------------------------------

# 📝 字符串 str —— 用引号包起来的文字
host = "10.0.0.1"
log_level = "ERROR"
empty_string = ""              # 空字符串也合法

# 🔢 整数 int —— 没有小数点的数
port = 8000
timeout_seconds = 30
error_count = 0

# 🔢 浮点数 float —— 有小数点的数
cpu_usage = 87.5               # CPU 使用率 87.5%
model_size_gb = 14.3           # 模型大小 14.3 GB
response_time = 2.34           # 响应时间 2.34 秒

# ✅ 布尔值 bool —— 只有 True 或 False 两种
service_ok = True
gpu_overheating = False

# type() 函数能查看任意变量的类型
print(type(host))              # <class 'str'>
print(type(port))              # <class 'int'>
print(type(cpu_usage))         # <class 'float'>
print(type(service_ok))        # <class 'bool'>

# --------------------------------------------------
# 4. f-string —— 最常用的输出方式（重点！）
# --------------------------------------------------
# 在字符串前加 f，用 {} 包住变量名，就能把变量嵌入字符串

model = "qwen-72b"
status = "running"
gpu = 4

# 老办法（不推荐，但你会看到别人这么写）
print("模型 " + model + " 状态 " + status)

# f-string（推荐！简洁清晰）
print(f"模型 {model} 状态 {status}")
print(f"使用了 {gpu} 张显卡")
print(f"模型名: {model}, 端口: {port}")

# {} 里还能写简单的表达式
print(f"总显存: {gpu * 80} GB")
print(f"服务{'正常' if service_ok else '异常'}")

# --------------------------------------------------
# 5. 数据类型转换
# --------------------------------------------------
# 用户输入或从文件读到的数据，通常是字符串，需要转换

# 字符串 → 整数
port_str = "8080"
port_int = int(port_str)
print(type(port_str), type(port_int))   # str → int

# 整数 → 字符串
num = 8000
text = str(num)
print(f"端口是 {text}，类型是 {type(text)}")

# 字符串 → 浮点数
usage_str = "92.3"
usage_float = float(usage_str)
print(f"CPU使用率: {usage_float}%")

# 转换失败会报错（这个你可以试试取消注释运行看报错）
# int("hello")        # ValueError
# int("80.5")         # ValueError（不能直接转带小数的字符串）
# float("hello")      # ValueError

# --------------------------------------------------
# 6. 命名规范 —— 变量怎么起名
# --------------------------------------------------

# ✅ 推荐写法（蛇形命名法 snake_case）
server_name = "gpu-01"
gpu_count = 8
is_healthy = True

# ❌ 不推荐（但不会报错）
ServerName = "gpu-01"     # 这是类名的风格，别用在变量上
x = "gpu-01"              # 名字没意义，过两天你就忘了它存的是啥

# ❌ 语法错误（这些名字不能用）
# 1server = "gpu"          # 不能数字开头
# my-server = "gpu"        # 不能用横杠（Python 会当成减法）
# class = "gpu"            # 不能用 Python 关键字（if/for/class/while 等）

# --------------------------------------------------
# 7. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：定义变量描述你管理的模型服务，然后 print 出来
# 要求：模型名、版本号、端口号、GPU数量、是否在线
# 输出格式类似：
#   模型服务 qwen-72b v2.1 运行在端口 8000，使用 4 张 GPU，状态: 在线

# ====== 在这里写你的代码 ======




# 练习2：模拟一个简单的状态检查输出
# 定义一个变量 gpu_temperature = 78
# 如果温度 >= 80，输出"告警：温度过高！"
# 否则输出"温度正常"
# 提示：用 if/else（明天会正式学，今天试着自己查或问AI）

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# model_name = "qwen-72b"
# version = "v2.1"
# port = 8000
# gpu_num = 4
# online = True
# print(f"模型服务 {model_name} {version} 运行在端口 {port}，使用 {gpu_num} 张 GPU，状态: {'在线' if online else '离线'}")

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# gpu_temperature = 78
# if gpu_temperature >= 80:
#     print(f"告警：GPU温度 {gpu_temperature}°C，温度过高！")
# else:
#     print(f"GPU温度 {gpu_temperature}°C，温度正常")
