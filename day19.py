# ============================================================
# Day 19: 告警推送 — 企业微信/钉钉 webhook
# 目标：能通过 Python 发送告警消息到企业微信和钉钉
# 用法：python day19.py 逐段运行，改一改，看看结果变不变
# ============================================================

import requests
import json
import time
from datetime import datetime

# --------------------------------------------------
# 1. Webhook 基础概念
# --------------------------------------------------
# Webhook = 一个 URL，往它发 POST 请求就能发消息
# 不需要登录 App，一条 HTTP 请求搞定

# 企业微信和钉钉都支持"自定义机器人" Webhook
# 创建步骤：
# 1. 群设置 → 添加机器人 → 自定义机器人
# 2. 获得 Webhook URL
# 3. 用 requests.post() 发消息

# 通用发送函数
def send_webhook(url, data):
    """发送 Webhook 消息"""
    try:
        resp = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        result = resp.json()
        if resp.status_code == 200:
            print(f"发送成功: {result}")
            return True
        else:
            print(f"发送失败: {result}")
            return False
    except Exception as e:
        print(f"发送异常: {e}")
        return False

# --------------------------------------------------
# 2. 钉钉 Webhook
# --------------------------------------------------
# 钉钉机器人 Webhook URL 格式：
# https://oapi.dingtalk.com/robot/send?access_token=xxx

DINGTALK_URL = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"

# 发送文本消息
def dingtalk_text(content, at_all=False):
    """发送钉钉文本消息"""
    data = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"isAtAll": at_all}
    }
    # 取消注释发送真实消息
    # return send_webhook(DINGTALK_URL, data)
    print(f"[模拟] 钉钉文本: {content}")

# 发送 Markdown 消息
def dingtalk_markdown(title, text):
    """发送钉钉 Markdown 消息"""
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text,
        }
    }
    # return send_webhook(DINGTALK_URL, data)
    print(f"[模拟] 钉钉 Markdown: {title}")

# 钉钉 Markdown 示例
alert_md = """## GPU 告警

**服务器**: gpu-01
**GPU**: #0
**温度**: 92°C
**阈值**: 85°C

> 请及时处理！
"""
# dingtalk_markdown("GPU 告警", alert_md)

# --------------------------------------------------
# 3. 企业微信 Webhook
# --------------------------------------------------
# 企业微信机器人 Webhook URL 格式：
# https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx

WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

# 发送文本消息
def wechat_text(content, mentioned_list=None):
    """发送企业微信文本消息"""
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": mentioned_list or [],
        }
    }
    # return send_webhook(WECHAT_URL, data)
    print(f"[模拟] 企业微信文本: {content}")

# 发送 Markdown 消息
def wechat_markdown(content):
    """发送企业微信 Markdown 消息"""
    data = {
        "msgtype": "markdown",
        "markdown": {"content": content}
    }
    # return send_webhook(WECHAT_URL, data)
    print(f"[模拟] 企业微信 Markdown")

# --------------------------------------------------
# 4. 告警消息模板
# --------------------------------------------------

def format_gpu_alert(host, gpu_index, temperature, threshold=85):
    """格式化 GPU 温度告警"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 文本格式（简单）
    text = f"[GPU告警] {host} GPU#{gpu_index} 温度 {temperature}°C，超过阈值 {threshold}°C ({now})"

    # Markdown 格式（好看）
    md = f"""## GPU 温度告警
> 时间: {now}

**服务器**: {host}
**GPU**: #{gpu_index}
**当前温度**: <font color="warning">{temperature}°C</font>
**告警阈值**: {threshold}°C

请及时检查散热情况！"""

    return text, md

def format_service_alert(service_name, status, error_msg=""):
    """格式化服务状态告警"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"[服务告警] {service_name} 状态异常: {status} ({now})"
    if error_msg:
        text += f"\n错误信息: {error_msg}"
    return text

# --------------------------------------------------
# 5. 实际场景：监控 + 告警
# --------------------------------------------------

