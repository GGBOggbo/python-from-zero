# ============================================================
# Day 03: 列表 List
# 目标：能管理一组服务器、一批日志、一组配置
# 用法：python day03.py
# ============================================================

# --------------------------------------------------
# 1. 创建列表
# --------------------------------------------------

# 列表用方括号 []，元素用逗号隔开
servers = ["gpu-01", "gpu-02", "gpu-03"]
ports = [8000, 8080, 9000]
mixed = ["gpu-01", 8000, True, 87.5]   # 一个列表里可以放不同类型（但不推荐）

# 空列表
empty1 = []
empty2 = list()

print(servers)
print(type(servers))           # <class 'list'>

# --------------------------------------------------
# 2. 索引和切片（和字符串一模一样的规则）
# --------------------------------------------------
#         0       1       2       3       4
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
print(gpus[::-1])           # ['gpu-05', 'gpu-04', ...]（反序）

# --------------------------------------------------
# 3. 增 —— 往列表里加东西
# --------------------------------------------------
servers = ["gpu-01", "gpu-02", "gpu-03"]

# append: 末尾加一个
servers.append("gpu-04")
print(servers)              # [..., "gpu-04"]

# insert: 指定位置插入
servers.insert(1, "cpu-01")              # 在第2个位置插入
print(servers)              # ["gpu-01", "cpu-01", "gpu-02", ...]

# extend: 批量加（合并另一个列表）
servers.extend(["gpu-05", "gpu-06"])
print(servers)

# + 号也能合并（生成新列表，不改动原来的）
new_servers = servers + ["gpu-07", "gpu-08"]
print(new_servers)

# --------------------------------------------------
# 4. 删 —— 从列表里去掉东西
# --------------------------------------------------
servers = ["gpu-01", "cpu-01", "gpu-02", "gpu-03", "gpu-04", "gpu-05", "gpu-06"]

# remove: 按值删（删第一个匹配的）
servers.remove("cpu-01")
print(servers)              # cpu-01 没了

# pop: 按位置删，并返回被删的值
removed = servers.pop()     # 不填位置 = 删最后一个
print(f"被删掉的是: {removed}")
print(servers)

removed2 = servers.pop(0)   # 删第一个
print(f"被删掉的是: {removed2}")

# del: 按位置删（不需要返回值）
del servers[0]
print(servers)

# clear: 清空整个列表
backup = servers.copy()     # 先备份一份
servers.clear()
print(f"清空后: {servers}")
print(f"备份: {backup}")

# --------------------------------------------------
# 5. 改 —— 直接赋值
# --------------------------------------------------
servers = ["gpu-01", "gpu-02", "gpu-03"]

# 按下标改
servers[0] = "gpu-new-01"
print(servers)              # ["gpu-new-01", "gpu-02", "gpu-03"]

# 切片赋值（批量改）
servers[1:3] = ["gpu-new-02", "gpu-new-03", "gpu-new-04"]
print(servers)              # 2个位置塞了3个元素，列表会变长

# --------------------------------------------------
# 6. 查 —— 查找和统计
# --------------------------------------------------
servers = ["gpu-01", "gpu-02", "gpu-03", "gpu-01"]

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
    print(f"{target} 不在列表中")

# --------------------------------------------------
# 7. 排序和反转
# --------------------------------------------------

nums = [3, 1, 4, 1, 5, 9, 2, 6]
names = ["gpu-03", "gpu-01", "gpu-10", "gpu-02"]

# sort: 原地排序（改的是自己）
nums.sort()
print(nums)                  # [1, 1, 2, 3, 4, 5, 6, 9]

nums.sort(reverse=True)
print(nums)                  # [9, 6, 5, 4, 3, 2, 1, 1]

names.sort()
print(names)                 # 字符串按字母排 → ['gpu-01', 'gpu-02', 'gpu-03', 'gpu-10']

# sorted: 排序但返回新列表，不改原来的
original = [3, 1, 4]
sorted_copy = sorted(original)
print(f"原列表: {original}")       # [3, 1, 4]（没变）
print(f"排序后: {sorted_copy}")    # [1, 3, 4]

# reverse: 反转
nums = [1, 2, 3, 4, 5]
nums.reverse()
print(nums)                  # [5, 4, 3, 2, 1]

# --------------------------------------------------
# 8. 列表推导式（进阶，先了解）
# --------------------------------------------------
# 把一个列表变成另一个列表的快捷写法

# 普通写法：给每个服务器加前缀
servers = ["01", "02", "03"]
result = []
for s in servers:
    result.append("gpu-" + s)
print(result)                # ['gpu-01', 'gpu-02', 'gpu-03']

# 推导式：一行搞定，效果一样
result2 = ["gpu-" + s for s in servers]
print(result2)               # ['gpu-01', 'gpu-02', 'gpu-03']

