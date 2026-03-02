# WhatsApp配置指南

> OpenClaw WhatsApp Business API 配置教程

---

## 概述

WhatsApp Business API 允许企业通过编程方式发送和接收消息。需要通过 Meta 开发者平台申请访问权限，并完成企业验证。

---

## 前提条件

在开始配置前，请确保满足以下条件：

- [ ] Meta 开发者账号
- [ ] Facebook Business 账号
- [ ] 有效的商业电话号码（未注册 WhatsApp）
- [ ] 企业营业执照或相关证明文件
- [ ] 企业网站（可访问）

---

## 配置步骤

### 1. 创建 Meta 应用

#### 步骤 1.1：访问 Meta 开发者平台

1. 打开 [Meta for Developers](https://developers.facebook.com/)
2. 使用 Facebook 账号登录

#### 步骤 1.2：创建应用

1. 点击「我的应用」→「创建应用」
2. 选择应用类型：「商务」（Business）
3. 填写应用信息：
   - 应用显示名称：如 `OpenClaw`
   - 应用联系邮箱
   - 关联的商务管理平台账号（Business Manager）
4. 点击「创建应用」

#### 步骤 1.3：添加 WhatsApp 产品

1. 在应用仪表板，点击「添加产品」
2. 找到「WhatsApp」并点击「设置」

### 2. 完成企业验证

企业验证是使用 WhatsApp Business API 的必要步骤。

#### 步骤 2.1：开始企业验证

1. 在应用左侧菜单选择「设置」→「基本」
2. 找到「企业验证」部分，点击「开始验证」

#### 步骤 2.2：提供企业信息

填写以下信息：

| 信息项 | 说明 |
|--------|------|
| 企业法定名称 | 与营业执照完全一致 |
| 企业注册地址 | 详细地址 |
| 企业网站 | 可访问的官方网站 |
| 企业邮箱 | 企业域名邮箱优先 |
| 营业执照 | 清晰的扫描件或照片 |

#### 步骤 2.3：等待审核

- 审核时间：通常 1-5 个工作日
- 状态查询：在「设置」→「基本」页面查看
- 如被拒绝，根据反馈修改后重新提交

### 3. 设置 WhatsApp 商业账号

#### 步骤 3.1：创建商业账号

1. 在 WhatsApp 产品页面，点击「开始」
2. 选择「创建新的 WhatsApp 商业账号」
3. 或使用现有的商业账号

#### 步骤 3.2：添加电话号码

1. 点击「添加电话号码」
2. 输入未注册 WhatsApp 的手机号
3. 选择验证方式：
   - **短信验证**：接收短信验证码
   - **语音验证**：接听电话获取验证码

> ⚠️ **重要**：该号码不能已注册 WhatsApp 个人版或商业版

#### 步骤 3.3：设置商业资料

填写商业信息：
- 显示名称（用户看到的名称）
- 商业类别
- 商业描述
- 商业地址
- 营业时间

### 4. 获取 API 凭证

在 WhatsApp 产品页面的「API 设置」中，获取以下信息：

| 凭证 | 说明 | 示例 |
|------|------|------|
| 电话号码 ID | 用于发送消息的号码标识 | `123456789012345` |
| WhatsApp 商业账号 ID | 商业账号标识 | `123456789012345` |
| 访问令牌 | 用于 API 调用的 Token | `EAAXXXXXXXXXXXXXXXXX` |

#### 生成长期访问令牌

1. 进入「系统用户」（System Users）设置
2. 点击「添加」创建系统用户
3. 分配资产：选择你的 WhatsApp 商业账号
4. 分配权限：选择 `whatsapp_business_messaging`
5. 生成访问令牌，选择「永不过期」

### 5. 配置 Webhook

#### 步骤 5.1：配置 Webhook URL

1. 在 WhatsApp 产品页面，点击「配置 Webhook」
2. 输入回调 URL：
   ```
   https://your-domain.com/webhook/whatsapp
   ```
3. 输入验证令牌（Verify Token）：自定义字符串，如 `openclaw_webhook_2024`
4. 点击「验证并保存」

#### 步骤 5.2：验证 Webhook 端点

Webhook 端点需要正确处理验证请求：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
VERIFY_TOKEN = "your_verify_token"

@app.route("/webhook/whatsapp", methods=["GET"])
def verify_webhook():
    """处理 Webhook 验证"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        # 必须返回 challenge 值
        return challenge, 200
    
    return "Forbidden", 403
```

#### 步骤 5.3：订阅字段

订阅以下 Webhook 字段：

| 字段 | 说明 |
|------|------|
| `messages` | 接收消息事件 |
| `message_deliveries` | 消息送达确认 |
| `message_reads` | 消息已读确认 |
| `message_reactions` | 消息表情反应 |
| `message_handovers` | 会话移交事件 |

### 6. 配置消息模板

WhatsApp 要求使用模板消息进行主动推送（24 小时会话窗口外）。

#### 步骤 6.1：创建模板

1. 在 WhatsApp 管理器中选择「消息模板」
2. 点击「创建模板」
3. 选择模板类别：
   - **营销**（Marketing）：推广内容
   - **交易**（Transactional）：订单通知等
   - **一次性密码**（OTP）：验证码

4. 选择语言
5. 编辑模板内容：
   - 支持变量：如 `{{1}}`、`{{2}}`
   - 示例：`您好 {{1}}，您的订单 {{2}} 已发货。`

6. 添加示例内容
7. 提交审核

#### 步骤 6.2：模板审核

- 审核时间：通常几分钟到几小时
- 状态查询：在消息模板列表查看
- 常见拒绝原因：
  - 包含促销内容却选择交易类别
  - 语言与选择不符
  - 包含敏感内容

### 7. 配置 OpenClaw

#### 步骤 7.1：环境变量配置

```bash
# .env 文件
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_BUSINESS_ACCOUNT_ID=123456789012345
WHATSAPP_ACCESS_TOKEN=EAAXXXXXXXXXXXXXXXXX
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
```

#### 步骤 7.2：YAML 配置

```yaml
# config/channels/whatsapp.yaml
channels:
  whatsapp:
    enabled: true
    
    # API 凭证
    phone_number_id: "${WHATSAPP_PHONE_NUMBER_ID}"
    business_account_id: "${WHATSAPP_BUSINESS_ACCOUNT_ID}"
    access_token: "${WHATSAPP_ACCESS_TOKEN}"
    
    # Webhook 配置
    webhook:
      path: "/webhook/whatsapp"
      verify_token: "${WHATSAPP_VERIFY_TOKEN}"
      port: 8080
      
    # API 版本
    api_version: "v18.0"
    
    # 消息处理
    message_handler:
      # 自动标记已读
      auto_mark_read: true
      # 发送已读回执
      send_read_receipts: true
```

#### 步骤 7.3：Python SDK 示例

```python
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置
PHONE_NUMBER_ID = "123456789012345"
ACCESS_TOKEN = "EAAXXXXXXXXXXXXXXXXX"
VERIFY_TOKEN = "your_verify_token"
BASE_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# ============ 发送消息 ============

def send_text_message(to, text):
    """发送文本消息"""
    url = f"{BASE_URL}/messages"
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def send_template_message(to, template_name, language_code="zh_CN", components=None):
    """发送模板消息"""
    url = f"{BASE_URL}/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code}
        }
    }
    if components:
        data["template"]["components"] = components
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def send_image_message(to, image_url, caption=None):
    """发送图片消息"""
    url = f"{BASE_URL}/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {"link": image_url}
    }
    if caption:
        data["image"]["caption"] = caption
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# ============ 消息状态 ============

def mark_message_as_read(message_id):
    """标记消息为已读"""
    url = f"{BASE_URL}/messages"
    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# ============ Webhook 处理 ============

@app.route("/webhook/whatsapp", methods=["GET"])
def verify_webhook():
    """验证 Webhook"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook/whatsapp", methods=["POST"])
