# Slack配置指南

> OpenClaw Slack 渠道完整配置教程

---

## 概述

Slack 是企业协作平台，OpenClaw 支持通过 Slack API 进行集成，包括 Socket Mode（推荐）和 HTTP Mode 两种连接方式。

---

## 配置步骤

### 1. 创建 Slack 应用

#### 步骤 1.1：访问 Slack API

1. 打开 [Slack API](https://api.slack.com/)
2. 点击页面顶部的「Create New App」

#### 步骤 1.2：选择创建方式

选择创建方式：
- **From scratch**：从头创建（推荐）
- **From an app manifest**：从配置清单创建

选择「From scratch」：
1. 输入应用名称，如 `OpenClaw`
2. 选择工作区（Workspace）
3. 点击「Create App」

> 💡 提示：应用创建后可以随时修改名称和图标

### 2. 配置权限范围

#### 步骤 2.1：添加 Bot Token 权限

1. 在应用管理页面左侧菜单，选择「OAuth & Permissions」
2. 滚动到「Scopes」部分
3. 在「Bot Token Scopes」中添加以下权限：

| 权限 | 范围 | 说明 |
|------|------|------|
| 查看用户基本信息 | `users:read` | 获取用户信息 |
| 查看用户邮箱 | `users:read.email` | 读取用户邮箱 |
| 查看频道信息 | `channels:read` | 读取公共频道列表 |
| 查看群组信息 | `groups:read` | 读取私有频道 |
| 发送消息 | `chat:write` | 发送消息到频道 |
| 发送私信 | `chat:write.public` | 发送到公共频道 |
| 查看消息 | `channels:history` | 读取频道消息历史 |
| 查看 IM 消息 | `im:history` | 读取私信历史 |
| 查看群组消息 | `groups:history` | 读取群组消息 |
| 查看 IM 频道 | `im:read` | 读取私信频道 |
| 查看群组频道 | `mpim:read` | 读取多人私信 |
| 查看表情反应 | `reactions:read` | 读取表情反应 |
| 添加表情反应 | `reactions:write` | 添加表情反应 |
| 查看文件 | `files:read` | 读取文件信息 |
| 上传文件 | `files:write` | 上传文件 |
| 使用 slash 命令 | `commands` | 注册斜杠命令 |

#### 步骤 2.2：安装应用到工作区

1. 在「OAuth & Permissions」页面顶部
2. 点击「Install to Workspace」
3. 确认权限列表并点击「Allow」
4. 复制「Bot User OAuth Token」（以 `xoxb-` 开头）

```
xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **重要**：Token 是敏感信息，请妥善保管

### 3. 启用 Socket Mode（推荐）

Socket Mode 适合内网部署或无法提供公网 URL 的场景。

#### 步骤 3.1：启用 Socket Mode

1. 在应用管理页面左侧菜单，选择「Socket Mode」
2. 开启「Enable Socket Mode」开关
3. 生成 App-Level Token：
   - 点击「Generate Token and Scopes」
   - Token Name: `OpenClaw-Socket`
   - 添加权限范围：`connections:write`
   - 点击「Generate」
   - 复制 Token（以 `xapp-` 开头）

```
xapp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 步骤 3.2：订阅事件

1. 在左侧菜单选择「Event Subscriptions」
2. 开启「Enable Events」开关
3. 在「Subscribe to bot events」中添加：

| 事件 | 说明 |
|------|------|
| `app_mention` | 监听 @Bot 的消息 |
| `message.channels` | 监听公共频道消息 |
| `message.groups` | 监听私有频道消息 |
| `message.im` | 监听私信消息 |
| `message.mpim` | 监听多人私信 |
| `reaction_added` | 监听表情反应 |
| `member_joined_channel` | 监听用户加入频道 |
| `member_left_channel` | 监听用户离开频道 |

4. 点击「Save Changes」保存

### 4. 配置 HTTP Mode（可选）

如果不使用 Socket Mode，可以使用 HTTP 模式：

#### 步骤 4.1：配置 Request URL

1. 在「Event Subscriptions」页面
2. 关闭 Socket Mode（如果已开启）
3. 在「Request URL」中输入：
   - URL 格式：`https://your-domain.com/webhook/slack`
4. Slack 会发送验证请求，确保服务器正确响应

**验证逻辑示例**：

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import time

app = Flask(__name__)
SIGNING_SECRET = "your-signing-secret"

@app.route("/webhook/slack", methods=["POST"])
def slack_events():
    # 验证请求签名
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    signature = request.headers.get("X-Slack-Signature")
    
    # 检查时间戳（防止重放攻击）
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return "Request expired", 403
    
    # 验证签名
    request_body = request.get_data().decode()
    basestring = f"v0:{timestamp}:{request_body}"
    my_signature = "v0=" + hmac.new(
        SIGNING_SECRET.encode(),
        basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(my_signature, signature):
        return "Invalid signature", 403
    
    # 处理事件
    data = request.json
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})
    
    # 异步处理事件
    handle_event(data)
    return jsonify({"ok": True})