class AlertSender:
    """告警发送器"""

    def __init__(self, dingtalk_url=None, wechat_url=None):
        self.dingtalk_url = dingtalk_url
        self.wechat_url = wechat_url
        self.alert_count = 0
        self.cooldown = {}  # 防止频繁告警

    def send_alert(self, title, content, alert_type="warning"):
        """发送告警（带冷却）"""
        now = time.time()

        # 冷却机制：同一告警 5 分钟内不重复发送
        key = title
        if key in self.cooldown and now - self.cooldown[key] < 300:
            print(f"[冷却中] {title}")
            return False

        self.cooldown[key] = now
        self.alert_count += 1

        # 发送到所有配置的渠道
        if self.dingtalk_url:
            dingtalk_text(content)
        if self.wechat_url:
            wechat_text(content)

        print(f"[告警已发送 #{self.alert_count}] {title}")
        return True

    def send_gpu_alert(self, host, gpu_index, temperature, threshold=85):
        """发送 GPU 温度告警"""
        if temperature >= threshold:
            text, md = format_gpu_alert(host, gpu_index, temperature, threshold)
            return self.send_alert(f"GPU告警-{host}-#{gpu_index}", text)

    def send_service_alert(self, service_name, status, error=""):
        """发送服务状态告警"""
        text = format_service_alert(service_name, status, error)
        return self.send_alert(f"服务告警-{service_name}", text)

# 使用示例
alerter = AlertSender()  # 不传 URL 则只打印模拟消息
alerter.send_gpu_alert("gpu-01", 0, 92, threshold=85)
alerter.send_service_alert("vllm-qwen", "stopped", "容器意外退出")

# --------------------------------------------------
# 6. 小练习（先自己写，写不出再看下面的参考答案）
# --------------------------------------------------

# 练习1：发送钉钉文本告警
# 封装函数，发送包含服务器名、告警内容的文本消息

# ====== 在这里写你的代码 ======




# 练习2：发送格式化 GPU 告警
# 生成 Markdown 格式的 GPU 告警消息

# ====== 在这里写你的代码 ======




# 练习3：带冷却机制的告警器
# 同一告警 5 分钟内不重复发送

# ====== 在这里写你的代码 ======




# --------------------------------------------------
# 练习1 参考答案（先自己写！）
# --------------------------------------------------
# import requests
#
# def send_dingtalk_alert(url, server, message):
#     data = {
#         "msgtype": "text",
#         "text": {"content": f"[运维告警] {server}: {message}"}
#     }
#     try:
#         resp = requests.post(url, json=data, timeout=10)
#         return resp.json().get("errcode") == 0
#     except Exception as e:
#         print(f"发送失败: {e}")
#         return False

# --------------------------------------------------
# 练习2 参考答案（先自己写！）
# --------------------------------------------------
# from datetime import datetime
#
# def gpu_alert_markdown(host, gpu_id, temp, threshold=85):
#     now = datetime.now().strftime("%Y-%m-%d %H:%M")
#     md = f"""## GPU 温度告警
# > {now}
#
# **服务器**: {host}
# **GPU**: #{gpu_id}
# **温度**: {temp}°C (阈值: {threshold}°C)
# """
#     data = {
#         "msgtype": "markdown",
#         "markdown": {"title": f"GPU告警-{host}", "text": md}
#     }
#     return data

# --------------------------------------------------
# 练习3 参考答案（先自己写！）
# --------------------------------------------------
# import time
#
# class CooldownAlerter:
#     def __init__(self, cooldown_seconds=300):
#         self.cooldown_seconds = cooldown_seconds
#         self.last_alert = {}
#
#     def send(self, alert_key, message):
#         now = time.time()
#         if alert_key in self.last_alert:
#             if now - self.last_alert[alert_key] < self.cooldown_seconds:
#                 remaining = int(self.cooldown_seconds - (now - self.last_alert[alert_key]))
#                 print(f"[冷却] {alert_key} 还需 {remaining} 秒")
#                 return False
#         self.last_alert[alert_key] = now
#         print(f"[发送] {message}")
#         return True
#
# alerter = CooldownAlerter(cooldown_seconds=300)
# alerter.send("gpu-01-temp", "GPU 温度过高: 92°C")
# alerter.send("gpu-01-temp", "GPU 温度过高: 93°C")  # 冷却中，不会发送
