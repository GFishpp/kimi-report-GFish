# Browser 工具详解

> OpenClaw 浏览器自动化工具完整文档

---

## 目录

1. [功能概述](#1-功能概述)
2. [参数详解](#2-参数详解)
3. [使用示例](#3-使用示例)
4. [最佳实践](#4-最佳实践)
5. [常见错误处理](#5-常见错误处理)

---

## 1. 功能概述

Browser 工具提供强大的浏览器控制能力，支持通过 Chrome 扩展中继或独立的 OpenClaw 管理浏览器进行网页自动化操作。

### 核心功能

| 功能类别 | 说明 |
|----------|------|
| **浏览器控制** | 启动、停止、管理浏览器实例 |
| **页面导航** | 打开 URL、前进后退、刷新页面 |
| **元素交互** | 点击、输入、悬停、选择等操作 |
| **页面分析** | 获取 DOM 快照、截图、PDF 生成 |
| **多标签管理** | 创建、切换、关闭标签页 |
| **JavaScript 执行** | 在页面上下文中运行自定义脚本 |

### 支持的浏览器模式

| 模式 | 说明 | 使用场景 |
|------|------|----------|
| `chrome` | Chrome 扩展中继模式 | 复用现有 Chrome 浏览器和标签页 |
| `openclaw` | 独立管理浏览器 | 需要隔离环境的自动化任务 |

---

## 2. 参数详解

### 2.1 核心参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `action` | string | ✅ | - | 操作类型 |
| `profile` | string | ❌ | - | 浏览器配置文件 |
| `target` | string | ❌ | `host` | 目标位置 |
| `targetId` | string | 条件 | - | 目标标签页 ID |
| `targetUrl` | string | 条件 | - | 目标 URL |
| `selector` | string | ❌ | - | CSS 选择器 |
| `ref` | string | ❌ | - | 元素引用 ID |
| `refs` | string | ❌ | `role` | 引用类型：role/aria |
| `fullPage` | boolean | ❌ | `false` | 是否完整页面截图 |
| `type` | string | ❌ | `png` | 截图格式：png/jpeg |
| `timeoutMs` | number | ❌ | `30000` | 操作超时时间（毫秒） |
| `node` | string | ❌ | - | 节点 ID（用于 node 目标） |

### 2.2 Action 类型详解

#### 浏览器管理

| Action | 说明 | 必填参数 |
|--------|------|----------|
| `status` | 获取浏览器状态 | - |
| `start` | 启动浏览器 | `profile`（推荐） |
| `stop` | 停止浏览器 | `profile` |
| `profiles` | 列出可用配置文件 | - |

#### 标签页管理

| Action | 说明 | 必填参数 |
|--------|------|----------|
| `tabs` | 列出所有标签页 | - |
| `open` | 打开新标签页 | `targetUrl` |
| `focus` | 聚焦到指定标签页 | `targetId` |
| `close` | 关闭标签页 | `targetId` |
| `navigate` | 导航到 URL | `targetUrl`, `targetId` |

#### 页面分析

| Action | 说明 | 必填参数 |
|--------|------|----------|
| `snapshot` | 获取页面 DOM 快照 | `targetId` |
| `screenshot` | 页面截图 | `targetId` |
| `pdf` | 生成 PDF | `targetId` |
| `console` | 获取控制台日志 | `targetId` |

#### 元素操作

| Action | 说明 | 必填参数 |
|--------|------|----------|
| `act` | 执行元素操作 | `targetId`, `request` |
| `upload` | 文件上传 | `targetId`, `selector`, `paths` |
| `dialog` | 处理对话框 | `targetId` |

### 2.3 Request 对象（act action）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `kind` | string | ✅ | 操作类型 |
| `ref` | string | 条件 | 元素引用（click/type 等需要） |
| `text` | string | 条件 | 输入文本（type/fill 使用） |
| `textGone` | string | ❌ | 替换文本时的原内容 |
| `key` | string | 条件 | 按键（press 使用） |
| `button` | string | ❌ | `left`/`right`/`middle` |
| `doubleClick` | boolean | ❌ | 是否双击 |
| `slowly` | boolean | ❌ | 是否慢速操作 |
| `submit` | boolean | ❌ | 是否提交表单 |
| `fn` | string | 条件 | JavaScript 函数（evaluate 使用） |
| `values` | array | 条件 | 选择值（select 使用） |
| `startRef`/`endRef` | string | 条件 | 拖拽起始/结束元素 |
| `width`/`height` | number | 条件 | 调整大小尺寸 |
| `timeMs` | number | 条件 | 等待时间（wait 使用） |

#### Request Kind 类型

| Kind | 说明 | 示例 |
|------|------|------|
| `click` | 点击元素 | `{kind:"click", ref:"e12"}` |
| `type` | 输入文本 | `{kind:"type", ref:"e15", text:"hello", submit:true}` |
| `fill` | 填充表单 | `{kind:"fill", ref:"e20", text:"value"}` |
| `press` | 按键 | `{kind:"press", key:"Enter"}` |
| `hover` | 悬停 | `{kind:"hover", ref:"e30"}` |
| `select` | 选择选项 | `{kind:"select", ref:"e40", values:["option1"]}` |
| `drag` | 拖拽 | `{kind:"drag", startRef:"e1", endRef:"e2"}` |
| `resize` | 调整大小 | `{kind:"resize", ref:"e50", width:800, height:600}` |
| `wait` | 等待 | `{kind:"wait", timeMs:2000}` |
| `evaluate` | 执行 JS | `{kind:"evaluate", fn:"() => document.title"}` |
| `close` | 关闭 | `{kind:"close"}` |

### 2.4 Snapshot 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `compact` | boolean | `false` | 紧凑模式 |
| `depth` | number | - | 遍历深度 |
| `interactive` | boolean | - | 包含交互元素 |
| `labels` | boolean | - | 包含标签 |
| `maxChars` | number | - | 最大字符数 |

---

## 3. 使用示例

### 3.1 基础示例

#### 启动浏览器并打开页面

```json
{
  "action": "start",
  "profile": "openclaw"
}
```

```json
{
  "action": "open",
  "profile": "openclaw",
  "targetUrl": "https://example.com"
}
```

#### 使用 Chrome 扩展现有标签页

```json
{
  "action": "open",
  "profile": "chrome",
  "targetUrl": "https://example.com"
}
```

⚠️ **注意**：使用 `profile: "chrome"` 时需要先在 Chrome 中点击 OpenClaw 扩展图标连接标签页。

### 3.2 页面导航示例

#### 获取页面快照

```json
{
  "action": "snapshot",
  "targetId": "tab_abc123",
  "refs": "aria",
  "compact": true
}
```

响应示例：
```json
{
  "title": "Example Domain",
  "url": "https://example.com",
  "elements": [
    {"ref": "e1", "role": "heading", "name": "Example Domain"},
    {"ref": "e2", "role": "link", "name": "More information..."}
  ]
}
```

#### 导航到新 URL

```json
{
  "action": "navigate",
  "targetId": "tab_abc123",
  "targetUrl": "https://example.com/page2"
}
```

### 3.3 元素操作示例

#### 点击元素

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "click",
    "ref": "e2",
    "button": "left",
    "slowly": true
  }
}
```

#### 输入文本并提交

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "type",
    "ref": "e10",
    "text": "搜索关键词",
    "submit": true
  }
}
```

#### 填充表单

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "fill",
    "fields": [
      {"ref": "e20", "text": "用户名"},
      {"ref": "e21", "text": "密码"}
    ]
  }
}
```

#### 选择下拉选项

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "select",
    "ref": "e30",
    "values": ["option2"]
  }
}
```

#### 悬停元素

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "hover",
    "ref": "e40"
  }
}
```

### 3.4 截图示例

#### 视口截图

```json
{
  "action": "screenshot",
  "targetId": "tab_abc123",
  "type": "png"
}
```

#### 完整页面截图

```json
{
  "action": "screenshot",
  "targetId": "tab_abc123",
  "fullPage": true,
  "type": "jpeg"
}
```

### 3.5 PDF 生成示例

```json
{
  "action": "pdf",
  "targetId": "tab_abc123"
}
```

### 3.6 JavaScript 执行示例

#### 获取页面标题

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "evaluate",
    "fn": "() => document.title"
  }
}
```

