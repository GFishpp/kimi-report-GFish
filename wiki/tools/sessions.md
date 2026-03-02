# Sessions 工具详解

> OpenClaw 会话管理与子代理工具完整文档

---

## 目录

1. [功能概述](#1-功能概述)
2. [参数详解](#2-参数详解)
3. [使用示例](#3-使用示例)
4. [最佳实践](#4-最佳实践)
5. [常见错误处理](#5-常见错误处理)

---

## 1. 功能概述

Sessions 工具用于管理执行会话，支持后台任务、子代理管理和交互式操作。

### 核心功能

| 功能类别 | 说明 |
|----------|------|
| **会话列表** | 查看所有活动会话 |
| **会话控制** | 发送输入、获取日志、终止会话 |
| **后台任务** | 管理长时间运行的任务 |
| **子代理** | 创建和管理子代理会话 |
| **交互操作** | 与会话进行实时交互 |

### 使用场景

| 场景 | 说明 |
|------|------|
| 长时间任务 | 运行需要数小时的脚本 |
| 交互式程序 | 控制需要输入的 CLI 工具 |
| 子代理管理 | 创建子代理执行独立任务 |
| 日志监控 | 实时查看任务输出 |
| 会话恢复 | 重新连接到已存在的会话 |

---

## 2. 参数详解

### 2.1 核心参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `action` | string | ✅ | - | 操作类型 |
| `sessionId` | string | 条件 | - | 会话 ID（除 list 外必填） |

### 2.2 Action 类型详解

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `list` | 列出所有会话 | - |
| `poll` | 轮询会话状态 | `sessionId` |
| `log` | 获取会话日志 | `sessionId`, `offset`, `limit` |
| `write` | 向会话写入数据 | `sessionId`, `data`, `eof` |
| `send-keys` | 发送按键序列 | `sessionId`, `keys`, `hex`, `literal` |
| `submit` | 提交输入 | `sessionId` |
| `paste` | 粘贴文本 | `sessionId`, `text`, `bracketed` |
| `kill` | 终止会话 | `sessionId` |

### 2.3 各 Action 详细参数

#### list（列会话）

| 参数 | 类型 | 说明 |
|------|------|------|
| `status` | string | 过滤状态：running/stopped/all |
| `type` | string | 过滤类型：exec/subagent/all |

#### poll（轮询状态）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sessionId` | string | ✅ | 会话 ID |

#### log（获取日志）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sessionId` | string | ✅ | - | 会话 ID |
| `offset` | number | ❌ | 0 | 起始行偏移 |
| `limit` | number | ❌ | 100 | 返回行数限制 |
| `follow` | boolean | ❌ | false | 是否持续跟踪 |

#### write（写入数据）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sessionId` | string | ✅ | - | 会话 ID |
| `data` | string | ✅ | - | 要写入的数据 |
| `eof` | boolean | ❌ | false | 写入后关闭 stdin |

#### send-keys（发送按键）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `sessionId` | string | ✅ | 会话 ID |
| `keys` | array | 条件 | 按键名称数组 |
| `hex` | array | 条件 | 十六进制按键码 |
| `literal` | string | 条件 | 字面量字符串 |

支持的按键名称：
- 特殊键：`Enter`, `Return`, `Tab`, `Backspace`, `Delete`, `Escape`, `Space`
- 方向键：`Up`, `Down`, `Left`, `Right`
- 功能键：`F1`-`F12`
- 修饰键：`Ctrl`, `Alt`, `Shift`, `Meta`
- 组合键：`Ctrl+c`, `Ctrl+d`, `Ctrl+z`

#### paste（粘贴文本）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sessionId` | string | ✅ | - | 会话 ID |
| `text` | string | ✅ | - | 要粘贴的文本 |
| `bracketed` | boolean | ❌ | false | 使用括号模式 |

#### kill（终止会话）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `sessionId` | string | ✅ | - | 会话 ID |
| `signal` | string | ❌ | `TERM` | 信号：TERM/KILL/INT |

### 2.4 会话状态

| 状态 | 说明 |
|------|------|
| `running` | 正在运行 |
| `stopped` | 已停止 |
| `error` | 出错 |
| `completed` | 已完成 |

### 2.5 会话类型

| 类型 | 说明 |
|------|------|
| `exec` | 命令执行会话 |
| `subagent` | 子代理会话 |
| `interactive` | 交互式会话 |

---

## 3. 使用示例

### 3.1 基础示例

#### 列出所有会话

```json
{
  "action": "list"
}
```

响应示例：
```json
{
  "sessions": [
    {
      "id": "session_abc123",
      "type": "exec",
      "status": "running",
      "command": "python long_script.py",
      "startedAt": "2026-03-01T00:00:00Z",
      "pid": 12345
    },
    {
      "id": "session_def456",
      "type": "subagent",
      "status": "running",
      "name": "data-processor",
      "startedAt": "2026-03-01T01:00:00Z"
    }
  ]
}
```

#### 过滤会话列表

```json
{
  "action": "list",
  "status": "running",
  "type": "exec"
}
```

### 3.2 日志管理示例

#### 获取会话日志

```json
{
  "action": "log",
  "sessionId": "session_abc123",
  "offset": 0,
  "limit": 50
}
```

响应示例：
```json
{
  "lines": [
    {"timestamp": "2026-03-01T00:00:01Z", "level": "info", "message": "Starting process..."},
    {"timestamp": "2026-03-01T00:00:02Z", "level": "info", "message": "Processing item 1/100"},
    {"timestamp": "2026-03-01T00:00:05Z", "level": "warn", "message": "Slow response detected"}
  ],
  "totalLines": 150,
  "hasMore": true
}
```

#### 获取最新日志

```json
{
  "action": "log",
  "sessionId": "session_abc123",
  "offset": 100,
  "limit": 50
}
```

### 3.3 数据写入示例

#### 向会话发送命令

```json
{
  "action": "write",
  "sessionId": "session_abc123",
  "data": "status\n"
}
```

#### 发送多行数据

```json
{
  "action": "write",
  "sessionId": "session_abc123",
  "data": "line 1\nline 2\nline 3\n"
}
```

#### 发送数据并关闭输入

```json
{
  "action": "write",
  "sessionId": "session_abc123",
  "data": "final input",
  "eof": true
}
```

### 3.4 按键发送示例

#### 发送回车键

```json
{
  "action": "send-keys",
  "sessionId": "session_abc123",
  "keys": ["Enter"]
}
```

#### 发送组合键

```json
{
  "action": "send-keys",
  "sessionId": "session_abc123",
  "keys": ["Ctrl+c"]
}
```

#### 发送多个按键

```json
{
  "action": "send-keys",
  "sessionId": "session_abc123",
  "keys": ["Up", "Up", "Enter"]
}
```

#### 发送十六进制码

```json
{
  "action": "send-keys",
  "sessionId": "session_abc123",
  "hex": ["0x03"]
}
```

#### 发送字面量

```json
{
  "action": "send-keys",
  "sessionId": "session_abc123",
  "literal": "y\n"
}
```

### 3.5 粘贴文本示例

#### 基础粘贴

```json
{
  "action": "paste",
  "sessionId": "session_abc123",
  "text": "This is a long text to paste"
}
```

#### 使用括号模式

```json
{
  "action": "paste",
  "sessionId": "session_abc123",
  "text": "Special [characters] (here)",
  "bracketed": true
}
```

### 3.6 会话终止示例

#### 正常终止

```json
{
  "action": "kill",
  "sessionId": "session_abc123"
}
```

#### 强制终止

```json
{
  "action": "kill",
  "sessionId": "session_abc123",
  "signal": "KILL"
}
```

#### 发送中断信号

```json
{
  "action": "kill",
  "sessionId": "session_abc123",
  "signal": "INT"
}
```

### 3.7 完整工作流示例

#### 交互式程序控制

```javascript
// 1. 启动交互式程序（通过 exec 工具）
// sessionId: "session_interactive"

// 2. 等待程序启动
{
  action: "poll",
  sessionId: "session_interactive"
}

// 3. 查看初始输出
{
  action: "log",
  sessionId: "session_interactive",
  limit: 20
}

// 4. 发送输入
{
  action: "write",
  sessionId: "session_interactive",
  data: "option 1\n"
}

// 5. 等待处理
{
  action: "log",
  sessionId: "session_interactive",
  offset: 20,
  limit: 10
}

// 6. 发送确认
{
  action: "send-keys",
  sessionId: "session_interactive",
  keys: ["y", "Enter"]
}

// 7. 完成任务
{
  action: "write",
  sessionId: "session_interactive",
  data: "quit\n",
  eof: true
}

// 8. 等待完成并获取最终日志
{
  action: "log",
  sessionId: "session_interactive",
  offset: 30
}

// 9. 清理
{
  action: "kill",
  sessionId: "session_interactive"
}
```

#### 监控长时间运行任务

```javascript
// 监控循环
async function monitorSession(sessionId, interval = 5000) {
  while (true) {
    // 获取状态
    const status = await process({
      action: "poll",
      sessionId
    });
    
    if (status.status === "completed" || status.status === "stopped") {
      console.log("Task finished");
      break;
    }
    
    // 获取新日志
    const logs = await process({
      action: "log",
      sessionId,
      offset: currentOffset,
      limit: 100
    });
    
    // 处理日志...
    currentOffset += logs.lines.length;
    
    // 等待下次检查
    await sleep(interval);
  }
}
```

---

## 4. 最佳实践

### 4.1 会话生命周期管理

```
创建会话 → 监控状态 → 交互操作 → 获取结果 → 终止清理
    ↑___________________________________________|
```

### 4.2 日志处理策略

| 策略 | 适用场景 | 实现方式 |
|------|----------|----------|
| 轮询 | 实时监控 | 定期调用 `log` action |
| 增量 | 大日志处理 | 使用 `offset` 参数 |
| 批量 | 事后分析 | 一次性获取全部日志 |

### 4.3 输入发送模式

| 模式 | 适用场景 | 示例 |
|------|----------|------|
| `write` | 发送命令/数据 | 发送配置、输入参数 |
| `send-keys` | 模拟按键 | 快捷键、导航 |
| `paste` | 大段文本 | 粘贴代码、长文本 |

### 4.4 错误处理模式

```javascript
async function safeSessionOperation(sessionId, operation) {
  try {
    // 检查会话是否存在
    const status = await process({
      action: "poll",
      sessionId
    });
    
    if (status.status === "stopped") {
      throw new Error("Session already stopped");
    }
    
    // 执行操作
    return await operation();
    
  } catch (err) {
    if (err.message.includes("Session not found")) {
      console.error("Session does not exist");
    } else if (err.message.includes("Session already ended")) {
      console.error("Session has ended");
    } else {
      console.error("Operation failed:", err);
    }
    throw err;
  }
}
```

### 4.5 资源清理

```javascript
async function cleanupSession(sessionId) {
  try {
    // 尝试优雅终止
    await process({
      action: "kill",
      sessionId,
      signal: "TERM"
    });
    
    // 等待终止
    await sleep(2000);
    
    // 检查状态
    const status = await process({
      action: "poll",
      sessionId
    });
    
    // 如果还在运行，强制终止
    if (status.status === "running") {
      await process({
        action: "kill",
        sessionId,
        signal: "KILL"
      });
    }
  } catch (err) {
    // 会话可能已不存在，忽略错误
    console.log("Cleanup completed or session already gone");
  }
}
```

### 4.6 性能优化

1. **批量获取日志**：使用合适的 `limit` 避免频繁调用
2. **合理轮询间隔**：根据任务特性设置 poll 间隔
3. **及时清理**：用完会话后立即终止
4. **避免阻塞**：长时间操作使用后台会话

---

## 5. 常见错误处理

### 5.1 错误代码表

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Session not found` | 会话 ID 错误 | 检查 sessionId 是否正确 |
| `Session already ended` | 会话已结束 | 创建新会话 |
| `Write failed` | 写入失败 | 检查会话状态和权限 |
| `Invalid keys` | 按键名称无效 | 检查按键名称拼写 |
| `Permission denied` | 权限不足 | 检查操作权限 |
| `Session is not interactive` | 会话不支持交互 | 使用交互式会话类型 |

### 5.2 问题排查流程

```
遇到问题 → 检查会话是否存在 (list/poll)
        → 检查会话状态
        → 查看最近日志
        → 验证操作参数
        → 检查权限
```

### 5.3 调试技巧

#### 检查会话状态

```json
{
  "action": "poll",
  "sessionId": "session_abc123"
}
```

#### 查看完整日志

```json
{
  "action": "log",
  "sessionId": "session_abc123",
  "offset": 0,
  "limit": 1000
}
```

#### 测试输入响应

```json
// 先发送测试输入
{
  "action": "write",
  "sessionId": "session_abc123",
  "data": "echo 'test'\n"
}

// 然后查看输出
{
  "action": "log",
  "sessionId": "session_abc123",
  "limit": 10
}
```

### 5.4 常见场景解决方案

#### 会话无响应

```json
// 1. 检查状态
{ "action": "poll", "sessionId": "..." }

// 2. 发送中断信号
{ "action": "kill", "sessionId": "...", "signal": "INT" }

// 3. 如果仍无响应，强制终止
{ "action": "kill", "sessionId": "...", "signal": "KILL" }
```

#### 输入不生效

```json
// 确保发送换行符
{
  "action": "write",
  "sessionId": "...",
  "data": "command\n"
}

// 或使用 send-keys 发送 Enter
{
  "action": "send-keys",
  "sessionId": "...",
  "keys": ["Enter"]
}
```

#### 日志获取不完整

```json
// 使用 offset 获取增量日志
{
  "action": "log",
  "sessionId": "...",
  "offset": lastOffset,
  "limit": 100
}
```

---

## 附录

### A. 快速参考卡

```bash
# 列会话
{ "action": "list" }
{ "action": "list", "status": "running" }

# 查状态
{ "action": "poll", "sessionId": "..." }

# 看日志
{ "action": "log", "sessionId": "...", "offset": 0, "limit": 100 }

# 写数据
{ "action": "write", "sessionId": "...", "data": "..." }

# 发按键
{ "action": "send-keys", "sessionId": "...", "keys": ["Enter"] }
{ "action": "send-keys", "sessionId": "...", "keys": ["Ctrl+c"] }

# 粘贴文本
{ "action": "paste", "sessionId": "...", "text": "..." }

# 终止会话
{ "action": "kill", "sessionId": "..." }
```

### B. 按键参考

| 按键 | 名称 |
|------|------|
| Enter | `Enter`, `Return` |
| Tab | `Tab` |
| Backspace | `Backspace` |
| Delete | `Delete` |
| Escape | `Escape` |
| Space | `Space` |
| 方向键 | `Up`, `Down`, `Left`, `Right` |
| 功能键 | `F1`-`F12` |
| Ctrl+C | `Ctrl+c` |
| Ctrl+D | `Ctrl+d` |
| Ctrl+Z | `Ctrl+z` |

### C. 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.io)
- [POSIX 信号](https://man7.org/linux/man-pages/man7/signal.7.html)
- [终端控制序列](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)

---

*文档版本：1.0*  
*最后更新：2026-03-01*
