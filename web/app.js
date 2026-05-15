// ====== Theme ======
function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  html.setAttribute('data-theme', next);
  localStorage.setItem('py_theme', next);
  document.getElementById('themeIcon').textContent = next === 'light' ? '☀️' : '🌙';

  // Switch highlight.js theme
  const lightSheet = document.getElementById('hljs-light');
  const darkSheet = document.getElementById('hljs-dark');
  if (next === 'dark') {
    lightSheet.disabled = true;
    darkSheet.disabled = false;
  } else {
    lightSheet.disabled = false;
    darkSheet.disabled = true;
  }

  // Switch CodeMirror theme
  const isDark = next === 'dark';
  const cmDark = document.getElementById('cm-dark');
  if (cmDark) cmDark.disabled = !isDark;

  // Re-highlight
  document.querySelectorAll('pre code').forEach(el => {
    el.removeAttribute('data-highlighted');
    hljs.highlightElement(el);
  });
}

// Restore theme
(function() {
  const saved = localStorage.getItem('py_theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
    document.getElementById('themeIcon').textContent = saved === 'light' ? '☀️' : '🌙';
    if (saved === 'dark') {
      document.getElementById('hljs-light').disabled = true;
      document.getElementById('hljs-dark').disabled = false;
    }
  }
})();