```

#### 步骤 4.2：获取 Signing Secret

1. 在应用管理页面左侧选择「Basic Information」
2. 在「App Credentials」部分找到「Signing Secret」
3. 点击「Show」查看并复制

### 5. 将 Bot 加入频道

1. 在 Slack 中打开目标频道
2. 输入 `/invite @OpenClaw`（@你的 Bot 名称）
3. 或点击频道名称 → 集成 → 添加应用

### 6. 配置 OpenClaw

#### 步骤 6.1：环境变量配置

```bash
# .env 文件
# Socket Mode
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# HTTP Mode（如果使用）
SLACK_SIGNING_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 步骤 6.2：YAML 配置

```yaml
# config/channels/slack.yaml
channels:
  slack:
    enabled: true
    
    # 连接模式: socket 或 http
    mode: "socket"
    
    # Token 配置
    bot_token: "${SLACK_BOT_TOKEN}"      # xoxb-开头的 Bot Token
    app_token: "${SLACK_APP_TOKEN}"      # xapp-开头的 App Token（Socket Mode 需要）
    signing_secret: "${SLACK_SIGNING_SECRET}"  # HTTP Mode 需要
    
    # Socket Mode 配置
    socket:
      ping_interval: 30
      
    # HTTP Mode 配置
    http:
      path: "/webhook/slack"
      port: 8080
      
    # 消息处理
    message_handler:
      # 处理 @提及
      handle_mentions: true
      # 处理所有消息（不只是 @提及）
      handle_all_messages: false
      # Bot 用户 ID
      bot_user_id: "Uxxxxxxxx"
```

#### 步骤 6.3：Python SDK 示例

**使用 slack-bolt（推荐）**：

```python
# 安装: pip install slack-bolt
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# 初始化应用
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def handle_mention(event, say):
    """处理 @Bot 的消息"""
    user = event["user"]
    text = event["text"]
    channel = event["channel"]
    
    # 处理消息
    response = f"<@{user}> 收到你的消息: {text}"
    say(text=response, channel=channel)

@app.event("message")
def handle_message(event, say):
    """处理普通消息"""
    # 忽略 Bot 自己的消息
    if event.get("bot_id"):
        return
    
    # 只处理私信
    if event.get("channel_type") == "im":
        text = event.get("text", "")
        user = event["user"]
        response = f"私信收到: {text}"
        say(text=response)

@app.command("/openclaw")
def handle_command(ack, command, say):
    """处理斜杠命令"""
    ack()  # 立即确认收到命令
    text = command["text"]
    user = command["user_name"]
    response = f"{user} 使用了命令: {text}"
    say(text=response)

@app.action("button_click")
def handle_button_click(ack, body, say):
    """处理按钮点击"""
    ack()
    user = body["user"]["name"]
    say(text=f"{user} 点击了按钮!")

if __name__ == "__main__":
    # Socket Mode
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
```

**HTTP Mode 示例**：

```python
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@app.event("app_mention")
def handle_mention(event, say):
    say(text=f"收到消息: {event['text']}")

@flask_app.route("/webhook/slack", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=8080)
```

**发送消息示例**：

```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

def send_message(channel, text):
    """发送文本消息"""
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                }
            ]
        )
        return response
    except SlackApiError as e:
        print(f"Error: {e}")

def send_ephemeral(channel, user, text):
    """发送仅指定用户可见的消息"""
    try:
        response = client.chat_postEphemeral(
            channel=channel,
            user=user,
            text=text
        )
        return response
    except SlackApiError as e:
        print(f"Error: {e}")
```

