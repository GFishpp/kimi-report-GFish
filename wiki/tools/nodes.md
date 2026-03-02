# Nodes 工具详解

> OpenClaw 节点控制与设备管理工具完整文档

---

## 目录

1. [功能概述](#1-功能概述)
2. [参数详解](#2-参数详解)
3. [使用示例](#3-使用示例)
4. [最佳实践](#4-最佳实践)
5. [常见错误处理](#5-常见错误处理)

---

## 1. 功能概述

Nodes 工具用于管理和控制配对的节点设备，支持远程执行、设备控制和通知推送。

### 核心功能

| 功能类别 | 说明 |
|----------|------|
| **节点发现** | 发现和配对节点设备 |
| **设备控制** | 相机、屏幕、位置等硬件控制 |
| **远程执行** | 在节点上执行命令 |
| **通知推送** | 向节点发送通知 |
| **状态监控** | 获取节点状态和信息 |

### 使用场景

| 场景 | 说明 |
|------|------|
| 远程监控 | 获取节点相机画面 |
| 设备管理 | 管理配对的手机、服务器 |
| 自动化测试 | 在真实设备上执行测试 |
| 位置服务 | 获取设备位置信息 |
| 远程通知 | 向设备推送重要通知 |
| 命令执行 | 在远程服务器上运行脚本 |

---

## 2. 参数详解

### 2.1 核心参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `action` | string | ✅ | - | 操作类型 |
| `node` | string | 条件 | - | 目标节点 ID 或名称 |
| `deviceId` | string | 条件 | - | 设备 ID |

### 2.2 Action 类型详解

#### 节点管理

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `status` | 获取所有节点状态 | - |
| `describe` | 获取节点详细信息 | `node` |
| `pending` | 列出待配对请求 | - |
| `approve` | 批准配对请求 | `deviceId` |
| `reject` | 拒绝配对请求 | `deviceId` |

#### 通知

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `notify` | 发送通知 | `node`, `title`, `body` |

#### 相机

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `camera_snap` | 拍照 | `node`, `facing`, `quality` |
| `camera_list` | 列出相机 | `node` |
| `camera_clip` | 录制视频 | `node`, `facing`, `durationMs` |

#### 屏幕

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `screen_record` | 屏幕录制 | `node`, `durationMs`, `quality` |

#### 位置

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `location_get` | 获取位置 | `node`, `desiredAccuracy` |

#### 远程执行

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `run` | 执行命令 | `node`, `command`, `timeoutMs` |
| `invoke` | 调用节点方法 | `node`, `invokeCommand`, `invokeParamsJson` |

### 2.3 各 Action 详细参数

#### status（节点状态）

| 参数 | 类型 | 说明 |
|------|------|------|
| `gatewayUrl` | string | 网关 URL |
| `gatewayToken` | string | 网关令牌 |

#### describe（节点详情）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `node` | string | ✅ | 节点 ID 或名称 |

#### pending（待配对请求）

| 参数 | 类型 | 说明 |
|------|------|------|
| `gatewayUrl` | string | 网关 URL |
| `gatewayToken` | string | 网关令牌 |

#### approve/reject（配对处理）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | ✅ | 设备 ID |
| `requestId` | string | 条件 | 请求 ID |

#### notify（发送通知）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `node` | string | ✅ | - | 节点 ID |
| `title` | string | ✅ | - | 通知标题 |
| `body` | string | ✅ | - | 通知内容 |
| `sound` | string | ❌ | - | 通知声音 |
| `priority` | string | ❌ | `active` | 优先级：passive/active/timeSensitive |
| `delivery` | string | ❌ | `auto` | 投递方式：system/overlay/auto |

优先级说明：
- `passive`：被动通知，不打扰用户
- `active`：主动通知，正常提醒
- `timeSensitive`：时效性通知，可突破勿扰模式

#### camera_snap（拍照）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `node` | string | ✅ | - | 节点 ID |
| `facing` | string | ❌ | `back` | 相机朝向：front/back/both |
| `quality` | number | ❌ | 90 | 图片质量（0-100） |
| `maxWidth` | number | ❌ | - | 最大宽度 |
| `flash` | string | ❌ | `auto` | 闪光灯：auto/on/off |

#### camera_list（列出相机）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `node` | string | ✅ | 节点 ID |

#### camera_clip（录制视频）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `node` | string | ✅ | - | 节点 ID |
| `facing` | string | ❌ | `back` | 相机朝向：front/back |
| `durationMs` | number | ❌ | 5000 | 录制时长（毫秒） |
| `quality` | number | ❌ | 80 | 视频质量（0-100） |
| `fps` | number | ❌ | 30 | 帧率 |

#### screen_record（屏幕录制）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `node` | string | ✅ | - | 节点 ID |
| `durationMs` | number | ❌ | 10000 | 录制时长（毫秒） |
| `quality` | number | ❌ | 80 | 视频质量（0-100） |
| `fps` | number | ❌ | 30 | 帧率 |
| `includeAudio` | boolean | ❌ | false | 是否包含音频 |
| `screenIndex` | number | ❌ | 0 | 屏幕索引 |

#### location_get（获取位置）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `node` | string | ✅ | - | 节点 ID |
| `desiredAccuracy` | string | ❌ | `balanced` | 精度：coarse/balanced/precise |
| `timeoutMs` | number | ❌ | 30000 | 超时时间（毫秒） |
| `maxAgeMs` | number | ❌ | 60000 | 最大缓存时间（毫秒） |

精度说明：
- `coarse`：粗略位置，省电
- `balanced`：平衡精度和耗电
- `precise`：精确位置，可能更耗电

#### run（执行命令）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `node` | string | ✅ | - | 节点 ID |
| `command` | array | ✅ | - | 命令数组 |
| `cwd` | string | ❌ | - | 工作目录 |
| `env` | array | ❌ | - | 环境变量（KEY=VALUE 格式） |
| `timeoutMs` | number | ❌ | 60000 | 超时时间（毫秒） |
| `commandTimeoutMs` | number | ❌ | - | 命令执行超时 |

#### invoke（调用方法）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `node` | string | ✅ | 节点 ID |
| `invokeCommand` | string | ✅ | 要调用的命令 |
| `invokeParamsJson` | string | ✅ | JSON 格式的参数 |
| `invokeTimeoutMs` | number | ❌ | 调用超时 |

---

## 3. 使用示例

### 3.1 节点管理示例

#### 获取所有节点状态

```json
{
  "action": "status"
}
```

响应示例：
```json
{
  "nodes": [
    {
      "id": "node_iphone_001",
      "name": "iPhone",
      "type": "mobile",
      "status": "online",
      "lastSeen": "2026-03-01T00:00:00Z",
      "capabilities": ["camera", "location", "notify"]
    },
    {
      "id": "node_server_001",
      "name": "Home Server",
      "type": "server",
      "status": "online",
      "lastSeen": "2026-03-01T00:00:00Z",
      "capabilities": ["run", "screen_record"]
    }
  ]
}
```

#### 获取节点详细信息

```json
{
  "action": "describe",
  "node": "node_iphone_001"
}
```

#### 列出待配对请求

```json
{
  "action": "pending"
}
```

#### 批准配对请求

```json
{
  "action": "approve",
  "deviceId": "device_abc123"
}
```

#### 拒绝配对请求

```json
{
  "action": "reject",
  "deviceId": "device_abc123"
}
```

### 3.2 通知示例

#### 发送基础通知

```json
{
  "action": "notify",
  "node": "node_iphone_001",
  "title": "提醒",
  "body": "会议即将开始"
}
```

#### 发送高优先级通知

```json
{
  "action": "notify",
  "node": "node_iphone_001",
  "title": "紧急",
  "body": "系统需要立即关注",
  "priority": "timeSensitive",
  "sound": "alert"
}
```

#### 发送带声音的通知

```json
{
  "action": "notify",
  "node": "node_iphone_001",
  "title": "新消息",
  "body": "您有一条新消息",
  "sound": "default"
}
```

### 3.3 相机示例

#### 拍照（后置相机）

```json
{
  "action": "camera_snap",
  "node": "node_iphone_001",
  "facing": "back",
  "quality": 90
}
```

#### 拍照（前置相机）

```json
{
  "action": "camera_snap",
  "node": "node_iphone_001",
  "facing": "front",
  "quality": 85
}
```

#### 拍照（双相机）

```json
{
  "action": "camera_snap",
  "node": "node_iphone_001",
  "facing": "both",
  "quality": 90
}
```

#### 列出可用相机

```json
{
  "action": "camera_list",
  "node": "node_iphone_001"
}
```

#### 录制视频

```json
{
  "action": "camera_clip",
  "node": "node_iphone_001",
  "facing": "back",
  "durationMs": 10000,
  "quality": 80,
  "fps": 30
}
```

### 3.4 屏幕录制示例

#### 基础屏幕录制

```json
{
  "action": "screen_record",
  "node": "node_iphone_001",
  "durationMs": 10000,
  "quality": 80
}
```

#### 带音频的屏幕录制

```json
{
  "action": "screen_record",
  "node": "node_iphone_001",
  "durationMs": 30000,
  "quality": 85,
  "includeAudio": true,
  "fps": 30
}
```

#### 多屏幕录制（服务器）

```json
{
  "action": "screen_record",
  "node": "node_server_001",
  "durationMs": 5000,
  "screenIndex": 1,
  "quality": 75
}
```

### 3.5 位置获取示例

#### 获取粗略位置

```json
{
  "action": "location_get",
  "node": "node_iphone_001",
  "desiredAccuracy": "coarse",
  "timeoutMs": 10000
}
```

#### 获取精确位置

```json
{
  "action": "location_get",
  "node": "node_iphone_001",
  "desiredAccuracy": "precise",
  "timeoutMs": 30000,
  "maxAgeMs": 0
}
```

响应示例：
```json
{
  "latitude": 39.9042,
  "longitude": 116.4074,
  "altitude": 50.5,
  "accuracy": 10.0,
  "timestamp": "2026-03-01T00:00:00Z"
}
```

### 3.6 远程命令执行示例

#### 执行简单命令

```json
{
  "action": "run",
  "node": "node_server_001",
  "command": ["ls", "-la"],
  "timeoutMs": 30000
}
```

#### 指定工作目录

```json
{
  "action": "run",
  "node": "node_server_001",
  "command": ["git", "status"],
  "cwd": "/path/to/repo",
  "timeoutMs": 30000
}
```

#### 设置环境变量

```json
{
  "action": "run",
  "node": "node_server_001",
  "command": ["python", "script.py"],
  "env": [
    "API_KEY=secret_key",
    "ENV=production",
    "DEBUG=false"
  ],
  "timeoutMs": 60000
}
```

#### 执行复杂命令

```json
{
  "action": "run",
  "node": "node_server_001",
  "command": ["bash", "-c", "cd /app && npm install && npm run build"],
  "timeoutMs": 300000
}
```

### 3.7 方法调用示例

#### 调用节点方法

```json
{
  "action": "invoke",
  "node": "node_iphone_001",
  "invokeCommand": "getBatteryLevel",
  "invokeParamsJson": "{}",
  "invokeTimeoutMs": 10000
}
```

#### 带参数的方法调用

```json
{
  "action": "invoke",
  "node": "node_iphone_001",
  "invokeCommand": "setBrightness",
  "invokeParamsJson": "{\"level\": 0.8}",
  "invokeTimeoutMs": 5000
}
```

### 3.8 完整工作流示例

#### 远程监控流程

```javascript
// 1. 获取节点状态
const status = await nodes({ action: "status" });

// 2. 发送开始通知
await nodes({
  action: "notify",
  node: "node_iphone_001",
  title: "监控开始",
  body: "开始录制监控视频"
});

// 3. 拍照
const photo = await nodes({
  action: "camera_snap",
  node: "node_iphone_001",
  facing: "back",
  quality": 90
});

// 4. 录制视频
const video = await nodes({
  action: "camera_clip",
  node: "node_iphone_001",
  facing: "back",
  durationMs: 30000,
  quality: 80
});

// 5. 获取位置
const location = await nodes({
  action: "location_get",
  node: "node_iphone_001",
  desiredAccuracy: "precise"
});

// 6. 发送完成通知
await nodes({
  action: "notify",
  node: "node_iphone_001",
  title: "监控完成",
  body: "监控数据已收集完成"
});
```

#### 远程服务器维护

```javascript
// 1. 检查系统状态
const systemStatus = await nodes({
  action: "run",
  node: "node_server_001",
  command: ["df", "-h"]
});

// 2. 清理临时文件
await nodes({
  action: "run",
  node: "node_server_001",
  command: ["find", "/tmp", "-type", "f", "-mtime", "+7", "-delete"]
});

// 3. 更新应用
await nodes({
  action: "run",
  node: "node_server_001",
  command: ["bash", "-c", "cd /app && git pull && docker-compose up -d"],
  timeoutMs: 300000
});

// 4. 发送通知
await nodes({
  action: "notify",
  node: "node_iphone_001",
  title: "维护完成",
  body: "服务器维护已成功完成"
});
```

---

## 4. 最佳实践

### 4.1 节点选择策略

| 场景 | 推荐节点类型 | 说明 |
|------|--------------|------|
| 移动通知 | 手机节点 | iOS/Android 设备 |
| 服务器操作 | 服务器节点 | Linux/Windows 服务器 |
| 监控录制 | 任意在线节点 | 根据位置选择 |
| 位置服务 | 手机/平板 | 带 GPS 的设备 |

### 4.2 权限管理

1. **首次配对**：仔细验证设备身份
2. **权限审查**：定期检查已配对节点
3. **及时撤销**：不再使用的节点及时移除
4. **最小权限**：只授予必要的操作权限

### 4.3 相机使用建议

| 场景 | 设置 | 说明 |
|------|------|------|
| 文档拍摄 | quality: 95, facing: back | 高清晰度 |
| 监控录像 | quality: 75, fps: 15 | 平衡质量和文件大小 |
| 快速预览 | quality: 60 | 小文件快速传输 |
| 自拍 | facing: front | 前置相机 |

### 4.4 位置获取策略

| 精度需求 | 设置 | 适用场景 |
|----------|------|----------|
| 城市级 | coarse | 天气、时区 |
| 街区级 | balanced | 附近服务 |
| 米级 | precise | 导航、追踪 |

### 4.5 命令执行安全

```bash
# ❌ 不推荐：直接拼接用户输入
cmd = "process " + userInput

# ✅ 推荐：使用数组形式，避免注入
command: ["process", "--input", userInput]

# ✅ 推荐：验证和清理输入
command: ["process", "--input", sanitize(userInput)]
```

### 4.6 错误处理和重试

```javascript
async function safeNodeOperation(node, operation, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await operation();
    } catch (err) {
      if (err.message.includes("Node not found")) {
        throw err; // 不重试节点不存在的情况
      }
      if (i === maxRetries - 1) throw err;
      
      console.log(`Retry ${i + 1}/${maxRetries}...`);
      await sleep(1000 * Math.pow(2, i)); // 指数退避
    }
  }
}
```

### 4.7 资源释放

```javascript
// 录制完成后确保资源释放
async function recordWithCleanup(node, options) {
  try {
    const result = await nodes({
      action: "camera_clip",
      node,
      ...options
    });
    return result;
  } finally {
    // 确保相机资源释放
    await nodes({
      action: "invoke",
      node,
      invokeCommand: "releaseCamera",
      invokeParamsJson: "{}"
    }).catch(() => {}); // 忽略清理错误
  }
}
```

---

## 5. 常见错误处理

### 5.1 错误代码表

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Node not found` | 节点未配对 | 检查节点 ID 或重新配对 |
| `Permission denied` | 无权限 | 请求节点授权 |
| `Device offline` | 设备离线 | 检查网络连接 |
| `Camera not available` | 相机被占用 | 关闭其他使用相机的应用 |
| `Location unavailable` | 定位服务关闭 | 开启设备定位服务 |
| `Command failed` | 命令执行失败 | 检查命令语法和权限 |
| `Timeout` | 操作超时 | 增加 timeoutMs 参数 |
| `Not supported` | 节点不支持该操作 | 检查节点能力列表 |

### 5.2 问题排查流程

```
遇到问题 → 检查节点状态 (status)
        → 确认节点在线
        → 检查操作权限
        → 验证参数格式
        → 查看详细错误信息
```

### 5.3 调试技巧

#### 检查节点能力

```json
{
  "action": "describe",
  "node": "node_xxx"
}
```

#### 测试基本连接

```json
{
  "action": "notify",
  "node": "node_xxx",
  "title": "测试",
  "body": "连接测试"
}
```

#### 检查命令可用性

```json
{
  "action": "run",
  "node": "node_server_001",
  "command": ["which", "command_name"]
}
```

### 5.4 常见场景解决方案

#### 节点离线

```javascript
// 1. 检查状态
const status = await nodes({ action: "status" });

// 2. 如果离线，发送通知提醒
if (node.status === "offline") {
  // 使用其他节点发送通知
  await nodes({
    action: "notify",
    node: "backup_node",
    title: "节点离线",
    body: `${node.name} 已离线`
  });
}
```

#### 相机被占用

```javascript
// 重试机制
async function captureWithRetry(node, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await nodes({
        action: "camera_snap",
        node,
        ...options
      });
    } catch (err) {
      if (!err.message.includes("Camera not available")) throw err;
      if (i === maxRetries - 1) throw err;
      
      console.log("Camera busy, waiting...");
      await sleep(2000);
    }
  }
}
```

#### 位置获取失败

```javascript
// 降级策略
async function getLocationWithFallback(node) {
  try {
    // 先尝试精确位置
    return await nodes({
      action: "location_get",
      node,
      desiredAccuracy: "precise",
      timeoutMs: 30000
    });
  } catch (err) {
    console.log("Precise location failed, trying coarse...");
    
    // 降级到粗略位置
    return await nodes({
      action: "location_get",
      node,
      desiredAccuracy: "coarse",
      timeoutMs: 10000
    });
  }
}
```

#### 命令执行超时

```javascript
// 使用合适的超时时间
await nodes({
  action: "run",
  node: "node_server_001",
  command: ["long-running-task"],
  timeoutMs: 600000  // 10 分钟
});
```

---

## 附录

### A. 快速参考卡

```bash
# 节点状态
{ "action": "status" }
{ "action": "describe", "node": "..." }

# 配对管理
{ "action": "pending" }
{ "action": "approve", "deviceId": "..." }
{ "action": "reject", "deviceId": "..." }

# 通知
{ "action": "notify", "node": "...", "title": "...", "body": "..." }

# 相机
{ "action": "camera_snap", "node": "...", "facing": "back" }
{ "action": "camera_list", "node": "..." }
{ "action": "camera_clip", "node": "...", "durationMs": 10000 }

# 屏幕录制
{ "action": "screen_record", "node": "...", "durationMs": 10000 }

# 位置
{ "action": "location_get", "node": "...", "desiredAccuracy": "precise" }

# 远程执行
{ "action": "run", "node": "...", "command": ["ls", "-la"] }
{ "action": "invoke", "node": "...", "invokeCommand": "...", "invokeParamsJson": "..." }
```

### B. 节点能力列表

| 能力 | 说明 | 适用节点 |
|------|------|----------|
| `camera` | 相机控制 | 手机、平板 |
| `location` | 位置服务 | 手机、平板 |
| `notify` | 通知推送 | 手机、平板、桌面 |
| `run` | 命令执行 | 服务器、桌面 |
| `screen_record` | 屏幕录制 | 手机、平板、桌面 |

### C. 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.io)
- [iOS 通知指南](https://developer.apple.com/documentation/usernotifications)
- [Android 通知指南](https://developer.android.com/guide/topics/ui/notifiers/notifications)

---

*文档版本：1.0*  
*最后更新：2026-03-01*