#### 获取页面所有链接

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "evaluate",
    "fn": "() => Array.from(document.querySelectorAll('a')).map(a => ({text: a.textContent, href: a.href}))"
  }
}
```

#### 滚动页面

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "evaluate",
    "fn": "() => { window.scrollTo(0, document.body.scrollHeight); return 'scrolled'; }"
  }
}
```

### 3.7 文件上传示例

```json
{
  "action": "upload",
  "targetId": "tab_abc123",
  "selector": "input[type='file']",
  "paths": ["/path/to/file.pdf"]
}
```

### 3.8 对话框处理示例

```json
{
  "action": "dialog",
  "targetId": "tab_abc123",
  "accept": true,
  "promptText": "输入的内容"
}
```

### 3.9 完整工作流示例

```javascript
// 1. 启动浏览器
{ action: "start", profile: "openclaw" }

// 2. 打开页面
{ action: "open", targetUrl: "https://example.com/login" }

// 3. 获取快照（假设返回 targetId: "tab_001"）
{ action: "snapshot", targetId: "tab_001", refs: "aria" }

// 4. 填充登录表单
{
  action: "act",
  targetId: "tab_001",
  request: {
    kind: "fill",
    fields: [
      { ref: "e5", text: "user@example.com" },
      { ref: "e6", text: "password123" }
    ]
  }
}

// 5. 点击登录按钮
{
  action: "act",
  targetId: "tab_001",
  request: { kind: "click", ref: "e10" }
}

// 6. 等待页面加载
{
  action: "act",
  targetId: "tab_001",
  request: { kind: "wait", timeMs: 2000 }
}

// 7. 截图保存
{ action: "screenshot", targetId: "tab_001", fullPage: true }

// 8. 关闭标签页
{ action: "close", targetId: "tab_001" }
```