// ====== Course Data ======
const courses = [
  {
    id: 1, title: "变量、数据类型、print", icon: "D1",
    tag: "基础", tagClass: "green",
    desc: "能读懂别人写的脚本，能自己写100行以内的小程序",
    sections: [
      {
        title: "print — 让程序说话",
        content: `<div class="text-block">代码不会自己说话，<code>print()</code> 就是让它在屏幕上输出东西。括号里放什么，就输出什么。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">print("hello world")  # 最经典的入门
print(42)             # 也能输出数字
print()               # 输出一个空行</code></pre></div>`
      },
      {
        title: "变量 — 给数据起个名字",
        content: `<div class="text-block">变量就像一个盒子，你往里面放东西，以后用名字就能找到它。Python 里不用声明类型，直接赋值就行。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">server_name = "gpu-01"        # 字符串 str
gpu_count = 8                 # 整数 int
gpu_memory_gb = 80.0          # 浮点数 float
is_running = True             # 布尔值 bool

print(server_name)            # 输出: gpu-01
print(type(server_name))      # 输出: &lt;class 'str'></code></pre></div>
<div class="tip-box info"><p><strong>type()</strong> 函数能查看任意变量的类型，调试时很有用。</p></div>`
      },
      {
        title: "四种基本数据类型",
        content: `<div class="table-wrap"><table><tr><th>类型</th><th>写法</th><th>例子</th><th>说明</th></tr>
<tr><td><code>str</code></td><td>引号包起来</td><td><code>"gpu-01"</code></td><td>文字/字符串</td></tr>
<tr><td><code>int</code></td><td>没有小数点</td><td><code>8000</code></td><td>整数</td></tr>
<tr><td><code>float</code></td><td>有小数点</td><td><code>87.5</code></td><td>小数</td></tr>
<tr><td><code>bool</code></td><td>True/False</td><td><code>True</code></td><td>布尔值，只有两种</td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 字符串
host = "10.0.0.1"
log_level = "ERROR"

# 整数
port = 8000
timeout_seconds = 30

# 浮点数
cpu_usage = 87.5
response_time = 2.34

# 布尔值
service_ok = True
gpu_overheating = False

print(type(host))        # &lt;class 'str'>
print(type(port))        # &lt;class 'int'>
print(type(cpu_usage))   # &lt;class 'float'>
print(type(service_ok))  # &lt;class 'bool'></code></pre></div>`
      },
      {
        title: "f-string — 最常用的输出方式",
        content: `<div class="text-block">在字符串前加 <code>f</code>，用 <code>{}</code> 包住变量名，就能把变量嵌入字符串。这是<strong>必须掌握</strong>的技能。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">model = "qwen-72b"
status = "running"
gpu = 4

# 老办法（不推荐）
print("模型 " + model + " 状态 " + status)

# f-string（推荐！简洁清晰）
print(f"模型 {model} 状态 {status}")
print(f"使用了 {gpu} 张显卡")
print(f"模型名: {model}, 端口: {port}")

# {} 里还能写简单的表达式
print(f"总显存: {gpu * 80} GB")
print(f"服务{'正常' if service_ok else '异常'}")</code></pre></div>`
      },
      {
        title: "数据类型转换",
        content: `<div class="text-block">从文件读到的数据通常是字符串，需要转换才能用。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 字符串 → 整数
port_str = "8080"
port_int = int(port_str)
print(type(port_str), type(port_int))   # str → int

# 整数 → 字符串
num = 8000
text = str(num)

# 字符串 → 浮点数
usage_str = "92.3"
usage_float = float(usage_str)
print(f"CPU使用率: {usage_float}%")

# 转换失败会报错
# int("hello")     # ValueError
# int("80.5")      # ValueError（不能直接转带小数）</code></pre></div>`
      },
      {
        title: "命名规范 — 变量怎么起名",
        content: `<div class="text-block">好的变量名让代码自解释，过两个月回来看也能立刻理解。Python 用<strong>蛇形命名法</strong>（snake_case）。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># ✅ 推荐写法（蛇形命名法 snake_case）
server_name = "gpu-01"
gpu_count = 8
is_healthy = True

# ❌ 不推荐（但不会报错）
ServerName = "gpu-01"     # 这是类名的风格，别用在变量上
x = "gpu-01"              # 名字没意义，过两天就忘了它存的是啥

# ❌ 语法错误（这些名字不能用）
# 1server = "gpu"          # 不能数字开头
# my-server = "gpu"        # 不能用横杠（Python 会当成减法）
# class = "gpu"            # 不能用 Python 关键字</code></pre></div>
<div class="tip-box success"><p><strong>原则：</strong>变量名要有意义，用小写字母+下划线，如 <code>gpu_count</code>、<code>is_running</code>。</p></div>`
      }
    ],
    exercises: [
      { title: "定义变量描述一个模型服务", desc: `要求：模型名、版本号、端口号、GPU数量、是否在线<br>输出格式类似：<br>模型服务 qwen-72b v2.1 运行在端口 8000，使用 4 张 GPU，状态: 在线`, answer: `model_name = "qwen-72b"
version = "v2.1"
port = 8000
gpu_num = 4
online = True
print(f"模型服务 {model_name} {version} 运行在端口 {port}，使用 {gpu_num} 张 GPU，状态: {'在线' if online else '离线'}")` },
      { title: "模拟 GPU 温度检查", desc: `定义一个变量 gpu_temperature = 78<br>如果温度 >= 80，输出"告警：温度过高！"<br>否则输出"温度正常"<br>提示：用 if/else（明天会正式学，今天试着自己查或问AI）`, answer: `gpu_temperature = 78
if gpu_temperature >= 80:
    print(f"告警：GPU温度 {gpu_temperature}°C，温度过高！")
else:
    print(f"GPU温度 {gpu_temperature}°C，温度正常")`
      }
    ]
  },
  {
    id: 2, title: "字符串操作", icon: "D2",
    tag: "基础", tagClass: "green",
    desc: "能处理日志文本，提取你需要的信息",
    sections: [
      {
        title: "字符串基础：引号",
        content: `<div class="text-block">Python 里单引号和双引号没区别，选一个用就行。字符串里有引号时，外面用另一种。三引号用于多行文本。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">host1 = 'gpu-01'
host2 = "gpu-02"

# 字符串里本身有引号时，外面用另一种
msg = "服务 'gpu-01' 已启动"       # 外面双引号，里面单引号
msg2 = '他说"部署完成"'            # 外面单引号，里面双引号

# 三引号：多行文本
config_text = """
[model]
name=qwen-72b
port=8000
gpu=4
"""
print(config_text)</code></pre></div>` },
      {
        title: "索引和切片 — 取字符串的一部分",
        content: `<div class="text-block">和列表一样，字符串用索引取字符、用切片取子串。索引从 0 开始，<code>[起:止]</code> 取起到止之前。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">#        索引:  0 1 2 3 4 5 6 7 8 9
log = "ERROR: GPU-01 OOM"

# 取单个字符（从0开始数）
print(log[0])              # E（第1个字符）
print(log[7])              # G（第8个字符）

# 负数索引：从末尾往前数
print(log[-1])             # M（最后1个字符）
print(log[-4])             # 1（倒数第4个）

# 切片：[起:止] 取起到止之前（不包含止那个位置）
print(log[0:5])            # ERROR
print(log[7:13])           # GPU-01
print(log[:5])             # ERROR（省略起=从头开始）
print(log[7:])             # GPU-01 OOM（省略止=取到末尾）</code></pre></div>`
      },
      {
        title: "常用方法（最实用的几个）",
        content: `<div class="table-wrap"><table><tr><th>类别</th><th>方法</th><th>作用</th><th>例子</th></tr>
<tr><td>去空白</td><td><code>strip()</code></td><td>去首尾空白</td><td><code>" hi ".strip()</code> → <code>"hi"</code></td></tr>
<tr><td>去空白</td><td><code>lstrip()/rstrip()</code></td><td>只去左边/右边</td><td>同上</td></tr>
<tr><td>大小写</td><td><code>upper()/lower()</code></td><td>全大/小写</td><td><code>"abc".upper()</code> → <code>"ABC"</code></td></tr>
<tr><td>查找</td><td><code>find()</code></td><td>找位置</td><td><code>"abc".find("b")</code> → <code>1</code></td></tr>
<tr><td>查找</td><td><code>in</code></td><td>是否包含</td><td><code>"gpu" in log</code> → <code>True</code></td></tr>
<tr><td>查找</td><td><code>startswith()/endswith()</code></td><td>前缀/后缀</td><td><code>log.startswith("ERROR")</code></td></tr>
<tr><td>替换</td><td><code>replace()</code></td><td>替换文字</td><td><code>"a b".replace(" ", "")</code></td></tr>
<tr><td>计数</td><td><code>count()</code></td><td>出现几次</td><td><code>"hello".count("l")</code> → <code>2</code></td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">log_line = "  ERROR: gpu-01 out of memory  "
print(log_line.strip())           # 去掉首尾空白

print(log_line.upper())           # 全变大写
print(log_line.lower())           # 全变小写

log_clean = "ERROR: gpu-01 out of memory"
print(log_clean.find("gpu"))      # 找位置 → 7
print(log_clean.find("xxx"))      # 找不到 → -1
print("gpu" in log_clean)         # 是否包含 → True
print(log_clean.startswith("ERROR"))  # 是否以ERROR开头 → True</code></pre></div>`
      },
      {
        title: "split 和 join（超高频！）",
        content: `<div class="text-block"><strong>split</strong> 把字符串拆成列表，<strong>join</strong> 把列表拼成字符串。处理日志、CSV 全靠它们。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># split：按分隔符拆成列表
log_entry = "2024-01-15 10:30:00 ERROR gpu-01 out of memory"
parts = log_entry.split(" ")
print(parts)
# → ['2024-01-15', '10:30:00', 'ERROR', 'gpu-01', 'out', 'of', 'memory']

date = parts[0]        # 2024-01-15
level = parts[2]       # ERROR

# 指定拆分次数
csv_line = "qwen-72b,8000,running,4,80.5"
result = csv_line.split(",", 2)   # 只拆2次
print(result)  # → ['qwen-72b', '8000', 'running,4,80.5']

# join：把列表合并成字符串（split 的反操作）
servers = ["gpu-01", "gpu-02", "gpu-03"]
print(",".join(servers))         # gpu-01,gpu-02,gpu-03
print(" -> ".join(servers))      # gpu-01 -> gpu-02 -> gpu-03</code></pre></div>
<div class="tip-box success"><p>口诀：<strong>拼接用 f-string 和 join，删改都靠 replace，查找 find/in/split 三件套</strong></p></div>`
      },
      {
        title: "f-string 进阶技巧",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">gpu_temp = 87.3456
request_count = 1024
ratio = 0.8567

# 控制小数位数
print(f"温度: {gpu_temp:.1f}°C")          # 保留1位 → 87.3°C
print(f"温度: {gpu_temp:.2f}°C")          # 保留2位 → 87.35°C

# 格式化数字（千位分隔符、补零）
print(f"请求数: {request_count:,}")        # 1,024
print(f"编号: {42:04d}")                   # 0042（补零到4位）

# 百分比
print(f"成功率: {ratio:.1%}")              # 85.7%

# 对齐（生成表格输出时有用）
print(f"{'服务器':<10} {'状态':^8} {'GPU':>4}")
print(f"{'gpu-01':<10} {'running':^8} {4:>4}")
print(f"{'gpu-02':<10} {'stopped':^8} {0:>4}")
# <10 左对齐宽10   ^8 居中宽8   >4 右对齐宽4</code></pre></div>`
      },
      {
        title: "字符串不可变",
        content: `<div class="text-block">字符串是<strong>不可变</strong>的——每次操作都返回新字符串，不能直接改某个字符。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">name = "gpu-01"
# name[0] = "G"   # 这行会报错！字符串不能直接改某个字符

# 要"改"只能生成新的
name = "G" + name[1:]
print(name)        # Gpu-01（新字符串）</code></pre></div>
<div class="tip-box info"><p><strong>记住：</strong>字符串、数字都是不可变类型。列表、字典是可变类型。</p></div>`
      },
      {
        title: "实战：从日志中提取关键信息",
        content: `<div class="text-block">学以致用——用上面学的字符串操作来分析模型服务日志。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">logs = """
[2024-01-15 10:23:01] INFO  Service started on port 8000
[2024-01-15 10:23:15] INFO  Model qwen-72b loaded, GPU: 4
[2024-01-15 10:25:30] WARN  Request timeout, client=192.168.1.100
[2024-01-15 10:26:02] ERROR GPU-01 OOM, used=79.2GB/80GB
[2024-01-15 10:26:05] WARN  Auto restart triggered
[2024-01-15 10:26:30] INFO  Service recovered
[2024-01-15 10:30:00] ERROR GPU-02 OOM, used=78.8GB/80GB
"""

print("=== 日志分析 ===")
lines = logs.strip().split("\n")
print(f"总日志行数: {len(lines)}")

# 统计各级别
error_count = 0
warn_count = 0
info_count = 0
error_lines = []

for line in lines:
    if "ERROR" in line:
        error_count += 1
        error_lines.append(line)
    elif "WARN" in line:
        warn_count += 1
    elif "INFO" in line:
        info_count += 1

print(f"ERROR: {error_count} 次")
print(f"WARN:  {warn_count} 次")
print(f"INFO:  {info_count} 次")

# 提取 ERROR 行的详情
print("\n=== ERROR 详情 ===")
for line in error_lines:
    time_str = line.split("]")[0].replace("[", "")
    parts = line.split()
    for part in parts:
        if part.startswith("GPU-"):
            server = part.replace(",", "")
    print(f"时间: {time_str}, 服务器: {server}")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "解析配置字符串", desc: "从 model=qwen-72b;port=8000;gpu=4 中提取模型名和端口号。", answer: `config_str = "model=qwen-72b;port=8000;gpu=4"
items = config_str.split(";")
model = items[0].split("=")[1]    # qwen-72b
port = items[1].split("=")[1]     # 8000
print(f"模型名: {model}, 端口: {port}")` ,
        starter: `config_str = "model=qwen-72b;port=8000;gpu=4"`
      },
      { title: "列表和字符串互转", desc: "把服务器列表用 join 拼成字符串，再用 split 拆回来。", answer: `server_list = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
joined = ",".join(server_list)
print(f"合并后: {joined}")
back = joined.split(",")
print(f"拆回来: {back}")
print(f"类型: {type(back)}")` ,
        starter: `server_list = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]`
      },
      { title: "解析 URL（挑战）", desc: "从 http://gpu-cluster:8080/api/v1/models 提取协议、域名、端口、路径。", answer: `url = "http://gpu-cluster.internal:8080/api/v1/models"
protocol = url.split("://")[0]                          # http
rest = url.split("://")[1]                              # gpu-cluster.internal:8080/api/v1/models
domain_port = rest.split("/")[0]                         # gpu-cluster.internal:8080
path = "/" + "/".join(rest.split("/")[1:])              # /api/v1/models
domain = domain_port.split(":")[0]                       # gpu-cluster.internal
port = domain_port.split(":")[1]                         # 8080
print(f"协议: {protocol}")
print(f"域名: {domain}")
print(f"端口: {port}")
print(f"路径: {path}")`
      ,
        starter: `url = "http://gpu-cluster.internal:8080/api/v1/models"`
      }
    ]
  },
  {
    id: 3, title: "列表 (list)", icon: "D3",
    tag: "基础", tagClass: "green",
    desc: "能管理一组服务器、一批日志、一组配置",
    sections: [
            {
        title: "创建列表",
        content: `<div class="text-block">列表用方括号 <code>[]</code>，元素用逗号隔开。一个列表里可以放不同类型（但不推荐）。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">servers = ["gpu-01", "gpu-02", "gpu-03"]
ports = [8000, 8080, 9000]
mixed = ["gpu-01", 8000, True, 87.5]   # 可以放不同类型（但不推荐）

# 空列表
empty1 = []
empty2 = list()

print(servers)
print(type(servers))           # &lt;class 'list'></code></pre></div>` },
      {
        title: "索引和切片（和字符串一模一样的规则）",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">#         0       1       2       3       4
gpus = ["gpu-01", "gpu-02", "gpu-03", "gpu-04", "gpu-05"]

# 取单个元素
print(gpus[0])              # gpu-01（第一个）
print(gpus[2])              # gpu-03（第三个）
print(gpus[-1])             # gpu-05（最后一个）
print(gpus[-2])             # gpu-04（倒数第二个）

# 切片 [起:止] —— 和字符串完全一样
print(gpus[1:3])            # ['gpu-02', 'gpu-03']
print(gpus[:3])             # ['gpu-01', 'gpu-02', 'gpu-03']（前3个）
print(gpus[2:])             # ['gpu-03', 'gpu-04', 'gpu-05']（第3个往后）
print(gpus[-3:])            # ['gpu-03', 'gpu-04', 'gpu-05']（最后3个）

# 步长 [起:止:步长]
print(gpus[::2])            # ['gpu-01', 'gpu-03', 'gpu-05']（隔一个取一个）
print(gpus[::-1])           # ['gpu-05', 'gpu-04', ...]（反序）</code></pre></div>`
      },
      {
        title: "增 — 往列表里加东西",
        content: `<div class="table-wrap"><table><tr><th>方法</th><th>作用</th><th>例子</th></tr>
<tr><td><code>append()</code></td><td>末尾加一个</td><td><code>servers.append("gpu-04")</code></td></tr>
<tr><td><code>insert(i, x)</code></td><td>指定位置插入</td><td><code>servers.insert(1, "cpu-01")</code></td></tr>
<tr><td><code>extend()</code></td><td>批量合并</td><td><code>servers.extend(["gpu-05", "gpu-06"])</code></td></tr>
<tr><td><code>+</code></td><td>合并生成新列表</td><td><code>new = servers + ["gpu-07"]</code></td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">servers = ["gpu-01", "gpu-02", "gpu-03"]

servers.append("gpu-04")          # 末尾加一个
servers.insert(1, "cpu-01")       # 在第2个位置插入
servers.extend(["gpu-05", "gpu-06"])  # 批量加
new_servers = servers + ["gpu-07", "gpu-08"]  # + 号合并（生成新列表）</code></pre></div>`
      },
      {
        title: "删 — 从列表里去掉东西",
        content: `<div class="table-wrap"><table><tr><th>方法</th><th>作用</th><th>说明</th></tr>
<tr><td><code>remove(x)</code></td><td>按值删</td><td>删第一个匹配的</td></tr>
<tr><td><code>pop(i)</code></td><td>按位置删，返回被删值</td><td>不填位置 = 删最后一个</td></tr>
<tr><td><code>del list[i]</code></td><td>按位置删</td><td>不需要返回值时用</td></tr>
<tr><td><code>clear()</code></td><td>清空整个列表</td><td></td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">servers = ["gpu-01", "cpu-01", "gpu-02", "gpu-03", "gpu-04"]

servers.remove("cpu-01")          # 按值删
removed = servers.pop()           # 删最后一个，返回被删的值
removed2 = servers.pop(0)         # 删第一个
del servers[0]                    # 按位置删

backup = servers.copy()
servers.clear()                   # 清空
print(f"清空后: {servers}")       # []
print(f"备份: {backup}")          # 还有数据</code></pre></div>`
      },
            {
        title: "改 — 直接赋值",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">servers = ["gpu-01", "gpu-02", "gpu-03"]

# 按下标改
servers[0] = "gpu-new-01"
print(servers)              # ["gpu-new-01", "gpu-02", "gpu-03"]

# 切片赋值（批量改）
servers[1:3] = ["gpu-new-02", "gpu-new-03", "gpu-new-04"]
print(servers)              # 2个位置塞了3个元素，列表会变长</code></pre></div>`
      },
      {
        title: "查 — 查找和统计",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">servers = ["gpu-01", "gpu-02", "gpu-03", "gpu-01"]

print(len(servers))                 # 4（总长度）
print("gpu-01" in servers)          # True（是否包含）
print("cpu-01" in servers)          # False
print(servers.index("gpu-02"))      # 1（所在位置）
print(servers.count("gpu-01"))      # 2（出现几次）

# index 找不存在的会报错
# servers.index("xxx")             # ValueError!

# 安全的写法：先 in 判断，再 index
target = "cpu-01"
if target in servers:
    print(f"{target} 在位置 {servers.index(target)}")
else:
    print(f"{target} 不在列表中")</code></pre></div>
<div class="tip-box danger"><p><strong>注意：</strong><code>index()</code> 找不存在的值会报 ValueError，先用 <code>in</code> 检查。</p></div>`
      },
      {
        title: "排序和反转",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">nums = [3, 1, 4, 1, 5, 9, 2, 6]
names = ["gpu-03", "gpu-01", "gpu-10", "gpu-02"]

# sort: 原地排序（改的是自己）
nums.sort()
print(nums)                  # [1, 1, 2, 3, 4, 5, 6, 9]
nums.sort(reverse=True)
print(nums)                  # [9, 6, 5, 4, 3, 2, 1, 1]
names.sort()
print(names)                 # 字符串按字母排

# sorted: 排序但返回新列表，不改原来的
original = [3, 1, 4]
sorted_copy = sorted(original)
print(f"原列表: {original}")       # [3, 1, 4]（没变）
print(f"排序后: {sorted_copy}")    # [1, 3, 4]

# reverse: 反转
nums = [1, 2, 3, 4, 5]
nums.reverse()
print(nums)                  # [5, 4, 3, 2, 1]</code></pre></div>
<div class="tip-box info"><p><strong>sort()</strong> 改原列表，<strong>sorted()</strong> 返回新列表。按需选择。</p></div>`
      },
      {
        title: "列表推导式",
        content: `<div class="text-block">把一个列表变成另一个列表的快捷写法——一行搞定 for + append。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 普通写法
servers = ["01", "02", "03"]
result = []
for s in servers:
    result.append("gpu-" + s)

# 推导式：一行搞定
result2 = ["gpu-" + s for s in servers]

# 带条件过滤
ports = [8000, 8001, 8080, 8081, 9000]
even_ports = [p for p in ports if p % 2 == 0]  # [8000, 8080, 9000]</code></pre></div>`
      },
            {
        title: "常用技巧",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># enumerate: 同时拿到索引和值
servers = ["gpu-01", "gpu-02", "gpu-03"]
for i, name in enumerate(servers):
    print(f"第 {i} 台: {name}")

# zip: 两个列表配对
servers = ["gpu-01", "gpu-02", "gpu-03"]
temps = [72, 85, 78]
for server, temp in zip(servers, temps):
    print(f"{server}: {temp}°C")

# join: 列表转字符串
ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
print(",".join(ips))         # 10.0.0.1,10.0.0.2,10.0.0.3

# 复制列表（注意陷阱！）
a = [1, 2, 3]
b = a           # 这不是复制！a 和 b 指向同一个列表
b[0] = 99
print(a)        # [99, 2, 3]（a 也被改了！）

# 正确的复制方式
c = [1, 2, 3]
d = c.copy()    # 或者 d = c[:] 或者 d = list(c)
d[0] = 99
print(c)        # [1, 2, 3]（c 没变）</code></pre></div>
<div class="tip-box danger"><p><strong>陷阱：</strong><code>b = a</code> 不是复制！它们指向同一个列表。要用 <code>b = a.copy()</code></p></div>`
      },
      {
        title: "实战：服务器状态管理",
        content: `<div class="text-block">用列表管理服务器集群——增删查改，模拟运维操作。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">all_servers = ["gpu-01", "gpu-02", "gpu-03", "gpu-04", "gpu-05"]
online = ["gpu-01", "gpu-03", "gpu-05"]
warning = ["gpu-03"]               # gpu-03 温度偏高
offline = ["gpu-02", "gpu-04"]

print("=== 服务器状态总览 ===")
print(f"总数: {len(all_servers)} 台")
print(f"在线: {len(online)} 台 → {', '.join(online)}")
print(f"告警: {len(warning)} 台 → {', '.join(warning)}")
print(f"离线: {len(offline)} 台 → {', '.join(offline)}")

# 模拟操作：gpu-02 恢复上线
offline.remove("gpu-02")
online.append("gpu-02")
print(f"\n>>> gpu-02 已恢复上线")
print(f"在线: {', '.join(online)}")

# 新增 gpu-06
all_servers.append("gpu-06")
online.append("gpu-06")
print(f"\n>>> gpu-06 已加入集群")
print(f"总数: {len(all_servers)} 台")

# 找出正常的服务器（在线但不在告警列表中）
normal = [s for s in online if s not in warning]
print(f"正常: {', '.join(normal)}")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "GPU 集群管理", desc: `给定初始列表，完成以下操作，每步都 print 验证`, answer: `gpus = ["gpu-01", "gpu-02", "gpu-03"]
gpus.append("gpu-04")
gpus.insert(0, "gpu-00")
gpus[2] = "gpu-02-new"
gpus.remove("gpu-03")
print(gpus)` ,
        starter: `gpus = ["gpu-01", "gpu-02", "gpu-03"]`
      },
      { title: "日志级别统计", desc: "统计每个级别出现次数，过滤出 ERROR 和 WARN，排序", answer: `log_levels = ["INFO", "ERROR", "WARN", "INFO", "ERROR", "INFO", "DEBUG", "ERROR"]
print(f"INFO: {log_levels.count('INFO')}")
print(f"ERROR: {log_levels.count('ERROR')}")
print(f"WARN: {log_levels.count('WARN')}")
print(f"DEBUG: {log_levels.count('DEBUG')}")
errors_and_warns = [l for l in log_levels if l in ("ERROR", "WARN")]
errors_and_warns.sort()
print(errors_and_warns)` ,
        starter: `log_levels = ["INFO", "ERROR", "WARN", "INFO", "ERROR", "INFO", "DEBUG", "ERROR"]`
      },
      { title: "交叉合并（挑战）", desc: "把 names 和 temps 列表合并成 ['gpu-01: 72°C', ...] 格式", answer: `names = ["gpu-01", "gpu-02", "gpu-03"]
temps = [72, 85, 78]
result = [f"{name}: {temp}°C" for name, temp in zip(names, temps)]
print(result)`
      ,
        starter: `names = ["gpu-01", "gpu-02", "gpu-03"]
temps = [72, 85, 78]`
      }
    ]
  },
  {
    id: 4, title: "字典 (dict)", icon: "D4",
    tag: "基础", tagClass: "green",
    desc: "能用字典存储和操作配置信息、服务状态等键值对数据",
    sections: [
            {
        title: "创建字典",
        content: `<div class="text-block">字典用花括号 <code>{}</code>，key:value 形式，key 通常是字符串。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">config = {
    "model": "qwen-72b",
    "port": 8000,
    "gpu_count": 4,
    "max_tokens": 2048
}

print(config)
print(type(config))          # &lt;class 'dict'>

# 空字典
empty1 = {}
empty2 = dict()

# 从两个列表创建字典
keys = ["name", "port", "status"]
values = ["gpu-01", 8000, "running"]
server = dict(zip(keys, values))
print(server)                # {'name': 'gpu-01', 'port': 8000, 'status': 'running'}</code></pre></div>` },
      {
        title: "查 — 取值（最常用的操作）",
        content: `<div class="text-block">取值用 <code>get()</code> 最安全，key 不存在返回 None 而不是报错。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">config = {"model": "qwen-72b", "port": 8000, "gpu_count": 4}

# 方式1：用方括号（key不存在会报 KeyError！）
print(config["model"])       # qwen-72b
# print(config["host"])      # KeyError! 不存在的key直接报错

# 方式2：用 get（推荐！不存在返回 None，不报错）
print(config.get("model"))           # qwen-72b
print(config.get("host"))            # None
print(config.get("host", "localhost"))  # 不存在时返回默认值

# 查看所有 key / value / 键值对
print(config.keys())         # dict_keys(['model', 'port', 'gpu_count'])
print(config.values())       # dict_values(['qwen-72b', 8000, 4])
print(config.items())        # dict_items([('model', 'qwen-72b'), ...])

# 判断 key 是否存在
print("model" in config)     # True
print("host" in config)      # False
print(len(config))           # 3</code></pre></div>`
      },
            {
        title: "增 / 改（操作一样！key 不存在就是增，存在就是改）",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">config = {"model": "qwen-72b", "port": 8000}

# 直接赋值
config["temperature"] = 0.7     # key 不存在 → 增
config["port"] = 8080           # key 已存在 → 改
print(config)

# update: 批量增/改
config.update({"port": 9000, "timeout": 30, "gpu_count": 4})
print(config)

# setdefault: 不存在才加，存在就不动
config.setdefault("port", 6006)      # port 已存在，不会改
config.setdefault("log_level", "INFO")  # log_level 不存在，会加上
print(config)</code></pre></div>`
      },
      {
        title: "删",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">config = {"model": "qwen-72b", "port": 8080, "gpu_count": 4, "timeout": 30}

# del: 按key删
del config["timeout"]
print(config)

# pop: 按key删，并返回被删的值
removed = config.pop("gpu_count")
print(f"删掉了: {removed}")       # 4
print(config)

# popitem: 删最后一个（Python 3.7+ 字典是有序的）
last = config.popitem()
print(f"最后插入的: {last}")       # ('port', 8080)

# clear: 清空
backup = config.copy()
config.clear()
print(f"清空后: {config}")
print(f"备份: {backup}")</code></pre></div>`
      },
      {
        title: "遍历字典",
        content: `<div class="text-block">遍历字典有三种方式，最常用的是 <code>items()</code> 同时拿 key 和 value。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">server = {
    "name": "gpu-01",
    "ip": "10.0.0.1",
    "port": 8000,
    "status": "running"
}

# 遍历 key
for key in server:
    print(key)

# 遍历 value
for value in server.values():
    print(value)

# 遍历 key-value 对（最常用！）
for key, value in server.items():
    print(f"{key}: {value}")</code></pre></div>`
      },
      {
        title: "嵌套字典",
        content: `<div class="text-block">实际工作中，字典里经常嵌套字典——比如多台服务器的信息。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">cluster = {
    "gpu-01": {"ip": "10.0.0.1", "gpu": 4, "status": "running"},
    "gpu-02": {"ip": "10.0.0.2", "gpu": 4, "status": "warning"},
    "gpu-03": {"ip": "10.0.0.3", "gpu": 2, "status": "offline"}
}

# 取某个服务器的信息
print(cluster["gpu-01"]["ip"])              # 10.0.0.1
print(cluster["gpu-02"]["status"])          # warning

# 遍历所有服务器
for name, info in cluster.items():
    print(f"{name} ({info['ip']}): {info['status']}, GPU: {info['gpu']}")

# 修改嵌套值
cluster["gpu-01"]["status"] = "maintenance"

# 添加新服务器
cluster["gpu-04"] = {"ip": "10.0.0.4", "gpu": 8, "status": "running"}
print(f"集群服务器数: {len(cluster)}")</code></pre></div>`
      },
      {
        title: "字典推导式",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 交换 key 和 value
status_map = {"running": 0, "stopped": 1, "error": 2}
reversed_map = {v: k for k, v in status_map.items()}
print(reversed_map)             # {0: 'running', 1: 'stopped', 2: 'error'}

# 从列表创建字典
servers = ["gpu-01", "gpu-02", "gpu-03"]
status_dict = {s: "running" for s in servers}

# 过滤：只保留 running 的
all_status = {"gpu-01": "running", "gpu-02": "offline", "gpu-03": "running"}
running_only = {k: v for k, v in all_status.items() if v == "running"}
print(running_only)  # {'gpu-01': 'running', 'gpu-03': 'running'}</code></pre></div>`
      },
      {
        title: "常用技巧",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 合并两个字典（Python 3.9+）
a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}
merged = a | b                 # {"x": 1, "y": 3, "z": 4}（b 覆盖 a 的重复 key）

# 旧版本写法
merged2 = {**a, **b}

# 安全取值的链式写法（避免 KeyError）
data = {"server": {"gpu": {"temp": 78}}}
temp = data.get("server", {}).get("gpu", {}).get("temp")
print(f"温度: {temp}")   # 温度: 78

# 不存在的路径也不会报错
temp2 = data.get("server", {}).get("cpu", {}).get("temp")
print(f"CPU温度: {temp2}")  # CPU温度: None</code></pre></div>
<div class="tip-box success"><p><strong>链式 get</strong> 是避免嵌套字典 KeyError 的利器：每层都给个 <code>{}</code> 默认值。</p></div>`
      },
      {
        title: "实战：模型服务配置管理",
        content: `<div class="text-block">用嵌套字典管理多个模型服务的配置——遍历、统计、修改。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">services = {
    "qwen-72b": {
        "port": 8000, "gpu": [0, 1, 2, 3],
        "max_tokens": 2048, "status": "running", "requests": 15823
    },
    "llama-70b": {
        "port": 8001, "gpu": [4, 5, 6, 7],
        "max_tokens": 4096, "status": "running", "requests": 8921
    },
    "mistral-7b": {
        "port": 8002, "gpu": [8],
        "max_tokens": 8192, "status": "stopped", "requests": 0
    }
}

print("=== 模型服务总览 ===")
for name, info in services.items():
    gpu_list = ",".join(str(g) for g in info["gpu"])
    print(f"  {name}: 端口={info['port']}, GPU=[{gpu_list}], 状态={info['status']}, 请求数={info['requests']:,}")

# 统计正在运行的服务
running = [name for name, info in services.items() if info["status"] == "running"]
print(f"\n运行中: {len(running)} 个 → {', '.join(running)}")

# 统计总 GPU 使用
total_gpus = sum(len(info["gpu"]) for info in services.values() if info["status"] == "running")
print(f"占用 GPU: {total_gpus} 张")

# 添加新服务
services["glm-4"] = {"port": 8003, "gpu": [9], "max_tokens": 4096, "status": "running", "requests": 0}
print(f"\n添加 glm-4 后，共 {len(services)} 个服务")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "配置管理", desc: `完成以下操作，每步 print 验证`, answer: `server = {"name": "gpu-01", "ip": "10.0.0.1", "port": 8000}
server["status"] = "running"
server["port"] = 8080
del server["ip"]
server["gpu_memory"] = "80GB"
print(server)` ,
        starter: `server = {"name": "gpu-01", "ip": "10.0.0.1", "port": 8000}`
      },
      { title: "GPU 统计", desc: "遍历嵌套字典，统计每个模型服务的 GPU 数量", answer: `total = 0
for name, info in models.items():
    gpu_count = len(info["gpu"])
    total += gpu_count
    print(f"{name}: {gpu_count} 张 GPU ({info['status']})")
print(f"总计: {total} 张 GPU")` ,
        starter: `models = {
    "qwen-72b": {"gpu": [0, 1, 2, 3], "status": "running"},
    "llama-70b": {"gpu": [4, 5], "status": "running"},
    "mistral-7b": {"gpu": [8], "status": "stopped"}
}`
      },
      { title: "配置合并（挑战）", desc: "合并两个字典，重复 key 以新配置为准", answer: `merged = old_config | new_config
print(merged)`
      ,
        starter: `old_config = {"model": "qwen-7b", "port": 8000, "gpu": 1}
new_config = {"model": "qwen-72b", "port": 8080, "timeout": 30}`
      }
    ]
  },
  {
    id: 5, title: "if/else 条件判断", icon: "D5",
    tag: "核心", tagClass: "blue",
    desc: "能让程序根据不同条件做不同的事",
    sections: [
            {
        title: "基础 if/else",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">gpu_temp = 85

if gpu_temp >= 80:
    print("告警：GPU 温度过高！")
else:
    print("温度正常")

# 改变温度值试试
gpu_temp = 72
if gpu_temp >= 80:
    print("告警：GPU 温度过高！")
else:
    print("温度正常")</code></pre></div>` },
      {
        title: "if/elif/else — 多个条件",
        content: `<div class="text-block">有多个条件分支时，用 <code>elif</code> 依次判断，直到匹配为止。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">status_code = 503

if status_code == 200:
    print("服务正常")
elif status_code == 404:
    print("接口不存在")
elif status_code == 500:
    print("服务器内部错误")
elif status_code == 503:
    print("服务不可用")
else:
    print(f"未知状态: {status_code}")</code></pre></div>`
      },
            {
        title: "比较运算符",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">cpu_usage = 87.5
threshold = 90

# 大于 / 小于
print(cpu_usage > threshold)     # False
print(cpu_usage < threshold)     # True
print(cpu_usage >= 87.5)         # True（大于等于）
print(cpu_usage <= 90)           # True（小于等于）

# 等于 / 不等于（注意：比较相等用 ==，不是 =）
port = 8000
print(port == 8000)              # True
print(port != 8080)              # True（不等于）</code></pre></div>`
      },
      {
        title: "逻辑运算符：and / or / not",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">cpu = 85
memory = 90
disk = 60

# and: 两个条件都满足
if cpu > 80 and memory > 80:
    print("CPU 和内存都高！")

# or: 满足其中一个
if cpu > 90 or memory > 90 or disk > 90:
    print("至少一项资源告警！")

# not: 取反
is_healthy = False
if not is_healthy:
    print("服务不健康")

# 实际例子：判断是否需要告警
if cpu > 80 or memory > 85 or disk > 90:
    print("资源告警！请检查")
else:
    print("资源正常")</code></pre></div>`
      },
      {
        title: "in 判断",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">status = "running"
valid_statuses = ["running", "stopped", "error"]

if status in valid_statuses:
    print(f"状态有效: {status}")
else:
    print(f"无效状态: {status}")

# 字符串也可以用 in
log = "ERROR: GPU OOM"
if "ERROR" in log:
    print("发现错误日志")
elif "WARN" in log:
    print("发现警告日志")

# not in
if "DEBUG" not in log:
    print("非调试日志")</code></pre></div>`
      },
      {
        title: "嵌套 if",
        content: `<div class="text-block">条件里还可以嵌套条件，但尽量别太深，2 层就够。更清晰的做法是用 <code>and</code> 合并。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">service = {
    "name": "qwen-72b",
    "status": "running",
    "gpu_temp": 82,
    "memory_usage": 75
}

# 嵌套判断
if service["status"] == "running":
    if service["gpu_temp"] > 80:
        print(f"{service['name']} 运行中但温度过高！")
    else:
        print(f"{service['name']} 一切正常")
else:
    print(f"{service['name']} 未运行")

# 更清晰的写法：用 and 合并
if service["status"] == "running" and service["gpu_temp"] > 80:
    print(f"{service['name']} 温度过高告警")</code></pre></div>`
      },
      {
        title: "三元表达式",
        content: `<div class="text-block">一行搞定简单的 if/else：<strong>值A if 条件 else 值B</strong></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">gpu_temp = 78
alert = "告警" if gpu_temp >= 80 else "正常"
print(f"GPU 温度: {gpu_temp}°C → {alert}")

# 用在 f-string 里
port = 8000
print(f"端口: {port} ({'开放' if port == 8000 else '异常'})")</code></pre></div>`
      },
      {
        title: "真值和假值",
        content: `<div class="text-block">以下值在 if 中被视为 <strong>False</strong>（假值）：<code>None</code>、<code>False</code>、<code>0</code>、<code>0.0</code>、<code>""</code>、<code>[]</code>、<code>{}</code>。其他都是 True。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 常见用法：检查变量是否有值
log = ""
if log:
    print(f"日志内容: {log}")
else:
    print("日志为空")

servers = []
if servers:
    print(f"有 {len(servers)} 台服务器")
else:
    print("没有服务器")

error_count = 0
if error_count:
    print(f"有 {error_count} 个错误")
else:
    print("没有错误")</code></pre></div>
<div class="tip-box success"><p><strong>实用：</strong><code>if var:</code> 可以检查字符串/列表/字典是否为空，比 <code>if len(var) > 0:</code> 更简洁。</p></div>`
      },
      {
        title: "实战：服务健康检查逻辑",
        content: `<div class="text-block">综合运用 if/elif/else、逻辑运算、in 判断，写一个服务健康检查函数。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def check_service(name, status, cpu, memory, gpu_temp, error_count):
    """检查服务状态，返回健康等级"""
    if status != "running":
        return "CRITICAL", f"{name} 未运行"

    issues = []
    if cpu > 90:
        issues.append(f"CPU {cpu}%")
    if memory > 90:
        issues.append(f"内存 {memory}%")
    if gpu_temp > 85:
        issues.append(f"GPU温度 {gpu_temp}°C")
    if error_count > 100:
        issues.append(f"错误数 {error_count}")

    if len(issues) == 0:
        return "HEALTHY", f"{name} 一切正常"
    elif len(issues) == 1:
        return "WARNING", f"{name} 注意: {'; '.join(issues)}"
    else:
        return "CRITICAL", f"{name} 多项异常: {'; '.join(issues)}"

# 测试
test_cases = [
    ("qwen-72b", "running", 45, 60, 72, 5),
    ("llama-70b", "running", 92, 88, 70, 10),
    ("mistral-7b", "stopped", 0, 0, 0, 0),
    ("glm-4", "running", 95, 92, 88, 150),
]

print("=== 服务健康检查 ===")
for name, status, cpu, mem, temp, errors in test_cases:
    level, msg = check_service(name, status, cpu, mem, temp, errors)
    print(f"[{level}] {msg}")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "端口范围判断", desc: `给定一个端口，判断属于哪个范围<br>0-1023: 系统保留端口<br>1024-49151: 注册端口<br>49152-65535: 动态端口<br>其他: 无效端口`, answer: `port = 8000
if 0 <= port <= 1023:
    print(f"端口 {port} 是系统保留端口")
elif 1024 <= port <= 49151:
    print(f"端口 {port} 是注册端口")
elif 49152 <= port <= 65535:
    print(f"端口 {port} 是动态端口")
else:
    print(f"端口 {port} 无效")` ,
        starter: `port = 8000`
      },
      { title: "日志级别处理", desc: `根据日志级别输出不同的处理方式<br>ERROR: 立即通知<br>WARN: 记录并关注<br>INFO: 正常记录<br>DEBUG: 开发环境才显示<br>其他: 未知级别`, answer: `level = "WARN"
if level == "ERROR":
    print("ERROR → 立即通知")
elif level == "WARN":
    print("WARN → 记录并关注")
elif level == "INFO":
    print("INFO → 正常记录")
elif level == "DEBUG":
    print("DEBUG → 开发环境才显示")
else:
    print(f"{level} → 未知级别")` ,
        starter: `level = "WARN"`
      },
      { title: "扩容判断（挑战）", desc: `条件：同时满足以下任意两项就需要扩容<br>- CPU使用率 > 80%<br>- 内存使用率 > 85%<br>- 请求队列 > 100<br>- GPU使用率 > 90%`, answer: `cpu_usage = 85
memory_usage = 88
request_queue = 50
gpu_usage = 92
flags = [cpu_usage > 80, memory_usage > 85, request_queue > 100, gpu_usage > 90]
if sum(flags) >= 2:
    print("需要扩容")
else:
    print("暂不需要扩容")`
      ,
        starter: `cpu_usage = 85
memory_usage = 88
request_queue = 50
gpu_usage = 92`
      }
    ]
  },
{
    id: 6, title: "for/while 循环", icon: "D6",
    tag: "核心", tagClass: "blue",
    desc: "能批量处理服务器、日志、配置等重复性任务",
    sections: [
      {
        title: "for 循环 — 遍历",
        content: `<div class="text-block">for 循环用于遍历序列（列表、字典、字符串等），是处理批量任务的基础。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 遍历列表
servers = ["gpu-01", "gpu-02", "gpu-03"]
for server in servers:
    print(f"检查 {server} ... 正常")

# 遍历字典
config = {"model": "qwen-72b", "port": 8000, "gpu": 4}
for key, value in config.items():
    print(f"{key} = {value}")

# 遍历字符串
for char in "GPU":
    print(char)</code></pre></div>` },
      {
        title: "range — 生成数字序列",
        content: `<div class="table-wrap"><table><tr><th>写法</th><th>生成</th><th>例子</th></tr>
<tr><td><code>range(止)</code></td><td>0 到 止-1</td><td><code>range(5)</code> → 0,1,2,3,4</td></tr>
<tr><td><code>range(起, 止)</code></td><td>起到 止-1</td><td><code>range(1,4)</code> → 1,2,3</td></tr>
<tr><td><code>range(起, 止, 步长)</code></td><td>步长间隔</td><td><code>range(0,10,2)</code> → 0,2,4,6,8</td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># range(止)
for i in range(5):
    print(i, end=" ")           # 0 1 2 3 4
print()

# range(起, 止)
for i in range(1, 4):
    print(i, end=" ")           # 1 2 3
print()

# range(起, 止, 步长)
for i in range(0, 10, 2):
    print(i, end=" ")           # 0 2 4 6 8
print()

# 实际用途：批量生成服务器名
for i in range(1, 6):
    print(f"gpu-{i:02d}")       # gpu-01 到 gpu-05（:02d 补零）

# 反着数
for i in range(5, 0, -1):
    print(i, end=" ")           # 5 4 3 2 1</code></pre></div>`
      },
      {
        title: "enumerate — 同时拿索引和值",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">servers = ["gpu-01", "gpu-02", "gpu-03"]

for index, name in enumerate(servers):
    print(f"第 {index} 台: {name}")

# 指定起始编号
for index, name in enumerate(servers, start=1):
    print(f"服务器 {index}: {name}")</code></pre></div>`
      },
      {
        title: "zip — 同时遍历多个列表",
        content: `<div class="text-block"><code>zip()</code> 把多个列表"拉链"在一起，同时遍历。长度不同时以最短的为准。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">servers = ["gpu-01", "gpu-02", "gpu-03"]
temps = [72, 85, 78]
statuses = ["running", "warning", "running"]

for server, temp, status in zip(servers, temps, statuses):
    print(f"{server}: {temp}°C ({status})")

# 长度不同时，以最短的为准
a = [1, 2, 3, 4, 5]
b = ["a", "b", "c"]
for x, y in zip(a, b):
    print(x, y)                 # 只输出3组</code></pre></div>`
      },
            {
        title: "while 循环 — 条件为 True 就一直跑",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 基础：倒计时
count = 5
while count > 0:
    print(f"等待 {count} 秒...")
    count -= 1
print("完成！")

# 实际用途：轮询服务状态（模拟）
import random
retry = 0
max_retry = 3
while retry < max_retry:
    retry += 1
    success = random.random() > 0.5
    if success:
        print(f"第 {retry} 次尝试: 成功")
        break
    else:
        print(f"第 {retry} 次尝试: 失败，重试...")
else:
    # while 的 else: 循环正常结束（没被 break）才执行
    print(f"重试 {max_retry} 次后仍然失败")</code></pre></div>`
      },
      {
        title: "break 和 continue",
        content: `<div class="text-block"><code>break</code> 立即跳出整个循环，<code>continue</code> 跳过本次继续下一次。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># break: 立即跳出整个循环
servers = ["gpu-01", "gpu-02", "ERROR", "gpu-03"]
for server in servers:
    if server == "ERROR":
        print("发现错误，停止检查")
        break
    print(f"检查 {server}: 正常")

# continue: 跳过本次，继续下一次
print()
for server in servers:
    if server == "ERROR":
        print(f"跳过异常项: {server}")
        continue
    print(f"检查 {server}: 正常")</code></pre></div>`
      },
      {
        title: "循环中的列表操作",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">logs = [
    "INFO  Service started",
    "ERROR GPU OOM",
    "WARN  Request timeout",
    "INFO  Model loaded",
    "ERROR GPU overheat",
]

# 只提取 ERROR 日志
errors = []
for log in logs:
    if "ERROR" in log:
        errors.append(log)
print("ERROR日志:", errors)

# 用列表推导式（更简洁）
errors2 = [log for log in logs if "ERROR" in log]

# 计数
log_levels = {"INFO": 0, "WARN": 0, "ERROR": 0, "DEBUG": 0}
for log in logs:
    for level in log_levels:
        if log.startswith(level):
            log_levels[level] += 1
            break
print("日志统计:", log_levels)</code></pre></div>`
      },
      {
        title: "嵌套循环",
        content: `<div class="text-block">循环里面还能套循环——比如检查每台服务器的每个 GPU。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">cluster = {
    "gpu-01": [72, 74, 71, 73],
    "gpu-02": [85, 88, 82, 90],
}

for server, temps in cluster.items():
    print(f"\n{server}:")
    for i, temp in enumerate(temps):
        status = "告警" if temp > 80 else "正常"
        print(f"  GPU{i}: {temp}°C {status}")</code></pre></div>
<div class="tip-box info"><p><strong>注意：</strong>嵌套循环层数尽量不超过 2 层，超过就该考虑封装成函数了。</p></div>`
      },
      {
        title: "实战：批量服务检查",
        content: `<div class="text-block">综合运用 for 循环、enumerate、条件判断，批量检查服务状态。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">services = [
    {"name": "qwen-72b", "port": 8000, "status": "running", "requests": 1500},
    {"name": "llama-70b", "port": 8001, "status": "running", "requests": 890},
    {"name": "mistral-7b", "port": 8002, "status": "stopped", "requests": 0},
    {"name": "glm-4", "port": 8003, "status": "running", "requests": 2300},
    {"name": "qwen-7b", "port": 8004, "status": "error", "requests": 0},
]

print("=== 批量服务检查 ===")
print(f"{'服务名':<15} {'端口':<8} {'状态':<10} {'请求数':>8}")
print("-" * 45)

total_requests = 0
running_count = 0
error_servers = []

for svc in services:
    total_requests += svc["requests"]
    if svc["status"] == "running":
        running_count += 1
    elif svc["status"] == "error":
        error_servers.append(svc["name"])
    print(f"{svc['name']:<15} {svc['port']:<8} {svc['status']:<10} {svc['requests']:>8,}")

print("-" * 45)
print(f"总计: {len(services)} 个服务, {running_count} 个运行中, 总请求 {total_requests:,}")
if error_servers:
    print(f"异常服务: {', '.join(error_servers)}")

# 找出请求数最多的服务
busiest = max(services, key=lambda s: s["requests"])
print(f"最繁忙: {busiest['name']} ({busiest['requests']:,} 请求)")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "批量生成配置", desc: `生成 5 台服务器的基础配置<br>期望输出:<br>gpu-01: port=8001, ip=10.0.1.1<br>gpu-02: port=8002, ip=10.0.1.2<br>... 以此类推`, answer: `for i in range(1, 6):
    port = 8000 + i
    ip = f"10.0.1.{i}"
    print(f"gpu-{i:02d}: port={port}, ip={ip}")` },
      { title: "找出异常温度", desc: "从嵌套数据中找出所有超过 80°C 的 GPU", answer: `for server, gpu_temps in temps.items():
    for i, temp in enumerate(gpu_temps):
        if temp > 80:
            print(f"{server} GPU{i}: {temp}°C")` ,
        starter: `temps = {"gpu-01": [72, 74, 71, 73], "gpu-02": [82, 88, 75, 91], "gpu-03": [70, 68, 72, 69]}`
      },
      { title: "服务重启模拟（挑战）", desc: `模拟一个不靠谱的服务，每次启动有 70% 概率失败<br>用 while 循环，最多重试 3 次<br>成功就 print "启动成功" 并停止<br>3 次都失败就 print "启动失败，需要人工介入"`, answer: `import random
retry = 0
max_retry = 3
while retry < max_retry:
    retry += 1
    success = random.random() > 0.7
    if success:
        print(f"第 {retry} 次尝试: 启动成功")
        break
    else:
        print(f"第 {retry} 次尝试: 启动失败")
else:
    print("启动失败，需要人工介入")`
      }
    ]
  },
  {
    id: 7, title: "函数 (def)", icon: "D7",
    tag: "核心", tagClass: "blue",
    desc: "能把重复代码封装成函数，提高复用性",
    sections: [
            {
        title: "定义和调用函数",
        content: `<div class="text-block">函数是<strong>可复用的代码块</strong>。用 <code>def</code> 定义，写一次，到处调用。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def greet():
    """简单的无参数函数"""
    print("Hello, 运维工程师！")

greet()        # 调用函数
greet()        # 可以反复调用</code></pre></div>` },
      {
        title: "带参数的函数",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def check_server(name, status):
    """带参数的函数"""
    if status == "running":
        print(f"{name}: 正常运行")
    else:
        print(f"{name}: 异常 ({status})")

check_server("gpu-01", "running")
check_server("gpu-02", "stopped")</code></pre></div>`
      },
      {
        title: "返回值 — 函数的结果",
        content: `<div class="text-block"><code>return</code> 让函数返回一个结果。可以返回多个值（实际是元组）。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def get_status_code(level):
    """根据日志级别返回状态码"""
    if level == "ERROR":
        return 2
    elif level == "WARN":
        return 1
    else:
        return 0

code = get_status_code("ERROR")
print(f"状态码: {code}")       # 2

# 返回多个值（实际返回的是元组）
def get_server_info(name):
    """返回服务器的多个信息"""
    return name, 8000, "running"

server, port, status = get_server_info("gpu-01")
print(f"{server}:{port} {status}")</code></pre></div>`
      },
            {
        title: "默认参数",
        content: `<div class="text-block">参数可以有默认值，调用时可以省略。也可以用<code>命名参数</code>跳着传。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def check_health(url, timeout=5, retries=3):
    """带默认值的参数，调用时可以省略"""
    print(f"检查 {url}, 超时={timeout}s, 重试={retries}次")

check_health("http://gpu-01:8000")                    # 用默认值
check_health("http://gpu-01:8000", timeout=10)        # 覆盖 timeout
check_health("http://gpu-01:8000", retries=5, timeout=10)  # 命名参数，顺序随意</code></pre></div>`
      },
      {
        title: "关键字参数（kwargs）",
        content: `<div class="text-block"><code>**kwargs</code> 接收任意额外的关键字参数，非常适合做灵活的配置函数。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def create_service(name, port, gpu=1, max_tokens=2048, **kwargs):
    """**kwargs 接收任意额外的关键字参数"""
    config = {
        "name": name,
        "port": port,
        "gpu": gpu,
        "max_tokens": max_tokens,
    }
    config.update(kwargs)       # 把额外的参数都加进去
    return config

svc = create_service(
    "qwen-72b", 8000,
    gpu=4, max_tokens=4096,
    temperature=0.7,            # 额外参数，会被 kwargs 接收
    top_p=0.9
)
print(svc)</code></pre></div>`
      },
      {
        title: "文档字符串 docstring",
        content: `<div class="text-block">三引号字符串放在函数体第一行，就是文档字符串。好的 docstring 让别人（和未来的自己）知道函数怎么用。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def calculate_gpu_memory(total_gb, used_gb, safety_margin=0.1):
    """
    计算可用的 GPU 显存

    参数:
        total_gb: 总显存 (GB)
        used_gb: 已用显存 (GB)
        safety_margin: 安全余量比例，默认 10%

    返回:
        可用显存 (GB)
    """
    available = (total_gb - used_gb) * (1 - safety_margin)
    return round(available, 2)

result = calculate_gpu_memory(80, 45)
print(f"可用显存: {result} GB")</code></pre></div>
<div class="tip-box success"><p>用 <code>help(函数名)</code> 可以查看 docstring。养成写 docstring 的习惯。</p></div>`
      },
      {
        title: "变量作用域",
        content: `<div class="text-block">函数内部的变量是<strong>局部变量</strong>，函数外访问不到。函数外的变量是<strong>全局变量</strong>，函数内能读但不能直接改（除非用 <code>global</code>）。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">global_var = "我是全局变量"

def test_scope():
    local_var = "我是局部变量"
    print(global_var)           # 能访问全局变量
    print(local_var)            # 能访问局部变量

test_scope()
# print(local_var)             # 报错！函数外访问不到局部变量

# 修改全局变量需要 global 关键字
counter = 0
def increment():
    global counter
    counter += 1

increment()
increment()
print(f"计数: {counter}")       # 2

# 更好的做法：通过参数传入，通过返回值传出（避免用 global）
def increment_better(n):
    return n + 1

counter = increment_better(increment_better(counter))
print(f"计数: {counter}")       # 2</code></pre></div>
<div class="tip-box info"><p><strong>最佳实践：</strong>尽量用参数和返回值传数据，少用 global。</p></div>`
      },
      {
        title: "lambda 匿名函数",
        content: `<div class="text-block">简短的一行函数，常和 <code>sorted</code>、<code>map</code>、<code>filter</code> 配合使用。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">services = [
    {"name": "qwen-72b", "port": 8000},
    {"name": "llama-70b", "port": 8001},
    {"name": "mistral-7b", "port": 8002},
]

# 常和 sorted / max / min 配合
sorted_by_port = sorted(services, key=lambda s: s["port"])
print([s["name"] for s in sorted_by_port])

# map: 对每个元素执行操作
names = list(map(lambda s: s["name"], services))
print(names)                   # ['qwen-72b', 'llama-70b', 'mistral-7b']

# filter: 过滤
running = list(filter(lambda s: s["port"] >= 8001, services))
print([s["name"] for s in running])</code></pre></div>`
      },
      {
        title: "实战：运维常用工具函数",
        content: `<div class="text-block">把常用操作封装成函数，写一次用无数次。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def parse_log_line(line):
    """解析一行日志，返回结构化数据"""
    try:
        parts = line.strip().split()
        return {
            "timestamp": f"{parts[0]} {parts[1]}",
            "level": parts[2],
            "message": " ".join(parts[3:])
        }
    except (IndexError, AttributeError):
        return None

def check_resource(name, usage, threshold=90):
    """检查资源使用率并返回状态"""
    if usage > threshold:
        return f"告警: {name} 使用率 {usage}% 超过阈值 {threshold}%"
    elif usage > threshold * 0.8:
        return f"注意: {name} 使用率 {usage}% 接近阈值"
    else:
        return f"正常: {name} 使用率 {usage}%"

def format_bytes(size_gb):
    """格式化存储大小"""
    if size_gb >= 1024:
        return f"{size_gb / 1024:.1f} TB"
    else:
        return f"{size_gb:.1f} GB"

# 使用
print("=== 资源检查 ===")
print(check_resource("CPU", 45))
print(check_resource("内存", 88))
print(check_resource("GPU显存", 95))
print(f"模型大小: {format_bytes(14.3)}")
print(f"数据集大小: {format_bytes(2048)}")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "GPU 利用率函数", desc: `输入: 总显存(GB), 已用显存(GB)<br>返回: 利用率百分比（保留1位小数）<br>例: <code>gpu_usage(80, 60)</code> → 75.0%`, answer: `def gpu_usage(total, used):
    return round(used / total * 100, 1)
print(gpu_usage(80, 60))` },
      { title: "端口过滤函数", desc: `输入: 端口列表<br>返回: 合法的端口列表（1024-65535）<br>例: <code>filter_ports([80, 8000, 99999, 443, 8080])</code> → [8000, 8080]`, answer: `def filter_ports(ports):
    return [p for p in ports if 1024 <= p <= 65535]
print(filter_ports([80, 8000, 99999, 443, 8080]))` },
      { title: "日志统计函数（挑战）", desc: `输入: 日志行列表<br>返回: 字典 {"INFO": x, "WARN": y, "ERROR": z, "total": n}`, answer: `def count_logs(logs):
    counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
    total = 0
    for log in logs:
        for level in counts:
            if level in log:
                counts[level] += 1
                total += 1
                break
    counts["total"] = total
    return counts
test_logs = ["INFO ok", "ERROR fail", "WARN slow", "INFO done", "ERROR crash"]
print(count_logs(test_logs))`
      }
    ]
  },
  {
    id: 8, title: "文件读写", icon: "D8",
    tag: "核心", tagClass: "amber",
    desc: "能读取日志文件、写入配置、处理 CSV/TXT",
    sections: [
            {
        title: "写入文件",
        content: `<div class="text-block"><strong>永远用 with 语句</strong>，它会自动关闭文件。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 写文本文件（覆盖已有内容）
with open("test_log.txt", "w") as f:
    f.write("2024-01-15 10:23:01 INFO  Service started\n")
    f.write("2024-01-15 10:25:30 WARN  Request timeout\n")
    f.write("2024-01-15 10:26:02 ERROR GPU OOM\n")
    f.write("2024-01-15 10:26:30 INFO  Service recovered\n")

print("文件已写入: test_log.txt")

# 追加内容（不覆盖）
with open("test_log.txt", "a") as f:
    f.write("2024-01-15 10:30:00 ERROR GPU overheat\n")

print("已追加内容")</code></pre></div>` },
      {
        title: "读取文件",
        content: `<div class="text-block">有三种读取方式，<strong>逐行遍历</strong>最推荐（省内存）。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 方式1：read() 读取全部内容为一个大字符串
with open("test_log.txt", "r") as f:
    content = f.read()
print("--- read() ---")
print(content)

# 方式2：readlines() 读取所有行为列表
with open("test_log.txt", "r") as f:
    lines = f.readlines()
print("--- readlines() ---")
print(f"共 {len(lines)} 行")
print(lines[0].strip())        # strip() 去掉末尾的 \n

# 方式3：逐行遍历（推荐！内存友好，适合大文件）
print("--- 逐行遍历 ---")
with open("test_log.txt", "r") as f:
    for line in f:
        print(line.strip())</code></pre></div>`
      },
      {
        title: "with 语句详解",
        content: `<div class="text-block">with 会自动关闭文件，即使出错了也会关。<strong>永远用 with</strong>，不要手动 open/close。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># ❌ 错误示范（不要这么写）
# f = open("test.txt")
# content = f.read()
# f.close()     # 忘了关就完了

# ✅ 正确写法（永远这么写）
with open("test.txt") as f:
    content = f.read()
# 出了 with 块，文件自动关了

# 同时打开多个文件
with open("input.txt") as fin, open("output.txt", "w") as fout:
    for line in fin:
        fout.write(line)</code></pre></div>
<div class="tip-box success"><p><strong>原则：</strong>只要操作文件，就用 <code>with open(...) as f:</code>，不要手动 close。</p></div>`
      },
      {
        title: "文件模式",
        content: `<div class="table-wrap"><table><tr><th>模式</th><th>含义</th><th>说明</th></tr>
<tr><td><code>"r"</code></td><td>读（默认）</td><td>文件不存在会报错</td></tr>
<tr><td><code>"w"</code></td><td>写（覆盖）</td><td>文件不存在会创建</td></tr>
<tr><td><code>"a"</code></td><td>追加</td><td>在末尾添加，不覆盖</td></tr>
<tr><td><code>"x"</code></td><td>创建新文件</td><td>已存在会报错，防止意外覆盖</td></tr>
<tr><td><code>"rb"/"wb"</code></td><td>二进制读写</td><td>图片、压缩包等</td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># "x" 模式：创建新文件，避免意外覆盖
try:
    with open("log.txt", "x") as f:
        f.write("不会执行，因为文件已存在")
except FileExistsError:
    print("文件已存在，跳过创建")</code></pre></div>`
      },
      {
        title: "JSON 配置文件",
        content: `<div class="text-block">JSON 是最常用的配置格式。Python 的 <code>json</code> 模块可以轻松读写。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import json

config = {
    "model": "qwen-72b",
    "port": 8000,
    "gpu_count": 4,
    "max_tokens": 2048,
    "servers": ["gpu-01", "gpu-02", "gpu-03"]
}

# 写 JSON
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)      # indent=2 让输出有缩进，好看
print("配置已写入: config.json")

# 读 JSON
with open("config.json", "r") as f:
    loaded = json.load(f)
print(f"读取配置: {loaded['model']}")</code></pre></div>`
      },
      {
        title: "CSV 文件处理",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import csv

# 写 CSV
logs_data = [
    ["timestamp", "level", "server", "message"],
    ["2024-01-15 10:23:01", "INFO", "gpu-01", "Service started"],
    ["2024-01-15 10:25:30", "WARN", "gpu-01", "Request timeout"],
    ["2024-01-15 10:26:02", "ERROR", "gpu-02", "GPU OOM"],
]

with open("logs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(logs_data)

# 用字典方式读 CSV（更方便）
with open("logs.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["level"] == "ERROR":
            print(f"ERROR: {row['server']} - {row['message']}")</code></pre></div>`
      },
      {
        title: "os 模块 — 文件和目录操作",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import os

# 获取文件信息
print(f"文件存在: {os.path.exists('log.txt')}")
print(f"文件大小: {os.path.getsize('log.txt')} 字节")

# 目录操作
os.makedirs("output", exist_ok=True)   # 创建目录（已存在不报错）

# 列出目录内容
for item in os.listdir("."):
    if item.endswith(".py"):
        print(f"  Python 文件: {item}")

# 路径拼接（推荐用 os.path.join，不要手动拼 /）
log_dir = "output"
log_file = "service.log"
full_path = os.path.join(log_dir, log_file)
print(f"完整路径: {full_path}")</code></pre></div>`
      },
      {
        title: "实战：日志分析器",
        content: `<div class="text-block">综合运用文件读写、字符串操作、循环——写一个完整的日志分析工具。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 创建测试日志
test_logs = """2024-01-15 10:23:01 INFO  [qwen-72b] Service started on port 8000
2024-01-15 10:23:15 INFO  [qwen-72b] Model loaded, GPU: 4
2024-01-15 10:25:30 WARN  [qwen-72b] Request timeout, client=10.0.1.100
2024-01-15 10:26:02 ERROR [qwen-72b] GPU OOM, used=79.2GB/80GB
2024-01-15 10:26:05 WARN  [qwen-72b] Auto restart triggered
2024-01-15 10:26:30 INFO  [qwen-72b] Service recovered
2024-01-15 10:28:00 INFO  [llama-70b] Service started on port 8001
2024-01-15 10:30:00 ERROR [llama-70b] GPU overheat, temp=92°C
2024-01-15 10:30:15 INFO  [llama-70b] Cooling down, temp=85°C
"""

with open("service.log", "w") as f:
    f.write(test_logs)

# 分析日志
stats = {"INFO": 0, "WARN": 0, "ERROR": 0}
error_lines = []

with open("service.log", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        for level in stats:
            if f" {level} " in line:
                stats[level] += 1
                if level == "ERROR":
                    error_lines.append(line)
                break

print("=== 日志分析器 ===")
for level, count in stats.items():
    print(f"  {level}: {count}")
print(f"  总计: {sum(stats.values())}")

print(f"\nERROR 详情:")
for line in error_lines:
    parts = line.split(" ", 3)
    time_str = f"{parts[0]} {parts[1]}"
    msg = parts[3]
    print(f"  [{time_str}] {msg}")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "文件行数统计", desc: `输入: 文件路径<br>返回: 行数<br>提示: 用 with open + <code>sum(1 for line in f)</code>`, answer: `def count_lines(filepath):
    with open(filepath, "r") as f:
        return sum(1 for line in f)
print(f"行数: {count_lines('test_log.txt')}")` },
      { title: "字典列表保存为 CSV", desc: `输入: 文件路径, 字典列表<br>例: <code>save_csv("servers.csv", [{"name": "gpu-01", "ip": "10.0.0.1"}, ...])</code>`, answer: `def save_csv(filepath, data):
    if not data:
        return
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
test_data = [{"name": "gpu-01", "ip": "10.0.0.1"}, {"name": "gpu-02", "ip": "10.0.0.2"}]
save_csv("test_servers.csv", test_data)` },
      { title: "日志过滤工具（挑战）", desc: `函数名: <code>filter_logs(input_file, output_file, level="ERROR")</code><br>功能: 从输入文件中过滤出指定级别的日志，写入输出文件`, answer: `def filter_logs(input_file, output_file, level="ERROR"):
    with open(input_file, "r") as fin:
        with open(output_file, "w") as fout:
            for line in fin:
                if f" {level} " in line:
                    fout.write(line)
filter_logs("service.log", "output/errors.log", "ERROR")`
      }
    ]
  },
  {
    id: 9, title: "异常处理 (try/except)", icon: "D9",
    tag: "进阶", tagClass: "amber",
    desc: "让脚本遇到错误不崩溃，能优雅处理",
    sections: [
      {
        title: "为什么要处理异常？",
        content: `<div class="text-block">没有异常处理：脚本一遇到错误就整个崩溃退出。有了异常处理：跳过错误继续运行，或者给出友好提示。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 这行会崩溃：
# result = 10 / 0               # ZeroDivisionError

# 用 try/except 保护
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零！")

print("脚本继续运行...")        # 没有崩溃，继续往下走</code></pre></div>` },
      {
        title: "基础 try/except",
        content: `<div class="text-block">捕获不同类型的异常，分别处理。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">try:
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
    print("key 不存在")</code></pre></div>`
      },
      {
        title: "捕获多种异常",
        content: `<div class="text-block">一个函数可能有多种错误，可以分别捕获，也可以用一个 except 捕获多种。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def safe_divide(a, b):
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
    print(f"转换失败: {e}")</code></pre></div>`
      },
      {
        title: "try/except/else/finally 完整结构",
        content: `<div class="table-wrap"><table><tr><th>子句</th><th>何时执行</th></tr>
<tr><td><code>try</code></td><td>尝试执行的代码</td></tr>
<tr><td><code>except</code></td><td>发生异常时</td></tr>
<tr><td><code>else</code></td><td>没有异常时</td></tr>
<tr><td><code>finally</code></td><td>无论如何都执行（清理资源）</td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def read_config(filepath):
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
        # 无论如何都会执行
        print("读取操作完成")

read_config("config.json")       # 存在的文件
read_config("not_exist.json")    # 不存在的文件</code></pre></div>`
      },
      {
        title: "获取异常信息",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python"># 获取异常类型和消息
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
    traceback.print_exc()      # 打印完整的错误栈（调试时很有用）</code></pre></div>
<div class="tip-box info"><p>调试时用 <code>traceback.print_exc()</code> 看完整错误栈，上线后用 <code>logging</code> 记录日志。</p></div>`
      },
      {
        title: "主动抛出异常",
        content: `<div class="text-block">用 <code>raise</code> 主动抛出异常，用于输入校验和业务逻辑检查。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">def check_port(port):
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
    print(f"类型检查失败: {e}")</code></pre></div>`
      },
      {
        title: "自定义异常",
        content: `<div class="text-block">继承 <code>Exception</code> 创建自己的异常类，让错误处理更有业务含义。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">class ServiceError(Exception):
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
        print(f"[显存告警] {e}")</code></pre></div>`
      },
      {
        title: "常见异常速查",
        content: `<div class="table-wrap"><table><tr><th>异常名</th><th>什么时候发生</th></tr>
<tr><td><code>ValueError</code></td><td>值不对，如 int('abc')</td></tr>
<tr><td><code>TypeError</code></td><td>类型不对，如 '2' + 2</td></tr>
<tr><td><code>KeyError</code></td><td>字典 key 不存在</td></tr>
<tr><td><code>IndexError</code></td><td>列表下标越界</td></tr>
<tr><td><code>FileNotFoundError</code></td><td>文件不存在</td></tr>
<tr><td><code>PermissionError</code></td><td>没有权限</td></tr>
<tr><td><code>ZeroDivisionError</code></td><td>除以零</td></tr>
<tr><td><code>AttributeError</code></td><td>对象没有这个属性/方法</td></tr>
<tr><td><code>ImportError</code></td><td>导入模块失败</td></tr>
<tr><td><code>json.JSONDecodeError</code></td><td>JSON 格式错误</td></tr></table></div>`
      },
      {
        title: "实战：健壮的配置文件读取",
        content: `<div class="text-block">综合运用异常处理，写一个安全的 JSON 配置读取器。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import json

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
print("=== 配置文件读取测试 ===")
config = load_config("config.json")
print(f"模型: {config.get('model', '未知')}")

config2 = load_config("not_exist.json", {"model": "default", "port": 8080})
print(f"默认配置: {config2}")</code></pre></div>`
      }
    ],
    exercises: [
      { title: "安全数字转换", desc: `<code>safe_int(value, default=0)</code><br>能转就转，不能转返回默认值<br><code>safe_int("42")</code> → 42<br><code>safe_int("abc")</code> → 0<br><code>safe_int("abc", default=-1)</code> → -1`, answer: `def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
print(safe_int("42"))
print(safe_int("abc"))
print(safe_int("abc", default=-1))` },
      { title: "安全字典取值", desc: `<code>safe_get(data, keys, default=None)</code><br>data = {"a": {"b": {"c": 42}}}<br><code>safe_get(data, ["a", "b", "c"])</code> → 42<br><code>safe_get(data, ["a", "x", "y"])</code> → None（不报错）<br><code>safe_get(data, ["a", "x", "y"], default=0)</code> → 0`, answer: `def safe_get(data, keys, default=None):
    try:
        result = data
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError, IndexError):
        return default
data = {"a": {"b": {"c": 42}}}
print(safe_get(data, ["a", "b", "c"]))
print(safe_get(data, ["a", "x", "y"]))` },
      { title: "健壮日志读取器（挑战）", desc: `函数名: <code>safe_read_logs(filepath)</code><br>要求:<br>- 文件不存在 → 返回空列表 + print 提示<br>- 每行解析失败 → 跳过该行 + print 警告<br>- 成功 → 返回解析后的字典列表`, answer: `def safe_read_logs(filepath):
    result = []
    try:
        with open(filepath, "r") as f:
            for i, line in enumerate(f, 1):
                try:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        result.append({"time": parts[1], "level": parts[2], "msg": " ".join(parts[3:])})
                except Exception:
                    print(f"警告: 第 {i} 行解析失败，已跳过")
    except FileNotFoundError:
        print(f"日志文件不存在: {filepath}")
    return result`
      }
    ]
  },
  {
    id: 10, title: "模块和 import", icon: "D10",
    tag: "进阶", tagClass: "amber",
    desc: "能用标准库和第三方库，能组织自己的代码",
    sections: [
      {
        title: "什么是模块？",
        content: `<div class="text-block">模块就是一个 <code>.py</code> 文件。你写的 <code>day01.py</code> 就是一个模块。<code>import</code> 就是把别的模块里的功能拿过来用。</div>
<div class="tip-box info"><p><strong>简单理解：</strong>模块 = 一个 .py 文件，import = 把别人的代码拿过来用。</p></div>` },
{
        title: "导入方式",
        content: `<div class="table-wrap"><table><tr><th>方式</th><th>写法</th><th>使用</th></tr>
<tr><td>导入整个模块</td><td><code>import os</code></td><td><code>os.getcwd()</code></td></tr>
<tr><td>起别名</td><td><code>import json as j</code></td><td><code>j.loads()</code></td></tr>
<tr><td>导入特定功能</td><td><code>from datetime import datetime</code></td><td><code>datetime.now()</code></td></tr>
<tr><td>导入多个</td><td><code>from collections import Counter, defaultdict</code></td><td>直接用名字</td></tr></table></div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import os
print(os.getcwd())              # 当前工作目录

import json as j
print(type(j))                  # &lt;class 'module'>

from datetime import datetime, timedelta
print(datetime.now())           # 当前时间</code></pre></div>
<div class="tip-box danger"><p><strong>避免</strong> <code>from os.path import *</code>，容易命名冲突。</p></div>`
      },
      {
        title: "os 模块 — 操作系统交互",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import os

# 路径操作
print(f"当前目录: {os.getcwd()}")
print(f"文件存在: {os.path.exists('day01.py')}")
print(f"是文件: {os.path.isfile('day01.py')}")
print(f"是目录: {os.path.isdir('.')}")

# 路径拼接（跨平台安全）
config_path = os.path.join("config", "model", "qwen.json")
print(f"拼接路径: {config_path}")

# 文件名拆分
filepath = "/data/python/day10.py"
print(f"目录: {os.path.dirname(filepath)}")
print(f"文件名: {os.path.basename(filepath)}")
print(f"扩展名: {os.path.splitext(filepath)}")

# 环境变量
print(f"HOME: {os.environ.get('HOME', '未设置')}")

# 创建和删除
os.makedirs("test_dir/sub", exist_ok=True)</code></pre></div>`
      },
      {
        title: "sys 模块 — Python 系统相关",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import sys

print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")
print(f"平台: {sys.platform}")
print(f"搜索路径: {sys.path[:3]}")  # 模块搜索路径

# 命令行参数
print(f"脚本名: {sys.argv[0]}")</code></pre></div>`
      },
      {
        title: "subprocess — 执行系统命令",
        content: `<div class="text-block">比 <code>os.popen</code> 更安全、更强大，是执行外部命令的推荐方式。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import subprocess

# 执行命令并获取输出
result = subprocess.run(
    ["echo", "Hello from subprocess"],
    capture_output=True,
    text=True
)
print(f"输出: {result.stdout.strip()}")
print(f"返回码: {result.returncode}")

# 检查命令是否存在
def command_exists(cmd):
    try:
        subprocess.run(["which", cmd], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

print(f"python3 存在: {command_exists('python3')}")
print(f"nvidia-smi 存在: {command_exists('nvidia-smi')}")</code></pre></div>`
      },
      {
        title: "json 模块详解",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import json

config = {"model": "qwen-72b", "port": 8000, "gpu": [0, 1, 2, 3]}

# Python 对象 → JSON 字符串
json_str = json.dumps(config, indent=2)
print(f"JSON 字符串:\n{json_str}")

# JSON 字符串 → Python 对象
parsed = json.loads(json_str)
print(f"解析后: {parsed['model']}")

# 直接读写 JSON 文件
with open("test_config.json", "w") as f:
    json.dump(config, f, indent=2)

with open("test_config.json", "r") as f:
    loaded = json.load(f)
print(f"从文件读取: {loaded}")</code></pre></div>`
      },
      {
        title: "datetime — 时间处理",
        content: `<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">from datetime import datetime, timedelta

# 当前时间
now = datetime.now()
print(f"现在: {now}")
print(f"格式化: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 时间计算
one_hour_later = now + timedelta(hours=1)
print(f"一小时后: {one_hour_later}")

yesterday = now - timedelta(days=1)
print(f"昨天: {yesterday.strftime('%Y-%m-%d')}")

# 解析时间字符串
log_time = datetime.strptime("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
print(f"解析时间: {log_time}")

# 计算时间差
start = datetime.strptime("2024-01-15 10:00:00", "%Y-%m-%d %H:%M:%S")
end = datetime.strptime("2024-01-15 10:05:30", "%Y-%m-%d %H:%M:%S")
diff = end - start
print(f"耗时: {diff.total_seconds()} 秒")</code></pre></div>`
      },
      {
        title: "collections — 特殊容器",
        content: `<div class="text-block"><code>Counter</code> 计数器和 <code>defaultdict</code> 带默认值的字典，是处理统计数据的利器。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">from collections import Counter, defaultdict

# Counter: 计数器（统计日志级别超方便）
logs = ["INFO", "ERROR", "WARN", "INFO", "ERROR", "INFO", "DEBUG", "ERROR"]
counts = Counter(logs)
print(f"日志统计: {counts}")
print(f"最常见的2个: {counts.most_common(2)}")

# defaultdict: 带默认值的字典（避免 KeyError）
server_logs = defaultdict(list)
for i, level in enumerate(logs):
    server_logs[level].append(i)
print(f"ERROR 出现在: {server_logs['ERROR']}")</code></pre></div>`
      },
      {
        title: "pathlib — 更优雅的路径操作",
        content: `<div class="text-block"><code>pathlib</code> 是比 <code>os.path</code> 更现代、更直观的路径操作模块。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">from pathlib import Path

p = Path("/data/python")
print(f"路径: {p}")
print(f"是否存在: {p.exists()}")
print(f"是目录: {p.is_dir()}")

# 列出所有 .py 文件
py_files = list(p.glob("*.py"))
print(f"\nPython 文件 ({len(py_files)} 个):")
for f in sorted(py_files):
    size = f.stat().st_size
    print(f"  {f.name} ({size:,} 字节)")

# 拼接路径（比 os.path.join 更直观）
config_file = p / "config" / "model.json"
print(f"\n配置路径: {config_file}")</code></pre></div>
<div class="tip-box success"><p><strong>推荐：</strong>新项目优先用 <code>pathlib</code>，比 <code>os.path</code> 更直观。用 <code>/</code> 拼接路径很优雅。</p></div>`
      },
      {
        title: "常用第三方库",
        content: `<div class="table-wrap"><table><tr><th>包名</th><th>安装</th><th>用途</th></tr>
<tr><td>requests</td><td><code>pip install requests</code></td><td>HTTP请求，调API</td></tr>
<tr><td>paramiko</td><td><code>pip install paramiko</code></td><td>SSH远程连接</td></tr>
<tr><td>psutil</td><td><code>pip install psutil</code></td><td>系统信息监控</td></tr>
<tr><td>pandas</td><td><code>pip install pandas</code></td><td>数据分析</td></tr>
<tr><td>fastapi</td><td><code>pip install fastapi</code></td><td>写API接口</td></tr>
<tr><td>docker</td><td><code>pip install docker</code></td><td>操作Docker容器</td></tr></table></div>`
      },
      {
        title: "实战：综合工具脚本",
        content: `<div class="text-block">综合运用多个标准库模块，写一个系统信息收集工具。</div>
<div class="code-block"><div class="code-header"><span class="lang-label">python</span><button class="copy-btn" onclick="copyCode(this)">Copy</button></div><pre><code class="language-python">import sys, os, json
from datetime import datetime
from pathlib import Path
from collections import Counter

def system_info():
    """收集系统信息"""
    info = {
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Python版本": sys.version.split()[0],
        "平台": sys.platform,
        "当前目录": os.getcwd(),
    }
    project_dir = Path(".")
    py_count = len(list(project_dir.glob("day*.py")))
    info["练习文件数"] = py_count
    return info

def print_report(info):
    """格式化打印报告"""
    print("\n=== 系统信息 ===")
    for key, value in info.items():
        print(f"  {key}: {value}")

info = system_info()
print_report(info)</code></pre></div>`
      }
    ],
    exercises: [
      { title: "查找日志文件", desc: `输入: 目录路径<br>返回: 文件路径列表<br>提示: 用 pathlib.Path.<code>glob()</code>`, answer: `def find_log_files(directory):
    return sorted(Path(directory).glob("*.log"))
for f in find_log_files("."):
    print(f.name)` },
      { title: "词频统计", desc: `输入: 文件路径<br>返回: Counter 对象<br>提示: 用 Counter + <code>split()</code>`, answer: `def word_count(filepath):
    try:
        with open(filepath, "r") as f:
            words = f.read().split()
            return Counter(words)
    except FileNotFoundError:
        print(f"文件不存在: {filepath}")
        return Counter()` },
      { title: "配置管理器（挑战）", desc: `功能: 读取 JSON 配置、更新配置、保存配置<br>要求: 异常处理、文件不存在时使用默认配置`, answer: `class ConfigManager:
    def __init__(self, filepath, default=None):
        self.filepath = filepath
        self.config = default or {}
        self.load()
    def load(self):
        try:
            with open(self.filepath, "r") as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    def get(self, key, default=None):
        return self.config.get(key, default)
    def set(self, key, value):
        self.config[key] = value
    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.config, f, indent=2)
    def __str__(self):
        return json.dumps(self.config, indent=2, ensure_ascii=False)`
      }
    ]
  }
]