# 带条件过滤：只保留偶数端口
ports = [8000, 8001, 8080, 8081, 9000]
even_ports = [p for p in ports if p % 2 == 0]
print(even_ports)            # [8000, 8080, 9000]

# --------------------------------------------------
# 9. 常用技巧
# --------------------------------------------------

# enumerate: 同时拿到索引和值
servers = ["gpu-01", "gpu-02", "gpu-03"]
for i, name in enumerate(servers):
    print(f"第 {i} 台: {name}")

# zip: 两个列表配对
servers = ["gpu-01", "gpu-02", "gpu-03"]
temps = [72, 85, 78]
for server, temp in zip(servers, temps):
    print(f"{server}: {temp}°C")

# join: 列表转字符串（昨天学的，这里再强化一下）
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
print(c)        # [1, 2, 3]（c 没变）

# --------------------------------------------------
# 10. 实战：服务器状态管理
# --------------------------------------------------
# 模拟一个简单的服务器状态管理

all_servers = ["gpu-01", "gpu-02", "gpu-03", "gpu-04", "gpu-05"]
online = ["gpu-01", "gpu-03", "gpu-05"]
warning = ["gpu-03"]               # gpu-03 温度偏高
offline = ["gpu-02", "gpu-04"]

print("=== 服务器状态总览 ===")
print(f"总数: {len(all_servers)} 台")
print(f"在线: {len(online)} 台 → {', '.join(online)}")
print(f"告警: {len(warning)} 台 → {', '.join(warning)}")
print(f"离线: {len(offline)} 台 → {', '.join(offline)}")
print()

# 模拟操作：gpu-02 恢复上线
offline.remove("gpu-02")
online.append("gpu-02")
print(">>> gpu-02 已恢复上线")
print(f"在线: {', '.join(online)}")
print(f"离线: {', '.join(offline)}")
print()

# 模拟操作：新增 gpu-06
all_servers.append("gpu-06")
online.append("gpu-06")
print(">>> gpu-06 已加入集群")
print(f"总数: {len(all_servers)} 台")
print(f"在线: {', '.join(online)}")

# 找出正常的服务器（在线但不在告警列表中）
normal = [s for s in online if s not in warning]
print(f"正常: {', '.join(normal)}")

# --------------------------------------------------
# 11. 练习
# --------------------------------------------------

# 练习1：管理 GPU 集群
# 给定初始列表，完成以下操作，每步都 print 验证
gpus = ["gpu-01", "gpu-02", "gpu-03"]
# 1. 末尾加 gpu-04
# 2. 在第1个位置插入 gpu-00
# 3. 把 gpu-02 改成 gpu-02-new
# 4. 删掉 gpu-03
# 最终期望: ['gpu-00', 'gpu-01', 'gpu-02-new', 'gpu-04']

# ====== 在这里写你的代码 ======



# 练习2：日志级别过滤
log_levels = ["INFO", "ERROR", "WARN", "INFO", "ERROR", "INFO", "DEBUG", "ERROR"]
# 1. 统计每个级别出现几次
# 2. 只保留 ERROR 和 WARN（用列表推导式）
# 3. 按字母排序

# ====== 在这里写你的代码 ======



# 练习3（挑战）：两个列表交叉合并
names = ["gpu-01", "gpu-02", "gpu-03"]
temps = [72, 85, 78]
# 期望输出: ["gpu-01: 72°C", "gpu-02: 85°C", "gpu-03: 78°C"]
# 提示：用 zip + 列表推导式

# ====== 在这里写你的代码 ======



# --------------------------------------------------
# 练习1 参考答案
# --------------------------------------------------
# gpus = ["gpu-01", "gpu-02", "gpu-03"]
# gpus.append("gpu-04")
# gpus.insert(0, "gpu-00")
# gpus[2] = "gpu-02-new"
# gpus.remove("gpu-03")
# print(gpus)

# --------------------------------------------------
# 练习2 参考答案
# --------------------------------------------------
# log_levels = ["INFO", "ERROR", "WARN", "INFO", "ERROR", "INFO", "DEBUG", "ERROR"]
# print(f"INFO: {log_levels.count('INFO')}")
# print(f"ERROR: {log_levels.count('ERROR')}")
# print(f"WARN: {log_levels.count('WARN')}")
# print(f"DEBUG: {log_levels.count('DEBUG')}")
# errors_and_warns = [l for l in log_levels if l in ("ERROR", "WARN")]
# errors_and_warns.sort()
# print(errors_and_warns)

# --------------------------------------------------
# 练习3 参考答案
# --------------------------------------------------
# names = ["gpu-01", "gpu-02", "gpu-03"]
# temps = [72, 85, 78]
# result = [f"{name}: {temp}°C" for name, temp in zip(names, temps)]
# print(result)
