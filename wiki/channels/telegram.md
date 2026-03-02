# Telegram配置指南

> OpenClaw Telegram Bot 配置教程

---

## 概述

Telegram 是 OpenClaw 支持的主要渠道之一，通过 Bot API 实现消息收发。本指南将详细介绍如何创建 Telegram Bot、获取 Token、配置 Webhook 以及集成到 OpenClaw。

---

## 配置步骤

### 1. 创建 Bot

#### 步骤 1.1：联系 BotFather

1. 打开 Telegram 应用（桌面版或手机版）
2. 在搜索框中输入 `@BotFather`
3. 点击 BotFather 账号，然后点击「Start」开始对话

#### 步骤 1.2：创建新 Bot

1. 向 BotFather 发送命令 `/newbot`
2. 按提示设置 Bot 信息：
   - **名称**（Name）：显示名称，如 `OpenClaw助手`
   - **用户名**（Username）：唯一标识，**必须以 `bot` 结尾**，如 `openclaw_bot`

> ⚠️ 注意：用户名必须是全局唯一的，如果已被占用需要更换

创建成功后，BotFather 会返回如下消息：

```
Done! Congratulations on your new bot. You will find it at t.me/openclaw_bot.
You can now add a description, about section and profile picture for your bot,
see /help for a list of commands.

Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrSTUvwxyz1234567890

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

**请妥善保存 Token**，格式为 `123456789:ABCdefGHIjklMNOpqrSTUvwxyz1234567890`

#### 步骤 1.3：设置 Bot 资料（可选）

向 BotFather 发送以下命令完善 Bot 信息：

```
/setname - 修改 Bot 名称
/setdescription - 设置描述（用户点击「开始」前看到的文字）
/setabouttext - 设置关于文本（Bot 资料页显示）
/setuserpic - 设置头像
/setcommands - 设置命令菜单
```

### 2. 获取 Token

Token 在创建 Bot 时由 BotFather 提供，格式为：

```
123456789:ABCdefGHIjklMNOpqrSTUvwxyz1234567890
```

**如果丢失 Token**：
1. 向 BotFather 发送 `/mybots`
2. 选择你的 Bot
3. 点击「API Token」
4. 点击「Revoke current token」生成新 Token

### 3. 配置 Webhook

Telegram 支持两种接收消息的方式：

| 方式 | 适用场景 | 特点 |
|------|----------|------|
| **Webhook** | 生产环境 | 实时推送，需要公网 HTTPS 服务器 |
| **Long Polling** | 开发/测试环境 | 主动拉取，适合内网或本地开发 |

#### 方式一：Webhook 模式（推荐用于生产）

**前置要求**：
- 有效的 SSL 证书（不能使用自签名证书）
- 公网可访问的 HTTPS 服务器

**步骤 3.1：设置 Webhook**

```bash
# 使用 curl 设置 Webhook
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-domain.com/webhook/telegram",
    "allowed_updates": ["message", "callback_query", "inline_query"],
    "drop_pending_updates": true
  }'
```

**参数说明**：
- `url`: 你的服务器接收 Webhook 的地址
- `allowed_updates`: 指定接收的事件类型
- `drop_pending_updates`: 是否丢弃设置前的积压消息

**步骤 3.2：验证 Webhook 设置**

```bash
# 获取当前 Webhook 信息
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

成功响应示例：

```json
{
  "ok": true,
  "result": {
    "url": "https://your-domain.com/webhook/telegram",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "max_connections": 40
  }
}
```

**步骤 3.3：删除 Webhook（如需切换回 Polling）**

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/deleteWebhook?drop_pending_updates=true"
```

#### 方式二：Long Polling 模式（适合开发）

```python
import requests
import time

TOKEN = "YOUR_BOT_TOKEN"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None):
    """获取更新"""
    params = {
        "timeout": 30,  # 长轮询超时时间
        "limit": 100    # 每次获取的最大消息数
    }
    if offset:
        params["offset"] = offset
    
    response = requests.get(f"{BASE_URL}/getUpdates", params=params)
    return response.json()

