# 飞书配置指南

> OpenClaw 飞书渠道完整配置教程

---

## 概述

飞书是字节跳动旗下的企业协作平台，OpenClaw 通过飞书开放平台 API 与飞书进行集成，支持个人聊天、群组互动、卡片消息等功能。

---

## 配置步骤

### 1. 创建飞书应用

#### 步骤 1.1：访问飞书开放平台

1. 打开 [飞书开放平台](https://open.feishu.cn/)
2. 使用企业管理员账号登录（或让管理员授权）
3. 点击右上角「开发者后台」

#### 步骤 1.2：创建企业自建应用

1. 在开发者后台，点击「创建应用」
2. 选择「企业自建应用」
3. 填写应用信息：
   - **应用名称**：例如 `OpenClaw助手`
   - **应用描述**：AI 助手集成应用
   - **应用图标**：上传应用图标（可选，建议 512x512 PNG）
4. 点击「创建应用」

> 💡 提示：应用名称创建后可以通过「凭证与基础信息」页面修改

### 2. 获取凭证

#### 步骤 2.1：获取 App ID 和 App Secret

1. 进入应用详情页
2. 在左侧菜单选择「凭证与基础信息」
3. 复制以下信息：
   - **App ID**（应用 ID）：格式如 `cli_xxxxxxxxxxxx`
   - **App Secret**（应用密钥）：点击「查看」按钮获取

```yaml
# 配置示例
feishu:
  app_id: "cli_xxxxxxxxxxxxxxxx"
  app_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

> ⚠️ **重要**：App Secret 是敏感信息，请妥善保管，不要提交到代码仓库

#### 步骤 2.2：获取加密密钥（可选）

如果启用事件加密，需要获取 Encrypt Key：

1. 在「凭证与基础信息」页面
2. 找到「事件订阅」-「加密密钥」
3. 点击「查看」获取

### 3. 配置权限

#### 步骤 3.1：添加机器人能力

1. 在应用详情页，点击「添加应用能力」
2. 选择「机器人」
3. 点击「添加」
4. 配置机器人信息：
   - 机器人名称
   - 机器人头像
   - 机器人描述

#### 步骤 3.2：申请权限

1. 进入「权限管理」页面
2. 点击「申请权限」
3. 添加以下必需权限：

| 权限名称 | 权限 Key | 说明 |
|---------|---------|------|
| 获取用户 ID | `contact:user.id:readonly` | 获取用户身份信息 |
| 获取用户基本信息 | `contact:user.base:readonly` | 读取用户基本信息 |
| 获取部门信息 | `contact:department.base:readonly` | 读取组织架构 |
| 读取消息 | `im:message:readonly` | 接收用户消息 |
| 发送消息 | `im:message:send` | 向用户发送消息 |
| 读取群信息 | `im:chat:readonly` | 获取群聊信息 |
| 读取群成员信息 | `im:chat:members:readonly` | 获取群成员列表 |
| 获取群组信息 | `im:chat.group:readonly` | 读取群组详情 |
| 管理群组 | `im:chat.group:manage` | 管理群组设置 |
| 上传图片 | `im:image:upload` | 上传图片资源 |
| 上传文件 | `im:file:upload` | 上传文件资源 |

4. 点击「申请」提交权限申请
5. **联系企业管理员审批权限**（重要！）

> ⏰ 注意：权限申请需要企业管理员审批后才能生效

### 4. 设置事件订阅

事件订阅用于接收用户发送的消息和其他事件。

#### 步骤 4.1：配置请求地址

1. 进入「事件订阅」页面
2. 开启「事件订阅」开关
3. 配置请求地址（Request URL）：
   - 格式：`https://your-domain.com/webhook/feishu`
4. 点击「验证」按钮验证 URL 可访问性

**验证逻辑示例**：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/feishu", methods=["POST"])
def feishu_webhook():
    data = request.json
    
    # 处理 URL 验证
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})
    
    # 处理事件
    handle_event(data)
    return jsonify({"code": 0})