def handle_webhook():
    """处理 Webhook 事件"""
    data = request.json
    
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            
            # 处理消息
            if "messages" in value:
                for message in value["messages"]:
                    handle_message(message, value.get("contacts", [{}])[0])
            
            # 处理状态更新
            if "statuses" in value:
                for status in value["statuses"]:
                    handle_status(status)
    
    return jsonify({"status": "ok"}), 200

def handle_message(message, contact):
    """处理收到的消息"""
    from_number = message.get("from")
    message_type = message.get("type")
    message_id = message.get("id")
    
    # 标记已读
    mark_message_as_read(message_id)
    
    # 处理不同类型的消息
    if message_type == "text":
        text = message.get("text", {}).get("body", "")
        response = process_text_message(text)
        send_text_message(from_number, response)
    
    elif message_type == "image":
        image_id = message.get("image", {}).get("id")
        caption = message.get("image", {}).get("caption", "")
        # 下载图片处理...
        send_text_message(from_number, "收到图片，正在处理...")
    
    elif message_type == "audio":
        audio_id = message.get("audio", {}).get("id")
        # 下载音频处理...
        send_text_message(from_number, "收到语音，正在处理...")
    
    elif message_type == "document":
        document_id = message.get("document", {}).get("id")
        filename = message.get("document", {}).get("filename", "")
        send_text_message(from_number, f"收到文件: {filename}")

def handle_status(status):
    """处理消息状态更新"""
    status_type = status.get("status")  # sent, delivered, read, failed
    message_id = status.get("id")
    timestamp = status.get("timestamp")
    
    print(f"消息 {message_id} 状态: {status_type}")

if __name__ == "__main__":
    app.run(port=8080)