def main():
    offset = None
    print("Bot 已启动，正在监听消息...")
    
    while True:
        try:
            updates = get_updates(offset)
            if updates.get("result"):
                for update in updates["result"]:
                    # 处理消息
                    handle_update(update)
                    # 更新 offset，避免重复处理
                    offset = update["update_id"] + 1
        except Exception as e:
            print(f"错误: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
```

### 4. 设置 OpenClaw

#### 步骤 4.1：配置环境变量

```bash
# .env 文件
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz1234567890
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook/telegram
TELEGRAM_MODE=webhook  # 或 polling
```

#### 步骤 4.2：OpenClaw 配置示例

**YAML 配置**：

```yaml
# config/channels/telegram.yaml
channels:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    
    # 连接模式: webhook 或 polling
    mode: "webhook"
    
    # Webhook 配置
    webhook:
      url: "${TELEGRAM_WEBHOOK_URL}"
      path: "/webhook/telegram"
      secret_token: "${TELEGRAM_SECRET_TOKEN}"  # 可选，用于验证请求
      max_connections: 40
      
    # Polling 配置（开发环境）
    polling:
      timeout: 30
      limit: 100
      
    # 消息处理配置
    message_handler:
      parse_mode: "Markdown"  # 或 "HTML"
      disable_web_page_preview: false
```

#### 步骤 4.3：Webhook 服务器代码示例

**Python (Flask)**：

```python
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def handle_message(update):
    """处理收到的消息"""
    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        # 处理消息并回复
        response_text = f"收到消息: {text}"
        send_message(chat_id, response_text)

def send_message(chat_id, text):
    """发送消息"""
    import requests
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route("/webhook/telegram", methods=["POST"])
def telegram_webhook():
    """接收 Telegram Webhook"""
    update = request.json
    handle_message(update)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

**Python (python-telegram-bot 库)**：

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    await update.message.reply_text("欢迎使用 OpenClaw Bot!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理普通消息"""
    text = update.message.text
    # 处理消息逻辑
    response = f"您说: {text}"
    await update.message.reply_text(response)

async def main():
    # 创建应用
    application = Application.builder().token(TOKEN).build()
    
    # 添加处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 启动 Webhook
    await application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        webhook_url="https://your-domain.com/webhook/telegram"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 常见问题

### Q1: Webhook 设置失败，返回错误

**现象**：调用 `setWebhook` 返回错误信息

**排查步骤**：

1. **检查 URL 协议**：必须使用 `https://`，不支持 `http://`
2. **验证 SSL 证书**：不能使用自签名证书
   ```bash
   # 检查证书有效性
   openssl s_client -connect your-domain.com:443 -servername your-domain.com
   ```
3. **测试端点可访问性**：
   ```bash
   curl -X POST https://your-domain.com/webhook/telegram -d '{}'
   ```
4. **检查端口**：确保服务器防火墙放行相应端口

**常见错误码**：

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Bad Request: bad webhook` | URL 格式错误或不可访问 | 检查 URL 和服务器状态 |
| `Bad Request: invalid webhook URL` | 使用了 http:// | 改为 https:// |
| `Bad Request: failed to set webhook` | SSL 证书问题 | 使用有效证书 |

### Q2: Bot 收不到消息

**现象**：用户发送消息但 Bot 无响应

**排查步骤**：

1. **确认用户已启动 Bot**：
   - 用户需要点击「Start」或发送 `/start` 命令
   - 检查 Bot 是否被用户屏蔽

2. **检查 Webhook 状态**：
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
   ```
   关注 `pending_update_count` 字段，如果数值很大说明消息积压

3. **检查服务器日志**：确认请求是否到达服务器

4. **尝试清除 Webhook 测试**：
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
   ```
   然后使用 Polling 模式测试是否能收到消息

### Q3: 消息格式错误，发送失败

**现象**：调用 `sendMessage` 返回 400 错误

**原因**：Markdown/HTML 格式不正确

**解决方案**：

```python
def escape_markdown(text):
    """转义 Markdown 特殊字符"""
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

# 发送消息时处理异常
try:
    await bot.send_message(chat_id, text, parse_mode="Markdown")
except Exception as e:
    # 如果 Markdown 解析失败，使用纯文本发送
    await bot.send_message(chat_id, text)
```

### Q4: Bot 响应延迟高

**可能原因**：
- 服务器处理速度慢
- Webhook 连接数不足

**优化方案**：

```bash
# 增加最大连接数
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d '{
    "url": "https://your-domain.com/webhook/telegram",
    "max_connections": 100
  }'
```

### Q5: 如何获取用户 ID 和聊天 ID

```python
async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    
    await update.message.reply_text(
        f"用户 ID: `{user_id}`\n"
        f"聊天 ID: `{chat_id}`\n"
        f"用户名: @{username}",
        parse_mode="Markdown"
    )
```

---

## 参考链接

- [Telegram Bot API 官方文档](https://core.telegram.org/bots/api)
- [python-telegram-bot 文档](https://docs.python-telegram-bot.org/)
- [BotFather](https://t.me/botfather)

---

*文档版本: 1.0*  
*最后更新: 2026-03-01*