```

#### 步骤 4.2：订阅事件类型

添加以下事件订阅：

| 事件类型 | 事件 Key | 说明 |
|---------|---------|------|
| 接收消息 | `im.message.receive_v1` | 接收用户发送的消息 |
| 群组被创建 | `im.chat.group.created_v1` | 监听群组创建事件 |
| 用户进入群组 | `im.chat.member.user.added_v1` | 监听用户进群事件 |
| 用户离开群组 | `im.chat.member.user.deleted_v1` | 监听用户退群事件 |
| 消息已读 | `im.message.message_read_v1` | 消息已读状态 |

#### 步骤 4.3：配置加密（可选）

如需加密事件数据：

1. 在「事件订阅」页面开启「加密」
2. 获取加密密钥
3. 在代码中实现解密逻辑：

```python
import base64
import hashlib
from Crypto.Cipher import AES

def decrypt_feishu_event(encrypt_data, encrypt_key):
    """解密飞书事件数据"""
    # 对 encrypt_key 进行 SHA256 哈希，取前 32 字节
    key = hashlib.sha256(encrypt_key.encode()).digest()[:32]
    
    # Base64 解码
    cipher = base64.b64decode(encrypt_data)
    
    # AES-256-CBC 解密
    iv = cipher[:16]
    ciphertext = cipher[16:]
    
    aes = AES.new(key, AES.MODE_CBC, iv)
    plaintext = aes.decrypt(ciphertext)
    
    # 去除填充
    pad_len = plaintext[-1]
    plaintext = plaintext[:-pad_len]
    
    return json.loads(plaintext)
```

### 5. 发布应用

应用需要发布后才能被正常使用。

#### 步骤 5.1：创建版本

1. 进入「版本管理与发布」页面
2. 点击「创建版本」
3. 填写版本信息：
   - 版本号：如 `1.0.0`
   - 更新说明：初始版本
   - 可用范围：选择可用成员范围

#### 步骤 5.2：申请发布

1. 点击「申请发布」
2. 选择审批人（企业管理员）
3. 等待审批通过

> ⏰ 注意：发布审批通常需要企业管理员审核

### 6. 配置 OpenClaw

#### 步骤 6.1：环境变量配置

```bash
# .env 文件
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_ENCRYPT_KEY=          # 可选
FEISHU_VERIFICATION_TOKEN=   # 可选
```

#### 步骤 6.2：YAML 配置

```yaml
# config/channels/feishu.yaml
channels:
  feishu:
    enabled: true
    app_id: "${FEISHU_APP_ID}"
    app_secret: "${FEISHU_APP_SECRET}"
    encrypt_key: "${FEISHU_ENCRYPT_KEY}"      # 可选
    verification_token: "${FEISHU_VERIFICATION_TOKEN}"  # 可选
    
    # Webhook 配置
    webhook:
      path: "/webhook/feishu"
      port: 8080
      
    # 消息处理配置
    message_handler:
      # 是否处理群消息
      handle_group_message: true
      # 是否处理私聊消息
      handle_private_message: true
      # 机器人名称（用于 @识别）
      bot_name: "OpenClaw"
      # 需要 @机器人才能响应（群聊中）
      require_mention: true
```

#### 步骤 6.3：Python SDK 示例

**使用飞书官方 SDK**：

```python
# 安装: pip install lark-oapi
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

# 创建客户端
client = lark.Client.builder() \
    .app_id("cli_xxxxxxxxxxxxxxxx") \
    .app_secret("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") \
    .log_level(lark.LogLevel.DEBUG) \
    .build()

def send_text_message(chat_id, text):
    """发送文本消息"""
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(chat_id)
            .msg_type("text")
            .content(json.dumps({"text": text}))
            .build()) \
        .build()
    
    response = client.im.v1.message.create(request)
    if not response.success():
        print(f"发送失败: {response.msg}")
    return response

def send_card_message(chat_id, title, content):
    """发送卡片消息"""
    card_data = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": content}
            }
        ]
    }
    
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(chat_id)
            .msg_type("interactive")
            .content(json.dumps(card_data))
            .build()) \
        .build()
    
    return client.im.v1.message.create(request)
```

**Webhook 服务器示例**：

```python
from flask import Flask, request, jsonify
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

app = Flask(__name__)

# 初始化客户端
client = lark.Client.builder() \
    .app_id("cli_xxxxxxxxxxxxxxxx") \
    .app_secret("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") \
    .build()

