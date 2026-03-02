# OpenClaw 渠道配置文档索引

本文档汇总了 OpenClaw 支持的所有即时通讯渠道的配置指南。

---

## 支持的渠道

| 渠道 | 文档 | 难度 | 特点 |
|------|------|------|------|
| **Telegram** | [telegram.md](./telegram.md) | ⭐ 简单 | 无需审核，快速部署 |
| **飞书 (Feishu)** | [feishu.md](./feishu.md) | ⭐⭐ 中等 | 企业集成，需管理员审批 |
| **Slack** | [slack.md](./slack.md) | ⭐⭐ 中等 | Socket Mode 支持内网部署 |
| **Discord** | [discord.md](./discord.md) | ⭐⭐ 中等 | 社区友好，支持丰富交互 |
| **WhatsApp** | [whatsapp.md](./whatsapp.md) | ⭐⭐⭐ 复杂 | 需企业验证，模板消息限制 |

---

## 快速选择指南

### 个人/小团队项目
- **推荐**：Telegram、Discord
- **原因**：配置简单，无需企业资质

### 企业/办公场景
- **推荐**：飞书、Slack
- **原因**：企业级功能，与办公套件集成

### 客户/用户触达
- **推荐**：WhatsApp
- **原因**：用户基数大，消息触达率高

---

## 配置对比

| 功能 | Telegram | 飞书 | Slack | Discord | WhatsApp |
|------|----------|------|-------|---------|----------|
| 无需企业验证 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 支持 Webhook | ✅ | ✅ | ✅ | ❌ | ✅ |
| 支持 Socket | ❌ | ❌ | ✅ | ✅ | ❌ |
| 支持私聊 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 支持群聊 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 富媒体消息 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 消息模板 | ❌ | ✅ | ❌ | ❌ | ✅ |
| 斜杠命令 | ✅ | ✅ | ✅ | ✅ | ❌ |
| 卡片消息 | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 通用配置步骤

所有渠道的配置都遵循以下流程：

1. **创建应用/Bot** - 在对应平台创建应用或 Bot
2. **获取凭证** - 获取 Token、App ID 等凭证
3. **配置权限** - 设置所需的权限范围
4. **配置 Webhook/连接** - 设置事件接收方式
5. **部署测试** - 部署并测试消息收发

---

## 环境变量模板

```bash
# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxyz1234567890

# 飞书
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Slack
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Discord
DISCORD_BOT_TOKEN=MTAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# WhatsApp
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_ACCESS_TOKEN=EAAXXXXXXXXXXXXXXXXX
```

---

## 常见问题速查

### Webhook 验证失败
- 确认服务器可公网访问
- 检查 SSL 证书有效性
- 确认正确返回 challenge/验证值

### 收不到消息
- 确认 Bot 已加入频道/群组
- 检查权限是否正确配置
- 确认事件订阅已开启

### Token 无效/过期
- 检查 Token 是否复制完整
- 确认 Token 未过期
- 检查 Token 类型是否正确

---

## 参考资源

- [OpenClaw 主文档](../README.md)
- [技能系统开发指南](../技能系统开发.md)
- [开发运维文档](../devops/security.md)

---

*文档版本: 1.0*  
*最后更新: 2026-03-01*