// ====== State ======
let completed = JSON.parse(localStorage.getItem('py_progress') || '{}');

function saveProgress() {
  localStorage.setItem('py_progress', JSON.stringify(completed));
  updateProgress();
}

function updateProgress() {
  const done = Object.keys(completed).filter(k => !k.includes('_') && completed[k]).length;
  const pct = Math.round(done / 10 * 100);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressText').textContent = `已完成 ${done}/10 天`;
  document.getElementById('progressPct').textContent = pct + '%';
  document.querySelectorAll('.nav-item').forEach(el => {
    const id = parseInt(el.dataset.id);
    const icon = el.querySelector('.nav-icon');
    if (completed[id]) {
      icon.className = 'nav-icon done';
      icon.textContent = '✓';
    } else if (id === getCurrentDay()) {
      icon.className = 'nav-icon current';
      icon.textContent = courses.find(c=>c.id===id).icon;
    } else {
      icon.className = 'nav-icon pending';
      icon.textContent = courses.find(c=>c.id===id).icon;
    }
  });
}

function getCurrentDay() {
  for (let i = 1; i <= 10; i++) {
    if (!completed[i]) return i;
  }
  return 10;
}

// ====== Render Nav ======
function renderNav() {
  const nav = document.getElementById('navList');
  let html = '<div class="nav-section">基础阶段</div>';
  courses.forEach(c => {
    if (c.id === 5) html += '<div class="nav-section">核心阶段</div>';
    if (c.id === 9) html += '<div class="nav-section">进阶阶段</div>';
    const isActive = c.id === getCurrentDay() ? 'active' : '';
    html += `<div class="nav-item ${isActive}" data-id="${c.id}" onclick="loadDay(${c.id})">
      <span class="nav-icon pending">${c.icon}</span>
      <span class="nav-label">Day ${c.id} ${c.title}</span>
      <span class="nav-badge">${c.tag}</span>
    </div>`;
  });
  nav.innerHTML = html;
}