@app.route("/webhook/feishu", methods=["POST"])
def feishu_webhook():
    data = request.json
    
    # 处理 URL 验证
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})
    
    # 处理事件回调
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        
        # 处理消息事件
        if event.get("type") == "im.message.receive_v1":
            message = event.get("message", {})
            sender = event.get("sender", {})
            
            chat_id = message.get("chat_id")
            content = json.loads(message.get("content", "{}"))
            text = content.get("text", "")
            
            # 处理消息
            response_text = f"收到消息: {text}"
            
            # 回复消息
            reply_request = ReplyMessageRequest.builder() \
                .message_id(message.get("message_id")) \
                .request_body(ReplyMessageRequestBody.builder()
                    .content(json.dumps({"text": response_text}))
                    .msg_type("text")
                    .build()) \
                .build()
            
            client.im.v1.message.reply(reply_request)
    
    return jsonify({"code": 0})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

---

## 常见问题

### Q1: 事件订阅验证失败

**现象**：配置 Request URL 时提示验证失败

**排查步骤**：

1. **确认服务器可公网访问**：
   ```bash
   curl -X POST https://your-domain.com/webhook/feishu \
     -H "Content-Type: application/json" \
     -d '{"type":"url_verification","challenge":"test"}'
   ```

2. **检查响应格式**：必须正确返回 challenge 值
   ```python
   # 正确的响应格式
   {"challenge": "xxxxxxxxxxxxxxxx"}
   ```

3. **检查防火墙设置**：确保端口已放行

4. **检查 Content-Type**：确保返回 `application/json`

### Q2: 权限申请被拒绝

**现象**：权限申请状态显示「被拒绝」

**解决方案**：

1. 确认申请的权限与应用功能匹配
2. 联系企业管理员说明权限用途
3. 检查是否申请了敏感权限（如通讯录全量读取）
4. 在权限说明中详细描述使用场景

### Q3: 机器人收不到消息

**现象**：用户 @机器人但无响应

**排查步骤**：

1. **确认机器人已添加到群组**：
   - 在群组中 @机器人
   - 检查机器人是否在群成员列表中

2. **检查事件订阅**：
   - 确认已订阅 `im.message.receive_v1`
   - 检查事件订阅开关是否开启

3. **确认应用已发布**：
   - 进入「版本管理与发布」
   - 确认版本状态为「已发布」

4. **查看事件日志**：
   - 在「事件订阅」页面查看「推送记录」
   - 检查事件是否成功送达

### Q4: Token 过期

**现象**：API 调用返回 `99991663` 错误码（token 过期）

**解决方案**：

SDK 会自动处理 Token 刷新，如使用原生 HTTP：

```python
import time
import requests

class FeishuTokenManager:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token = None
        self._expire_time = 0
    
    def get_token(self):
        # 提前 5 分钟刷新
        if time.time() < self._expire_time - 300:
            return self._token
        
        # 获取新 Token
        resp = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
        )
        data = resp.json()
        
        if data.get("code") == 0:
            self._token = data["tenant_access_token"]
            self._expire_time = time.time() + data["expire"]
            return self._token
        else:
            raise Exception(f"获取 Token 失败: {data}")
```

### Q5: 发送消息失败，提示 "chat id not found"

**原因**：
- 机器人不在该群组中
- chat_id 格式错误

**解决方案**：

```python
# 先让机器人加入群组
# 或者使用 open_chat_id

# 获取群组列表
from lark_oapi.api.im.v1 import ListChatRequest

request = ListChatRequest.builder().build()
response = client.im.v1.chat.list(request)

if response.success():
    for chat in response.data.items:
        print(f"群名: {chat.name}, Chat ID: {chat.chat_id}")
```

### Q6: 如何获取用户的 Open ID

```python
# 从事件数据中获取
sender = event.get("sender", {})
sender_id = sender.get("sender_id", {})
open_id = sender_id.get("open_id")  # 用户唯一标识
union_id = sender_id.get("union_id")  # 跨应用用户标识
```

---

## 参考链接

- [飞书开放平台](https://open.feishu.cn/)
- [飞书 Bot API 文档](https://open.feishu.cn/document/home/develop-a-bot-in-5-minutes/create-an-app)
- [飞书事件订阅文档](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/event-real-time-events/event-overview)
- [飞书 Python SDK](https://github.com/larksuite/oapi-sdk-python)

---

*文档版本: 1.0*  
*最后更新: 2026-03-01*
