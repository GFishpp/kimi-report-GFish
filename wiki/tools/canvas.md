# Canvas 工具详解

> OpenClaw 画布控制与 A2UI 工具完整文档

---

## 目录

1. [功能概述](#1-功能概述)
2. [参数详解](#2-参数详解)
3. [使用示例](#3-使用示例)
4. [最佳实践](#4-最佳实践)
5. [常见错误处理](#5-常见错误处理)

---

## 1. 功能概述

Canvas 工具用于控制节点画布，支持渲染 UI、执行 JavaScript、捕获快照等功能。

### 核心功能

| 功能类别 | 说明 |
|----------|------|
| **画布展示** | 在节点上展示可视化内容 |
| **A2UI 推送** | 将 AI 生成的 UI 推送到画布 |
| **快照捕获** | 获取画布当前状态的截图 |
| **JavaScript 执行** | 在画布上下文中运行脚本 |
| **导航控制** | 控制画布的页面导航 |

### 使用场景

| 场景 | 说明 |
|------|------|
| 数据可视化 | 展示图表、仪表盘 |
| 实时预览 | 预览生成的 HTML/CSS/JS |
| 远程演示 | 在节点设备上展示内容 |
| UI 测试 | 测试和调试用户界面 |
| 截图生成 | 生成特定尺寸的图像 |

---

## 2. 参数详解

### 2.1 核心参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `action` | string | ✅ | - | 操作类型 |
| `node` | string | 条件 | - | 目标节点 ID 或名称 |
| `target` | string | ❌ | - | 目标标识 |

### 2.2 Action 类型详解

| Action | 说明 | 常用参数 |
|--------|------|----------|
| `present` | 展示画布 | `width`, `height`, `x`, `y` |
| `hide` | 隐藏画布 | - |
| `navigate` | 导航到指定 URL | `url` |
| `eval` | 执行 JavaScript 代码 | `javaScript` |
| `snapshot` | 捕获画布快照 | `outputFormat`, `quality` |
| `a2ui_push` | 推送 A2UI 内容到画布 | `jsonl`, `jsonlPath` |
| `a2ui_reset` | 重置 A2UI 状态 | - |

### 2.3 各 Action 详细参数

#### present（展示画布）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `width` | number | ❌ | 1280 | 画布宽度（像素） |
| `height` | number | ❌ | 720 | 画布高度（像素） |
| `x` | number | ❌ | 0 | X 坐标位置 |
| `y` | number | ❌ | 0 | Y 坐标位置 |
| `gatewayUrl` | string | ❌ | - | 网关 URL |
| `gatewayToken` | string | ❌ | - | 网关令牌 |

#### navigate（导航）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 要导航的 URL |

#### eval（执行 JavaScript）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `javaScript` | string | ✅ | 要执行的 JavaScript 代码 |
| `timeoutMs` | number | ❌ | 执行超时时间 |

#### snapshot（捕获快照）

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `outputFormat` | string | ❌ | `png` | 输出格式：png/jpg/jpeg |
| `quality` | number | ❌ | 90 | JPEG 质量（0-100） |
| `width` | number | ❌ | - | 输出宽度 |
| `height` | number | ❌ | - | 输出高度 |
| `delayMs` | number | ❌ | 0 | 捕获前延迟（毫秒） |

#### a2ui_push（推送 A2UI）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `jsonl` | string | 条件 | A2UI JSONL 数据字符串 |
| `jsonlPath` | string | 条件 | A2UI JSONL 文件路径 |

> 注意：`jsonl` 和 `jsonlPath` 二选一

### 2.4 A2UI JSONL 格式

A2UI 使用 JSON Lines 格式，每行一个 JSON 对象：

```jsonl
{"type": "component", "name": "Container", "props": {"layout": "vertical"}}
{"type": "component", "name": "Text", "props": {"content": "Hello World"}}
{"type": "component", "name": "Button", "props": {"label": "Click Me", "onClick": "handleClick"}}
```

#### 支持的组件类型

| 组件 | 说明 | 常用属性 |
|------|------|----------|
| `Container` | 容器 | `layout`, `padding`, `gap` |
| `Text` | 文本 | `content`, `size`, `color` |
| `Button` | 按钮 | `label`, `variant`, `onClick` |
| `Input` | 输入框 | `placeholder`, `value`, `onChange` |
| `Image` | 图片 | `src`, `alt`, `width`, `height` |
| `Chart` | 图表 | `type`, `data`, `options` |
| `Table` | 表格 | `columns`, `data`, `pagination` |

---

## 3. 使用示例

### 3.1 基础示例

#### 展示画布

```json
{
  "action": "present",
  "node": "node_001",
  "width": 1920,
  "height": 1080
}
```

#### 隐藏画布

```json
{
  "action": "hide",
  "node": "node_001"
}
```

### 3.2 导航示例

#### 导航到网页

```json
{
  "action": "navigate",
  "node": "node_001",
  "url": "https://example.com/dashboard"
}
```

#### 导航到本地文件

```json
{
  "action": "navigate",
  "node": "node_001",
  "url": "file:///path/to/local/file.html"
}
```

### 3.3 JavaScript 执行示例

#### 修改页面样式

```json
{
  "action": "eval",
  "node": "node_001",
  "javaScript": "document.body.style.backgroundColor = '#f0f0f0';"
}
```

#### 获取页面信息

```json
{
  "action": "eval",
  "node": "node_001",
  "javaScript": "JSON.stringify({title: document.title, url: location.href, width: window.innerWidth, height: window.innerHeight})"
}
```

#### 操作 DOM 元素

```json
{
  "action": "eval",
  "node": "node_001",
  "javaScript": "
    const element = document.getElementById('myElement');
    if (element) {
      element.textContent = 'Updated content';
      element.style.color = 'red';
    }
  "
}
```

#### 异步操作

```json
{
  "action": "eval",
  "node": "node_001",
  "javaScript": "
    (async () => {
      const response = await fetch('https://api.example.com/data');
      const data = await response.json();
      return JSON.stringify(data);
    })()
  ",
  "timeoutMs": 10000
}
```

### 3.4 快照捕获示例

#### 基础截图

```json
{
  "action": "snapshot",
  "node": "node_001",
  "outputFormat": "png"
}
```

#### 高质量 JPEG

```json
{
  "action": "snapshot",
  "node": "node_001",
  "outputFormat": "jpeg",
  "quality": 95
}
```

#### 带延迟的截图（等待渲染完成）

```json
{
  "action": "snapshot",
  "node": "node_001",
  "outputFormat": "png",
  "delayMs": 2000
}
```

#### 指定尺寸截图

```json
{
  "action": "snapshot",
  "node": "node_001",
  "outputFormat": "png",
  "width": 800,
  "height": 600
}
```

### 3.5 A2UI 推送示例

#### 推送简单 UI

```json
{
  "action": "a2ui_push",
  "node": "node_001",
  "jsonl": "{\"type\":\"component\",\"name\":\"Text\",\"props\":{\"content\":\"Hello from A2UI\"}}"
}
```

#### 推送复杂布局

```json
{
  "action": "a2ui_push",
  "node": "node_001",
  "jsonl": "{\"type\":\"component\",\"name\":\"Container\",\"props\":{\"layout\":\"vertical\",\"gap\":16}}\n{\"type\":\"component\",\"name\":\"Text\",\"props\":{\"content\":\"Dashboard\",\"size\":\"large\"}}\n{\"type\":\"component\",\"name\":\"Button\",\"props\":{\"label\":\"Refresh\",\"variant\":\"primary\"}}"
}
```

#### 从文件推送

```json
{
  "action": "a2ui_push",
  "node": "node_001",
  "jsonlPath": "/path/to/ui-definition.jsonl"
}
```

### 3.6 完整工作流示例

#### 创建数据仪表盘

```javascript
// 1. 展示画布
{
  action: "present",
  node: "display_node",
  width: 1920,
  height: 1080
}

// 2. 推送仪表盘 UI
{
  action: "a2ui_push",
  node: "display_node",
  jsonl: `
    {"type": "component", "name": "Container", "props": {"layout": "grid", "columns": 3}}
    {"type": "component", "name": "Card", "props": {"title": "总用户数", "value": "12,345"}}
    {"type": "component", "name": "Card", "props": {"title": "日活跃用户", "value": "3,456"}}
    {"type": "component", "name": "Card", "props": {"title": "转化率", "value": "23.5%"}}
    {"type": "component", "name": "Chart", "props": {"type": "line", "data": [...]}}
  `
}

// 3. 等待渲染
{
  action: "eval",
  node: "display_node",
  request: { kind: "wait", timeMs: 1000 }
}

// 4. 截图保存
{
  action: "snapshot",
  node: "display_node",
  outputFormat: "png",
  quality: 95
}

// 5. 隐藏画布
{
  action: "hide",
  node: "display_node"
}
```

#### 网页内容截图

```javascript
// 1. 展示画布
{ action: "present", node: "node_001", width: 1280, height: 800 }

// 2. 导航到目标页面
{ action: "navigate", node: "node_001", url: "https://example.com" }

// 3. 等待页面加载（通过 JS 检查）
{
  action: "eval",
  node: "node_001",
  javaScript: "
    () => new Promise(resolve => {
      if (document.readyState === 'complete') resolve('loaded');
      else window.addEventListener('load', () => resolve('loaded'));
    })
  ",
  timeoutMs: 30000
}

// 4. 执行页面操作（如滚动）
{
  action: "eval",
  node: "node_001",
  javaScript: "window.scrollTo(0, 500)"
}

// 5. 截图
{ action: "snapshot", node: "node_001", outputFormat: "jpeg", quality: 90 }

// 6. 清理
{ action: "hide", node: "node_001" }
```

---

## 4. 最佳实践

### 4.1 画布尺寸选择

| 用途 | 推荐尺寸 | 说明 |
|------|----------|------|
| 移动端预览 | 375×667 | iPhone SE 尺寸 |
| 平板预览 | 768×1024 | iPad 尺寸 |
| 桌面网页 | 1920×1080 | 标准 Full HD |
| 社交媒体 | 1200×630 | Open Graph 推荐 |
| 文档截图 | 1440×900 | 常见文档宽度 |

### 4.2 延迟策略

```json
// ❌ 不推荐：固定延迟可能不够或过多
{ "delayMs": 5000 }

// ✅ 推荐：使用 eval 检查渲染完成
{
  "action": "eval",
  "javaScript": "
    () => new Promise(resolve => {
      const check = () => {
        const element = document.querySelector('.chart-loaded');
        if (element) resolve('ready');
        else setTimeout(check, 100);
      };
      check();
      setTimeout(() => resolve('timeout'), 30000); // 最大等待 30s
    })
  "
}
```

### 4.3 A2UI 性能优化

1. **分批推送**：大量组件时分批推送
2. **避免频繁更新**：合并多次更新为一次
3. **使用合适组件**：选择性能优化的组件
4. **清理资源**：使用 `a2ui_reset` 重置状态

### 4.4 截图质量设置

| 用途 | 格式 | 质量 | 说明 |
|------|------|------|------|
| 存档 | PNG | - | 无损，文件大 |
| 网页展示 | JPEG | 85 | 平衡质量和大小 |
| 打印 | JPEG | 95 | 高质量 |
| 缩略图 | JPEG | 60 | 小文件 |

### 4.5 错误处理模式

```javascript
async function captureWithRetry(node, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      // 确保画布已展示
      await canvas({ action: "present", node, ...options });
      
      // 等待渲染
      await sleep(options.delayMs || 1000);
      
      // 捕获快照
      const result = await canvas({
        action: "snapshot",
        node,
        outputFormat: options.format || "png"
      });
      
      return result;
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      console.log(`Retry ${i + 1}/${maxRetries}...`);
      await sleep(1000);
    }
  }
}
```

---

## 5. 常见错误处理

### 5.1 错误代码表

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Canvas not found` | 画布未初始化 | 先执行 `action: "present"` |
| `Node not connected` | 节点未连接 | 检查节点 ID 和网络状态 |
| `JavaScript error` | JS 执行错误 | 检查代码语法和上下文 |
| `Invalid JSONL` | A2UI 数据格式错误 | 验证 JSONL 格式 |
| `Navigation failed` | 导航失败 | 检查 URL 和网络连接 |
| `Snapshot failed` | 截图失败 | 检查画布状态和尺寸 |
| `Timeout` | 操作超时 | 增加 `timeoutMs` 参数 |

### 5.2 问题排查流程

```
遇到问题 → 检查节点连接状态
        → 确认画布已展示 (present)
        → 检查网络连接
        → 验证参数格式
        → 查看详细错误信息
```

### 5.3 调试技巧

#### 检查画布状态

```json
{
  "action": "eval",
  "node": "node_001",
  "javaScript": "JSON.stringify({
    readyState: document.readyState,
    url: location.href,
    dimensions: {
      width: window.innerWidth,
      height: window.innerHeight
    }
  })"
}
```

#### 测试 A2UI 组件

```json
{
  "action": "a2ui_push",
  "node": "node_001",
  "jsonl": "{\"type\":\"component\",\"name\":\"Text\",\"props\":{\"content\":\"Test\"}}"
}
```

### 5.4 常见场景解决方案

#### 页面加载超时

```json
{
  "action": "navigate",
  "node": "node_001",
  "url": "https://slow-site.com"
}

// 然后使用 eval 等待特定元素
{
  "action": "eval",
  "node": "node_001",
  "javaScript": "
    () => new Promise((resolve, reject) => {
      let attempts = 0;
      const check = () => {
        attempts++;
        if (document.querySelector('.loaded')) {
          resolve('loaded');
        } else if (attempts > 100) {
          reject(new Error('Timeout waiting for element'));
        } else {
          setTimeout(check, 100);
        }
      };
      check();
    })
  ",
  "timeoutMs": 60000
}
```

#### A2UI 渲染问题

```json
// 重置后重新推送
{
  "action": "a2ui_reset",
  "node": "node_001"
}

{
  "action": "a2ui_push",
  "node": "node_001",
  "jsonl": "..."
}
```

#### 截图尺寸不正确

```json
// 先设置视口大小
{
  "action": "eval",
  "node": "node_001",
  "javaScript": "
    window.resizeTo(1920, 1080);
    document.documentElement.style.width = '1920px';
    document.documentElement.style.height = '1080px';
  "
}

// 然后截图
{
  "action": "snapshot",
  "node": "node_001",
  "width": 1920,
  "height": 1080
}
```

---

## 附录

### A. 快速参考卡

```bash
# 展示画布
{ "action": "present", "node": "...", "width": 1280, "height": 720 }

# 隐藏画布
{ "action": "hide", "node": "..." }

# 导航
{ "action": "navigate", "node": "...", "url": "..." }

# 执行 JS
{ "action": "eval", "node": "...", "javaScript": "..." }

# 截图
{ "action": "snapshot", "node": "...", "outputFormat": "png" }

# 推送 A2UI
{ "action": "a2ui_push", "node": "...", "jsonl": "..." }

# 重置 A2UI
{ "action": "a2ui_reset", "node": "..." }
```

### B. A2UI 组件示例

```jsonl
// 文本
{"type": "component", "name": "Text", "props": {"content": "Hello", "size": "medium"}}

// 按钮
{"type": "component", "name": "Button", "props": {"label": "Submit", "variant": "primary"}}

// 输入框
{"type": "component", "name": "Input", "props": {"placeholder": "Enter text", "type": "text"}}

// 图片
{"type": "component", "name": "Image", "props": {"src": "https://example.com/image.png", "alt": "Description"}}

// 容器
{"type": "component", "name": "Container", "props": {"layout": "horizontal", "gap": 16, "padding": 24}}
```

### C. 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.io)
- [A2UI 规范](https://docs.openclaw.io/a2ui)
- [JSON Lines 格式](https://jsonlines.org)

---

*文档版本：1.0*  
*最后更新：2026-03-01*