// ====== Render Content ======
function loadDay(id) {
  const c = courses.find(x => x.id === id);
  if (!c) return;

  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', parseInt(el.dataset.id) === id);
  });

  let html = `<div class="content-header">
    <div class="header-tags">
      <span class="header-tag ${c.tagClass}">Day ${c.id}</span>
      <span class="header-tag ${c.tagClass}">${c.tag}</span>
    </div>
    <h2>${c.title}</h2>
    <p class="desc">${c.desc}</p>
  </div>`;

  c.sections.forEach((s, i) => {
    html += `<div class="section">
      <h3 class="section-title"><span class="section-num">${i+1}</span> ${s.title}</h3>
      ${s.content}
    </div>`;
  });

  if (c.exercises.length) {
    html += `<div class="section"><h3 class="section-title"><span class="section-num" style="background:var(--warning);">✎</span> 练习</h3>`;
    c.exercises.forEach((ex, i) => {
      html += `<div class="exercise-box">
        <h4>练习 ${i+1}: ${ex.title}</h4>
        <p>${ex.desc}</p>
        <div class="code-editor">
          <textarea class="editor-textarea" id="editor-${id}-${i}" style="display:none" spellcheck="false">${(ex.starter || '').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</textarea>
          <div class="cm-wrapper" id="cm-${id}-${i}"></div>
          <div class="editor-actions">
            <button class="run-btn" onclick="runEditorCode(${id}, ${i}, this)">▶ 运行</button>
            <button class="reset-btn" onclick="resetCode(${id}, ${i}, this)" title="重置为初始代码">↺ 重置</button>
            <span class="shortcut-hint">Ctrl+Enter</span>
          </div>
          <div class="editor-output" id="output-${id}-${i}"></div>
        </div>
        <hr class="exercise-divider">
        <div class="answer-section" id="answer-${id}-${i}" style="display:none;">
          <div class="answer-header">参考答案</div>
          <pre><code class="language-python">${(ex.answer || '').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>
        </div>
        <div class="exercise-bottom-actions">
          <button class="answer-btn" onclick="toggleAnswer(${id}, ${i}, this)">
            👁 参考答案
          </button>
          <button class="check-btn ${completed[`${id}_${i}`] ? 'checked' : 'unchecked'}"
            onclick="toggleExercise(${id}, ${i}, this)">
            ${completed[`${id}_${i}`] ? '✓ 已完成' : '标记完成'}
          </button>
        </div>
      </div>`;
    });
    html += `</div>`;
  }

  html += `<div class="nav-buttons">`;
  html += id > 1 ? `<button class="nav-btn secondary" onclick="loadDay(${id-1})">← Day ${id-1}</button>` : '<div></div>';
  html += id < 10 ? `<button class="nav-btn primary" onclick="loadDay(${id+1})">Day ${id+1} →</button>` : '<div></div>';
  html += `</div>`;

  document.getElementById('mainContent').innerHTML = `<div class="main-inner">${html}</div>`;
  document.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
  // Restore saved code from localStorage
  c.exercises.forEach((ex, i) => {
    const editor = document.getElementById(`editor-${id}-${i}`);
    if (editor) {
      const saved = localStorage.getItem(`py_code_${id}_${i}`);
      if (saved !== null) editor.value = saved;
    }
  });
  // Initialize CodeMirror editors
  c.exercises.forEach((ex, i) => {
    const ta = document.getElementById(`editor-${id}-${i}`);
    const wrapper = document.getElementById(`cm-${id}-${i}`);
    if (ta && wrapper) {
      const cm = CodeMirror(wrapper, {
        value: ta.value || ex.starter || '',
        mode: 'python',
        lineNumbers: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        extraKeys: {
          'Ctrl-Enter': () => {
            const container = wrapper.closest('.code-editor');
            const btn = container.querySelector('.run-btn');
            if (btn) runEditorCode(id, i, btn);
          },
          'Cmd-Enter': () => {
            const container = wrapper.closest('.code-editor');
            const btn = container.querySelector('.run-btn');
            if (btn) runEditorCode(id, i, btn);
          },
          'Tab': (cm) => cm.replaceSelection('    ', 'end'),
        }
      });
      // Keep hidden textarea in sync and auto-save on change
      cm.on('change', () => {
        ta.value = cm.getValue();
      });
      // Auto-save on change (debounced)
      let timer;
      cm.on('change', () => {
        clearTimeout(timer);
        timer = setTimeout(() => localStorage.setItem(`py_code_${id}_${i}`, ta.value), 500);
      });
      // Store reference
      ta._codemirror = cm;
    }
  });
  document.getElementById('mainContent').scrollTop = 0;
}

