# Discord配置指南

> OpenClaw Discord Bot 配置教程

---

## 概述

Discord 是面向游戏社区和开发者的即时通讯平台，OpenClaw 通过 Discord Bot API 进行集成，支持消息收发、斜杠命令、嵌入消息等功能。

---

## 配置步骤

### 1. 创建 Discord 应用

#### 步骤 1.1：访问 Discord 开发者门户

1. 打开 [Discord Developer Portal](https://discord.com/developers/applications)
2. 使用 Discord 账号登录

#### 步骤 1.2：创建应用

1. 点击右上角的「New Application」
2. 输入应用名称，如 `OpenClaw`
3. 点击「Create」

> 💡 提示：应用名称可以稍后修改

#### 步骤 1.3：获取应用信息

1. 在「General Information」页面
2. 复制以下信息：
   - **Application ID**：应用唯一标识（18位数字）
   - **Public Key**：用于验证请求签名（Webhook 模式需要）

### 2. 创建 Bot

#### 步骤 2.1：添加 Bot

1. 在左侧菜单选择「Bot」
2. 点击「Add Bot」
3. 点击「Yes, do it!」确认

#### 步骤 2.2：配置 Bot 设置

1. **Bot 名称**：设置显示名称
2. **Icon**：点击「Upload Image」上传头像（建议 1024x1024 PNG/JPG）
3. **Token**：点击「Reset Token」生成新 Token

> ⚠️ **重要**：Token 只显示一次，务必立即保存！

Token 格式：
```
MTAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 步骤 2.3：配置 Intents

Intents 决定 Bot 可以接收哪些事件，必须正确配置才能正常工作。

1. 在「Bot」页面找到「Privileged Gateway Intents」
2. 启用以下 Intents：

| Intent | 说明 | 必需 |
|--------|------|------|
| **Message Content Intent** | 接收消息内容 | **是** |
| Server Members Intent | 接收服务器成员信息 | 推荐 |
| Presence Intent | 接收用户在线状态 | 可选 |

3. 点击「Save Changes」保存

> ⚠️ **注意**：如果 Bot 在 100 个以上服务器，启用 Privileged Intents 需要先验证 Bot

### 3. 配置权限并邀请 Bot

#### 步骤 3.1：生成 OAuth2 URL

1. 在左侧菜单选择「OAuth2」→「URL Generator」
2. 在「Scopes」中勾选：
   - `bot`：作为 Bot 加入服务器
   - `applications.commands`：使用斜杠命令（推荐）

3. 在「Bot Permissions」中勾选以下权限：

| 权限 | 值 | 说明 |
|------|-----|------|
| View Channels | 0x400 | 查看频道 |
| Send Messages | 0x800 | 发送消息 |
| Send Messages in Threads | 0x4000000 | 在线程中发送消息 |
| Create Public Threads | 0x800000000 | 创建公开线程 |
| Create Private Threads | 0x1000000000 | 创建私有线程 |
| Embed Links | 0x4000 | 发送嵌入链接 |
| Attach Files | 0x8000 | 上传文件 |
| Add Reactions | 0x40 | 添加表情反应 |
| Use External Emojis | 0x40000 | 使用外部表情 |
| Mention @everyone | 0x20000 | @所有人 |
| Read Message History | 0x10000 | 读取消息历史 |
| Use Slash Commands | 0x80000000 | 使用斜杠命令 |
| Connect | 0x100000 | 连接语音频道 |
| Speak | 0x200000 | 在语音频道说话 |

4. 页面底部会生成 URL，复制该链接

#### 步骤 3.2：邀请 Bot 到服务器

1. 打开生成的 OAuth2 URL
2. 选择要加入的服务器（需要管理员权限）
3. 确认权限列表
4. 点击「Authorize」
5. 完成人机验证（CAPTCHA）

### 4. 配置 OpenClaw

#### 步骤 4.1：环境变量配置

```bash
# .env 文件
DISCORD_BOT_TOKEN=MTAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 步骤 4.2：YAML 配置

```yaml
# config/channels/discord.yaml
channels:
  discord:
    enabled: true
    bot_token: "${DISCORD_BOT_TOKEN}"
    
    # Gateway Intents 配置
    intents:
      - guilds              # 服务器信息
      - guild_messages      # 服务器消息
      - guild_members       # 服务器成员
      - direct_messages     # 私信
      - message_content     # 消息内容（必需）
      - guild_reactions     # 表情反应
      
    # 消息处理
    message_handler:
      # 命令前缀（传统命令）
      command_prefix: "!"
      # 处理 @提及
      handle_mentions: true
      # 处理私信
      handle_dms: true
      
    # 分片配置（大型 Bot 需要）
    sharding:
      enabled: false
      shards: 1
```

#### 步骤 4.3：Python SDK 示例

**使用 discord.py**：

```python
# 安装: pip install discord.py
import discord
from discord.ext import commands
import asyncio

# 配置 Intents（必须启用 message_content）
intents = discord.Intents.default()
intents.message_content = True  # 必需！
intents.members = True
intents.dm_messages = True

# 创建 Bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None  # 禁用默认帮助命令
)

@bot.event
async def on_ready():
    """Bot 启动时调用"""
    print(f'{bot.user} 已上线!')
    print(f'已连接到 {len(bot.guilds)} 个服务器')
    
    # 设置 Bot 状态
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="OpenClaw"
        )
    )

@bot.event
async def on_message(message):
    """收到消息时调用"""
    # 忽略 Bot 自己的消息
    if message.author == bot.user:
        return
    
    # 处理命令
    await bot.process_commands(message)
    
    # 处理提及
    if bot.user.mentioned_in(message):
        # 移除提及标记
        content = message.content
        for mention in message.mentions:
            content = content.replace(f'<@!{mention.id}>', '')
            content = content.replace(f'<@{mention.id}>', '')
        content = content.strip()
        
        # 回复消息
        response = f"你好 {message.author.mention}! 收到: {content}"
        await message.reply(response)

@bot.command()
async def ping(ctx):
    """测试命令: !ping"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! 延迟: {latency}ms')

@bot.command()
async def ask(ctx, *, question):
    """提问命令: !ask 你的问题"""
    # 显示输入状态
    async with ctx.typing():
        response = process_question(question)
    await ctx.send(response)

@bot.command()
async def embed(ctx):
    """发送嵌入消息: !embed"""
    embed = discord.Embed(
        title="OpenClaw",
        description="这是一个嵌入消息示例",
        color=discord.Color.blue(),
        url="https://github.com/openclaw"
    )
    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )
    embed.add_field(name="字段1", value="值1", inline=True)
    embed.add_field(name="字段2", value="值2", inline=True)
    embed.set_footer(text="OpenClaw Bot")
    
    await ctx.send(embed=embed)

# 运行 Bot
TOKEN = "YOUR_BOT_TOKEN"
bot.run(TOKEN)
```

**使用 discord.py 2.0+ 的斜杠命令**：

```python
import discord
from discord import app_commands

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        # 同步斜杠命令
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'{bot.user} 已上线!')

# 定义斜杠命令
@bot.tree.command(name="ping", description="测试 Bot 延迟")
async def ping_command(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! {latency}ms")

@bot.tree.command(name="ask", description="向 AI 提问")
@app_commands.describe(question="你的问题")
async def ask_command(interaction: discord.Interaction, question: str):
    # 延迟响应（处理耗时操作）
    await interaction.response.defer()
    
    response = process_question(question)
    await interaction.followup.send(response)

# 运行
bot.run(TOKEN)
```

**使用 interactions.py（现代推荐）**：

```python
# 安装: pip install discord-py-interactions
import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext

bot = Client(
    token="YOUR_BOT_TOKEN",
    intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT
)

@listen()
async def on_ready():
    print(f"Bot 已登录为 {bot.user}")

@slash_command(name="ping", description="测试 Bot 延迟")
async def ping(ctx: SlashContext):
    latency = bot.latency * 1000
    await ctx.send(f"🏓 Pong! {latency:.0f}ms")

@slash_command(name="ask", description="向 AI 提问")
async def ask(ctx: SlashContext, question: str):
    await ctx.defer()  # 延迟响应
    response = process_question(question)
    await ctx.send(response)

bot.start()
```

---

## 常见问题

### Q1: Bot 无法接收消息内容

**现象**：`on_message` 事件触发但 `message.content` 为空

**原因**：未启用 Message Content Intent

**解决方案**：

1. 在 Discord 开发者门户的「Bot」页面
2. 启用「Message Content Intent」
3. 保存更改
4. 重启 Bot

> ⚠️ 如果 Bot 在 100 个以上服务器，需要先验证 Bot 才能启用 Privileged Intents

### Q2: Bot 无法加入服务器

**现象**：OAuth2 URL 无效或提示权限不足

**排查步骤**：

1. **确认 OAuth2 URL 包含 `bot` scope**：
   ```
   https://discord.com/api/oauth2/authorize?client_id=XXX&scope=bot&permissions=8
   ```

2. **检查权限数值**：确保 `permissions` 参数正确

3. **确认你不是以 Bot 身份登录**：必须使用普通 Discord 账号

4. **确认你有服务器管理权限**：需要「管理服务器」权限才能邀请 Bot

### Q3: Gateway 连接断开

**现象**：Bot 频繁掉线或无法连接

**排查步骤**：

1. **检查 Token 是否正确**：
   - 确认 Token 没有多余的空格
   - 确认使用的是 Bot Token 而不是 Client Secret

2. **确认 Intents 配置正确**：
   ```python
   intents = discord.Intents.default()
   intents.message_content = True  # 必需
   ```

3. **检查网络连接**：
   ```bash
   curl https://discord.com/api/v10/gateway
   ```

4. **查看 Discord API 状态**：
   - https://status.discord.com/

**解决方案**：

```python
@bot.event
async def on_disconnect():
    print("Bot 断开连接，将在 5 秒后尝试重连...")
    await asyncio.sleep(5)

@bot.event
async def on_resumed():
    print("Bot 已恢复连接")

# 启用自动重连
bot.run(TOKEN, reconnect=True)
```

### Q4: Rate Limit 限制

**现象**：API 调用返回 429 错误

**解决方案**：

```python
from discord.ext.commands import BucketType

# 命令限速：每用户每 5 秒 1 次
@commands.cooldown(1, 5, BucketType.user)
@bot.command()
async def slow_command(ctx):
    await ctx.send("这条命令有限速")

# 处理限速错误
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        await ctx.send(f"⏱️ 请等待 {retry_after:.1f} 秒后再试")
    else:
        raise error
```

### Q5: 如何获取用户 ID 和频道 ID

```python
@bot.command()
async def info(ctx):
    user_id = ctx.author.id
    username = ctx.author.name
    discriminator = ctx.author.discriminator  # 如 #1234
    
    channel_id = ctx.channel.id
    channel_name = ctx.channel.name
    
    guild_id = ctx.guild.id if ctx.guild else "DM"
    guild_name = ctx.guild.name if ctx.guild else "私信"
    
    await ctx.send(f"""
    用户: {username}#{discriminator} (ID: {user_id})
    频道: {channel_name} (ID: {channel_id})
    服务器: {guild_name} (ID: {guild_id})
    """)
```

### Q6: 如何发送私信

```python
@bot.command()
async def dm(ctx, *, message):
    """发送私信给用户"""
    try:
        await ctx.author.send(f"私信内容: {message}")
        await ctx.send("✅ 私信已发送")
    except discord.Forbidden:
        await ctx.send("❌ 无法发送私信，请检查隐私设置")
```

### Q7: 如何创建线程

```python
@bot.command()
async def thread(ctx, *, name):
    """创建线程"""
    thread = await ctx.channel.create_thread(
        name=name,
        type=discord.ChannelType.public_thread
    )
    await thread.send(f"{ctx.author.mention} 创建了此线程")
```

### Q8: Bot 验证问题

**现象**：Bot 在 100 个以上服务器，无法启用 Privileged Intents

**解决方案**：

1. 在 Discord 开发者门户选择你的应用
2. 点击左侧「Bot」→「Privileged Gateway Intents」旁的「Review»
3. 填写验证表单：
   - 应用描述
   - 使用场景说明
   - 隐私政策链接（如适用）
4. 提交审核（通常 5 个工作日内回复）

---

## 参考链接

- [Discord Developer Portal](https://discord.com/developers/applications)
- [discord.py 文档](https://discordpy.readthedocs.io/)
- [Discord API 文档](https://discord.com/developers/docs/intro)
- [Discord Permissions Calculator](https://discordapi.com/permissions.html)

---

*文档版本: 1.0*  
*最后更新: 2026-03-01*