```

---

## 常见问题

### Q1: 企业验证失败

**现象**：企业验证被拒绝

**常见原因及解决方案**：

| 原因 | 解决方案 |
|------|----------|
| 企业信息与证明文件不符 | 确保企业名称与营业执照完全一致 |
| 网站无法访问 | 确保网站可访问且与业务相关 |
| 缺少证明文件 | 提供清晰的营业执照扫描件 |
| 邮箱不匹配 | 使用企业域名邮箱 |

**重新提交**：根据拒绝原因修改后，在「设置」→「基本」页面重新提交

### Q2: 电话号码验证失败

**现象**：无法验证电话号码

**排查步骤**：

1. **确认号码未注册 WhatsApp**：
   - 如果已注册，需要先删除 WhatsApp 账号
   - 或更换新的号码

2. **确认可以接收短信/电话**：
   - 检查手机信号
   - 确认没有拦截短信

3. **检查号码格式**：
   - 必须包含国家代码，如 `+86 138xxxxxxxx`

**解决方案**：
- 使用固定电话选择语音验证
- 联系运营商确认短信服务正常
- 等待几分钟后重试

### Q3: Webhook 验证失败

**现象**：配置 Webhook 时提示验证失败

**排查步骤**：

1. **确认服务器可公网访问**：
   ```bash
   curl https://your-domain.com/webhook/whatsapp
   ```

2. **检查验证逻辑**：
   - 正确处理 `hub.mode`、`hub.verify_token`、`hub.challenge`
   - 必须返回 `hub.challenge` 值

3. **检查响应时间**：
   - 必须在 20 秒内响应

**正确实现**：

```python
@app.route("/webhook/whatsapp", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200  # 必须返回 challenge 值
    return "Forbidden", 403
```

### Q4: 消息发送失败

**现象**：API 返回错误

**常见错误码**：

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `131009` | 参数无效 | 检查请求参数格式 |
| `131021` | 电话号码不是有效 WhatsApp 用户 | 用户未使用 WhatsApp |
| `132001` | 模板不存在或未批准 | 检查模板名称和状态 |
| `133000` | 达到速率限制 | 降低发送频率 |
| `133004` | 消息过于频繁 | 等待后重试 |
| `133005` | 会话窗口已关闭 | 使用模板消息 |

**错误处理代码**：

```python
def send_message_with_error_handling(to, text):
    try:
        result = send_text_message(to, text)
        if "error" in result:
            error_code = result["error"].get("code")
            error_message = result["error"].get("message")
            
            if error_code == 131021:
                print(f"用户 {to} 未使用 WhatsApp")
            elif error_code == 132001:
                print("模板不存在或未批准")
            elif error_code == 133000:
                # 速率限制，等待后重试
                time.sleep(1)
                return send_message_with_error_handling(to, text)
            else:
                print(f"发送失败: {error_message}")
        return result
    except Exception as e:
        print(f"发送失败: {e}")
        return None
```

### Q5: 会话窗口过期

**现象**：无法向用户发送消息

**原因**：WhatsApp 有 24 小时会话窗口限制

**规则说明**：
- 用户最后一条消息后的 24 小时内：可以发送任意消息
- 24 小时后：只能通过模板消息联系

**解决方案**：

```python
from datetime import datetime, timedelta

# 记录用户最后消息时间
user_last_message = {}

def send_message(to, text):
    last_time = user_last_message.get(to)
    
    if last_time and datetime.now() - last_time < timedelta(hours=24):
        # 在会话窗口内，可以发送任意消息
        return send_text_message(to, text)
    else:
        # 会话窗口已关闭，使用模板消息
        return send_template_message(
            to, 
            "follow_up_template",
            components=[{
                "type": "body",
                "parameters": [{"type": "text", "text": text}]
            }]
        )

def handle_message(message, contact):
    from_number = message.get("from")
    # 更新最后消息时间
    user_last_message[from_number] = datetime.now()
    # 处理消息...
```

### Q6: 如何下载媒体文件

```python
def download_media(media_id, save_path):
    """下载媒体文件"""
    # 1. 获取媒体 URL
    url = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # 2. 下载文件
    file_url = data.get("url")
    file_response = requests.get(file_url, headers=headers)
    
    # 3. 保存文件
    with open(save_path, "wb") as f:
        f.write(file_response.content)
    
    return save_path
```

### Q7: 如何获取消息统计

```python
def get_analytics(start_date, end_date):
    """获取消息统计"""
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/analytics"
    params = {
        "start": start_date,
        "end": end_date,
        "granularity": "DAILY",
        "metric_types": "[\"SENT\",\"DELIVERED\",\"READ\"]"
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

---

## 参考链接

- [Meta for Developers](https://developers.facebook.com/)
- [WhatsApp Business API 文档](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [WhatsApp Business 管理平台](https://business.facebook.com/wa/manage/)
- [Webhook 设置指南](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks)
- [消息模板指南](https://developers.facebook.com/docs/whatsapp/message-templates)

---

*文档版本: 1.0*  
*最后更新: 2026-03-01*