---

## 常见问题

### Q1: Socket Mode 连接失败

**现象**：无法建立 Socket 连接或频繁断开

**排查步骤**：

1. **确认 Token 正确**：
   - Bot Token 以 `xoxb-` 开头
   - App Token 以 `xapp-` 开头

2. **检查 App Token 权限**：
   - 必须有 `connections:write` 权限

3. **检查网络连接**：
   ```bash
   curl https://slack.com/api/api.test
   ```

4. **查看日志**：启用调试模式
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

### Q2: 收不到事件

**现象**：订阅了事件但没有收到

**排查步骤**：

1. **确认应用已安装到工作区**：
   - 进入「OAuth & Permissions」
   - 确认显示「Installed to Workspace」

2. **检查事件订阅配置**：
   - 确认「Enable Events」已开启
   - 确认已订阅所需事件类型

3. **确认 Bot 在频道中**：
   - 在频道中输入 `/invite @BotName`
   - 或检查频道成员列表

4. **检查频道类型**：
   - 公共频道需要 `message.channels`
   - 私有频道需要 `message.groups`
   - 私信需要 `message.im`

**解决方案**：

```python
# 使用 API 将 Bot 加入频道
import requests

def join_channel(channel_id):
    response = requests.post(
        "https://slack.com/api/conversations.join",
        headers={"Authorization": f"Bearer {BOT_TOKEN}"},
        json={"channel": channel_id}
    )
    return response.json()
```

### Q3: 权限不足（missing_scope）

**现象**：API 调用返回 `missing_scope` 错误

**解决方案**：

1. 在「OAuth & Permissions」页面添加所需权限
2. **重新安装应用到工作区**（重要！）
3. 使用新生成的 Token

### Q4: 消息发送失败

**常见错误及解决方案**：

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `channel_not_found` | 频道不存在 | 检查频道 ID 是否正确 |
| `not_in_channel` | Bot 不在频道中 | 邀请 Bot 加入频道 |
| `msg_too_long` | 消息超过 4000 字符 | 截断或分段发送 |
| `rate_limited` | 触发速率限制 | 降低发送频率 |
| `invalid_blocks` | Block Kit 格式错误 | 检查 JSON 格式 |

**代码示例**：

```python
def send_message_safe(channel, text):
    try:
        # 截断长消息
        if len(text) > 4000:
            text = text[:3997] + "..."
        
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
    except SlackApiError as e:
        error = e.response["error"]
        if error == "not_in_channel":
            # 尝试加入频道
            client.conversations_join(channel=channel)
            # 重试发送
            response = client.chat_postMessage(channel=channel, text=text)
        elif error == "channel_not_found":
            print(f"频道不存在: {channel}")
        else:
            raise
```

### Q5: 如何获取用户 ID 和频道 ID

```python
@app.event("message")
def handle_message(event, say):
    user_id = event["user"]        # 用户 ID，如 U1234567890
    channel_id = event["channel"]  # 频道 ID，如 C1234567890
    team_id = event["team"]        # 工作区 ID
    
    # 获取用户信息
    user_info = client.users_info(user=user_id)
    user_name = user_info["user"]["name"]
    
    say(text=f"用户 {user_name} (ID: {user_id}) 在频道 {channel_id} 发送了消息")
```

### Q6: 如何创建斜杠命令

1. 在应用管理页面选择「Slash Commands」
2. 点击「Create New Command」
3. 填写命令信息：
   - Command: `/openclaw`
   - Request URL: `https://your-domain.com/slack/commands`
   - Short Description: `与 OpenClaw 交互`
4. 点击「Save」

```python
@app.command("/openclaw")
def handle_command(ack, command, say):
    ack()  # 必须在 3 秒内响应
    
    user = command["user_name"]
    text = command["text"]
    channel = command["channel_id"]
    
    # 异步处理耗时操作
    response = process_command(text)
    say(text=response)
```

---

## 参考链接

- [Slack API 官方文档](https://api.slack.com/)
- [Slack Bolt Python](https://slack.dev/bolt-python/)
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Slack API Methods](https://api.slack.com/methods)

---

*文档版本: 1.0*  
*最后更新: 2026-03-01*