function toggleExercise(dayId, exIdx, btn) {
  const key = `${dayId}_${exIdx}`;
  completed[key] = !completed[key];
  btn.className = `check-btn ${completed[key] ? 'checked' : 'unchecked'}`;
  btn.textContent = completed[key] ? '✓ 已完成' : '标记完成';

  const c = courses.find(x => x.id === dayId);
  const allDone = c.exercises.every((_, i) => completed[`${dayId}_${i}`]);
  completed[dayId] = allDone;
  saveProgress();
}

function copyCode(btn) {
  const code = btn.closest('.code-block').querySelector('code').textContent;
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(code).then(() => {
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = 'Copy', 1500);
    });
  } else {
    const ta = document.createElement('textarea');
    ta.value = code;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
  }
}

// ====== Server-side Python Execution ======
async function runEditorCode(dayId, exIdx, btn) {
  const editor = document.getElementById(`editor-${dayId}-${exIdx}`);
  const output = document.getElementById(`output-${dayId}-${exIdx}`);
  const code = editor.value.trim();

  if (!code) {
    output.innerHTML = '<span class="system">请先写点代码再运行</span>';
    output.classList.add('visible');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> 运行中...';

  try {
    const resp = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const result = await resp.json();

    let html = '';
    if (result.stdout) html += `<span class="stdout">${escapeHtml(result.stdout)}</span>`;
    if (result.stderr) html += `<span class="stderr">${escapeHtml(result.stderr)}</span>`;
    if (!result.stdout && !result.stderr) html += '<span class="system">（代码运行完毕，无输出）</span>';

    output.innerHTML = html;
    output.classList.add('visible');
  } catch (e) {
    output.innerHTML = `<span class="stderr">连接服务器失败: ${e.message}</span>`;
    output.classList.add('visible');
  }

  btn.disabled = false;
  btn.innerHTML = '▶ 运行';
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Tab key support for textareas
document.addEventListener('keydown', function(e) {
  if (e.target.classList.contains('editor-textarea') && e.key === 'Tab') {
    e.preventDefault();
    const start = e.target.selectionStart;
    const end = e.target.selectionEnd;
    e.target.value = e.target.value.substring(0, start) + '    ' + e.target.value.substring(end);
    e.target.selectionStart = e.target.selectionEnd = start + 4;
  }
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    // Find the run button for this editor
    const match = e.target.id.match(/editor-(\d+)-(\d+)/);
    if (match) {
      const [, dayId, exIdx] = match;
      const container = e.target.closest('.code-editor');
      const btn = container.querySelector('.run-btn');
      if (btn) runEditorCode(parseInt(dayId), parseInt(exIdx), btn);
    }
  }
});


function toggleAnswer(dayId, exIdx, btn) {
  const el = document.getElementById(`answer-${dayId}-${exIdx}`);
  if (el.style.display === 'none') {
    el.style.display = 'block';
    btn.textContent = '👁 隐藏答案';
    // Highlight the code
    el.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));
  } else {
    el.style.display = 'none';
    btn.textContent = '👁 参考答案';
  }
}

function resetCode(dayId, exIdx) {
  const editor = document.getElementById(`editor-${dayId}-${exIdx}`);
  const c = courses.find(x => x.id === dayId);
  const starter = c.exercises[exIdx].starter || '';
  editor.value = starter;
  localStorage.removeItem(`py_code_${dayId}_${exIdx}`);
  // Update CodeMirror if exists
  if (editor._codemirror) editor._codemirror.setValue(starter);
}

// ====== Init ======
renderNav();
updateProgress();