---

## 4. 最佳实践

### 4.1 元素引用策略

| 策略 | 推荐度 | 说明 |
|------|--------|------|
| `refs: "aria"` | ⭐⭐⭐⭐⭐ | 最稳定，基于 ARIA 属性 |
| `refs: "role"` | ⭐⭐⭐⭐ | 默认策略，基于角色和名称 |
| CSS Selector | ⭐⭐⭐ | 页面结构变化时易失效 |
| XPath | ⭐⭐ | 复杂且脆弱 |

### 4.2 等待策略

```json
// ❌ 不推荐：固定等待
{ "kind": "wait", "timeMs": 5000 }

// ✅ 推荐：使用 evaluate 检查元素存在
{
  "kind": "evaluate",
  "fn": "() => new Promise(resolve => {
    const check = () => {
      if (document.querySelector('.loaded')) resolve('ready');
      else setTimeout(check, 100);
    };
    check();
  })"
}
```

### 4.3 错误处理模式

```javascript
// 包装操作带重试
async function clickWithRetry(targetId, ref, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await browserAct({
        action: "act",
        targetId,
        request: { kind: "click", ref }
      });
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      await sleep(1000);
    }
  }
}
```

### 4.4 性能优化

1. **复用浏览器实例**：不要频繁启动/停止浏览器
2. **批量操作**：使用 `fill` 一次性填充多个字段
3. **合理超时**：根据网络情况设置 `timeoutMs`
4. **快照缓存**：页面未变化时复用元素引用

### 4.5 安全注意事项

- 不要在代码中硬编码敏感信息
- 使用 `profile: "openclaw"` 进行敏感操作
- 完成后及时关闭标签页和浏览器
- 避免在公共环境使用 `profile: "chrome"`

---

## 5. 常见错误处理

### 5.1 错误代码表

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `No tab is connected` | Chrome 扩展未连接 | 点击 Chrome 工具栏的 OpenClaw 图标 |
| `TimeoutError` | 页面加载超时 | 增加 `timeoutMs` 参数 |
| `Element not found` | 元素引用失效 | 重新获取 snapshot |
| `Browser not started` | 浏览器未启动 | 先执行 `action: "start"` |
| `Navigation failed` | 导航失败 | 检查 URL 和网络 |
| `Target closed` | 标签页已关闭 | 使用有效的 targetId |
| `Evaluation failed` | JS 执行错误 | 检查 JavaScript 语法 |

### 5.2 问题排查流程

```
遇到问题 → 检查浏览器状态 (action: status)
        → 检查标签页是否存在 (action: tabs)
        → 重新获取快照 (action: snapshot)
        → 验证元素引用
        → 检查网络连接
```

### 5.3 调试技巧

#### 启用控制台日志

```json
{
  "action": "console",
  "targetId": "tab_abc123",
  "level": "all"
}
```

#### 使用 evaluate 调试

```json
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "evaluate",
    "fn": "() => {
      console.log('Debug info:', document.readyState);
      return { url: location.href, title: document.title };
    }"
  }
}
```

### 5.4 常见场景解决方案

#### 页面加载慢

```json
{
  "action": "navigate",
  "targetId": "tab_abc123",
  "targetUrl": "https://slow-site.com",
  "timeoutMs": 60000
}
```

#### 动态内容加载

```json
// 等待特定元素出现
{
  "action": "act",
  "targetId": "tab_abc123",
  "request": {
    "kind": "evaluate",
    "fn": "() => new Promise(resolve => {
      const observer = new MutationObserver(() => {
        if (document.querySelector('.dynamic-content')) {
          observer.disconnect();
          resolve('loaded');
        }
      });
      observer.observe(document.body, { childList: true, subtree: true });
    })"
  }
}
```

#### 处理弹窗

```json
// 监听并处理 alert/confirm/prompt
{
  "action": "dialog",
  "targetId": "tab_abc123",
  "accept": true
}
```

---

## 附录

### A. 快速参考卡

```bash
# 启动浏览器
{ "action": "start", "profile": "openclaw" }

# 打开页面
{ "action": "open", "targetUrl": "..." }

# 获取快照
{ "action": "snapshot", "targetId": "...", "refs": "aria" }

# 点击元素
{ "action": "act", "targetId": "...", "request": { "kind": "click", "ref": "..." } }

# 输入文本
{ "action": "act", "targetId": "...", "request": { "kind": "type", "ref": "...", "text": "..." } }

# 截图
{ "action": "screenshot", "targetId": "...", "fullPage": true }

# 生成 PDF
{ "action": "pdf", "targetId": "..." }

# 执行 JS
{ "action": "act", "targetId": "...", "request": { "kind": "evaluate", "fn": "..." } }

# 关闭标签页
{ "action": "close", "targetId": "..." }
```

### B. 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.io)
- [Playwright 文档](https://playwright.dev)（底层技术参考）
- [ARIA 规范](https://www.w3.org/WAI/ARIA/)

---

*文档版本：1.0*  
*最后更新：2026-03-01*
