# Cron 工具详解

> OpenClaw 定时任务与调度工具完整文档

---

## 目录

1. [功能概述](#1-功能概述)
2. [参数详解](#2-参数详解)
3. [使用示例](#3-使用示例)
4. [最佳实践](#4-最佳实践)
5. [常见错误处理](#5-常见错误处理)

---

## 1. 功能概述

Cron 工具用于管理定时任务，支持按指定时间间隔自动执行任务。

### 核心功能

| 功能类别 | 说明 |
|----------|------|
| **定时执行** | 按 Cron 表达式指定的时间执行任务 |
| **调度语法** | 支持标准 Unix Cron 表达式 |
| **任务管理** | 创建、列出、删除、启用/禁用任务 |
| **子代理调度** | 定时触发子代理执行特定任务 |
| **日志记录** | 记录任务执行历史和输出 |

### 使用场景

| 场景 | 示例 |
|------|------|
| 定时报告 | 每天上午 9 点生成日报 |
| 数据同步 | 每小时同步一次数据 |
| 系统监控 | 每 5 分钟检查系统状态 |
| 定期清理 | 每周清理临时文件 |
| 定时通知 | 工作日早上发送提醒 |

---

## 2. 参数详解

### 2.1 CLI 命令结构

```bash
openclaw cron <subcommand> [options]
```

### 2.2 Subcommands

| 子命令 | 说明 | 常用选项 |
|--------|------|----------|
| `add` | 添加定时任务 | `--name`, `--schedule`, `--command` |
| `list` | 列出所有任务 | - |
| `remove` | 删除任务 | `--name` |
| `enable` | 启用任务 | `--name` |
| `disable` | 禁用任务 | `--name` |
| `logs` | 查看任务日志 | `--name`, `--lines` |
| `run` | 立即执行任务 | `--name` |

### 2.3 参数详解

#### add 子命令参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--name` | string | ✅ | 任务名称（唯一标识） |
| `--schedule` | string | ✅ | Cron 表达式 |
| `--command` | string | ✅ | 要执行的命令 |
| `--description` | string | ❌ | 任务描述 |
| `--enabled` | boolean | ❌ | 是否立即启用（默认 true） |
| `--timezone` | string | ❌ | 时区（默认系统时区） |

#### list 子命令参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--all` | boolean | 显示所有任务（包括禁用） |
| `--format` | string | 输出格式：table/json |

#### remove 子命令参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--name` | string | ✅ | 任务名称 |
| `--force` | boolean | ❌ | 强制删除不提示 |

#### logs 子命令参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--name` | string | - | 任务名称 |
| `--lines` | number | 50 | 显示行数 |
| `--follow` | boolean | false | 实时跟踪 |
| `--since` | string | - | 起始时间 |

### 2.4 Cron 表达式格式

```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日期 (1 - 31)
│ │ │ ┌───────────── 月份 (1 - 12)
│ │ │ │ ┌───────────── 星期几 (0 - 7, 0 和 7 都是周日)
│ │ │ │ │
│ │ │ │ │
* * * * *
```

### 2.5 特殊字符

| 字符 | 名称 | 说明 | 示例 |
|------|------|------|------|
| `*` | 星号 | 匹配任意值 | `* * * * *` 每分钟 |
| `,` | 逗号 | 列表分隔符 | `0,15,30,45 * * * *` 每 15 分钟 |
| `-` | 连字符 | 范围 | `9-17 * * * 1-5` 工作日 9-17 点 |
| `/` | 斜杠 | 步长 | `*/5 * * * *` 每 5 分钟 |
| `#` | 井号 | 第几个星期几 | `0 9 * * 1#1` 每月第一个周一 9 点 |
| `L` | L | 最后 | `0 0 L * *` 每月最后一天 |
| `W` | W | 最近工作日 | `0 0 15W * *` 每月 15 日最近工作日 |

### 2.6 预定义别名

| 别名 | 说明 | 等效表达式 |
|------|------|------------|
| `@yearly` | 每年 1 月 1 日 0:00 | `0 0 1 1 *` |
| `@monthly` | 每月 1 日 0:00 | `0 0 1 * *` |
| `@weekly` | 每周日 0:00 | `0 0 * * 0` |
| `@daily` | 每天 0:00 | `0 0 * * *` |
| `@hourly` | 每小时 0 分 | `0 * * * *` |
| `@reboot` | 系统启动时 | - |

---

## 3. 使用示例

### 3.1 基础示例

#### 每分钟执行

```bash
openclaw cron add \
  --name "minute-task" \
  --schedule "* * * * *" \
  --command "echo 'Running at $(date)'"
```

#### 每小时执行

```bash
openclaw cron add \
  --name "hourly-task" \
  --schedule "0 * * * *" \
  --command "openclaw run hourly-sync"
```

#### 每天执行

```bash
openclaw cron add \
  --name "daily-report" \
  --schedule "0 9 * * *" \
  --command "openclaw run generate-daily-report" \
  --description "每天上午 9 点生成日报"
```

### 3.2 常用时间模式

#### 工作日早上 8 点

```bash
openclaw cron add \
  --name "workday-morning" \
  --schedule "0 8 * * 1-5" \
  --command "openclaw run morning-routine"
```

#### 每 30 分钟

```bash
openclaw cron add \
  --name "frequent-check" \
  --schedule "*/30 * * * *" \
  --command "openclaw run health-check"
```

#### 每周一上午 9 点

```bash
openclaw cron add \
  --name "weekly-meeting" \
  --schedule "0 9 * * 1" \
  --command "openclaw run send-meeting-reminder"
```

#### 每月 1 日凌晨 2 点

```bash
openclaw cron add \
  --name "monthly-cleanup" \
  --schedule "0 2 1 * *" \
  --command "openclaw run cleanup-temp-files"
```

#### 每季度执行

```bash
openclaw cron add \
  --name "quarterly-report" \
  --schedule "0 9 1 1,4,7,10 *" \
  --command "openclaw run quarterly-analysis"
```

### 3.3 高级示例

#### 使用预定义别名

```bash
# 每小时执行
openclaw cron add \
  --name "hourly-task" \
  --schedule "@hourly" \
  --command "openclaw run sync-data"

# 每天执行
openclaw cron add \
  --name "daily-task" \
  --schedule "@daily" \
  --command "openclaw run daily-cleanup"
```

#### 复杂调度

```bash
# 工作日每 2 小时的整点和半点
openclaw cron add \
  --name "frequent-workday" \
  --schedule "0,30 9-17/2 * * 1-5" \
  --command "openclaw run check-queue"

# 每月第一个周一
openclaw cron add \
  --name "monthly-meeting" \
  --schedule "0 10 * * 1#1" \
  --command "openclaw run schedule-monthly-review"

# 每月最后一个工作日
openclaw cron add \
  --name "month-end" \
  --schedule "0 18 LW * *" \
  --command "openclaw run month-end-report"
```

#### 多命令任务

```bash
openclaw cron add \
  --name "complex-task" \
  --schedule "0 2 * * *" \
  --command "cd /app && ./backup.sh && openclaw run notify-backup-complete"
```

### 3.4 任务管理示例

#### 列出所有任务

```bash
# 表格格式
openclaw cron list

# JSON 格式
openclaw cron list --format json

# 包含禁用任务
openclaw cron list --all
```

输出示例：
```
NAME              SCHEDULE      COMMAND                    STATUS    LAST RUN
minute-task       * * * * *     echo 'Running...'          enabled   2 minutes ago
hourly-task       0 * * * *     openclaw run hourly-sync   enabled   45 minutes ago
daily-report      0 9 * * *     openclaw run generate...   enabled   5 hours ago
```

#### 禁用任务

```bash
openclaw cron disable --name "daily-report"
```

#### 启用任务

```bash
openclaw cron enable --name "daily-report"
```

#### 立即执行任务

```bash
openclaw cron run --name "daily-report"
```

#### 查看任务日志

```bash
# 最近 50 行
openclaw cron logs --name "daily-report"

# 最近 100 行
openclaw cron logs --name "daily-report" --lines 100

# 实时跟踪
openclaw cron logs --name "daily-report" --follow

# 最近 24 小时
openclaw cron logs --name "daily-report" --since "24h ago"
```

#### 删除任务

```bash
# 确认删除
openclaw cron remove --name "old-task"

# 强制删除
openclaw cron remove --name "old-task" --force
```

### 3.5 实际应用场景

#### 系统监控任务

```bash
# 每 5 分钟检查系统状态
openclaw cron add \
  --name "system-monitor" \
  --schedule "*/5 * * * *" \
  --command "openclaw run check-system-health" \
  --description "监控系统 CPU、内存、磁盘使用率"

# 每小时记录系统指标
openclaw cron add \
  --name "metrics-collector" \
  --schedule "0 * * * *" \
  --command "openclaw run collect-metrics"
```

#### 数据同步任务

```bash
# 每 10 分钟同步数据库
openclaw cron add \
  --name "db-sync" \
  --schedule "*/10 * * * *" \
  --command "openclaw run sync-database"

# 每天凌晨同步外部数据
openclaw cron add \
  --name "external-sync" \
  --schedule "0 3 * * *" \
  --command "openclaw run fetch-external-data"
```

#### 报告生成任务

```bash
# 每日报告
openclaw cron add \
  --name "daily-report" \
  --schedule "0 9 * * *" \
  --command "openclaw run generate-daily-report && openclaw run send-email --to admin@example.com"

# 周报（周五下午 5 点）
openclaw cron add \
  --name "weekly-report" \
  --schedule "0 17 * * 5" \
  --command "openclaw run generate-weekly-report"

# 月报（每月 1 日上午 10 点）
openclaw cron add \
  --name "monthly-report" \
  --schedule "0 10 1 * *" \
  --command "openclaw run generate-monthly-report"
```

#### 清理维护任务

```bash
# 每天清理临时文件
openclaw cron add \
  --name "temp-cleanup" \
  --schedule "0 2 * * *" \
  --command "find /tmp -type f -mtime +7 -delete"

# 每周清理日志
openclaw cron add \
  --name "log-rotation" \
  --schedule "0 3 * * 0" \
  --command "openclaw run rotate-logs"

# 每月优化数据库
openclaw cron add \
  --name "db-optimize" \
  --schedule "0 4 1 * *" \
  --command "openclaw run optimize-database"
```

---

## 4. 最佳实践

### 4.1 任务命名规范

| 类型 | 命名模式 | 示例 |
|------|----------|------|
| 报告任务 | `{频率}-report-{名称}` | `daily-report-sales` |
| 同步任务 | `sync-{数据源}` | `sync-database`, `sync-api` |
| 检查任务 | `check-{目标}` | `check-system-health` |
| 清理任务 | `cleanup-{类型}` | `cleanup-temp-files` |
| 通知任务 | `notify-{事件}` | `notify-deployment` |

### 4.2 调度时间选择

| 建议 | 说明 |
|------|------|
| 避免整点高峰 | 选择 `:05`, `:15` 等偏移时间 |
| 分散负载 | 不同任务使用不同分钟数 |
| 考虑时区 | 明确任务执行的时区 |
| 避开维护窗口 | 了解系统的维护时间 |

```bash
# ❌ 不推荐：所有任务都在整点
0 * * * *    # 每小时整点
0 0 * * *    # 每天零点

# ✅ 推荐：分散时间
5 * * * *    # 每小时第 5 分钟
15 2 * * *   # 每天 2:15
30 3 * * 0   # 每周日 3:30
```

### 4.3 命令编写建议

```bash
# ❌ 不推荐：简单命令无错误处理
echo "Starting task"
python script.py

# ✅ 推荐：完整的错误处理和日志
#!/bin/bash
set -euo pipefail

LOG_FILE="/var/log/cron/task-$(date +%Y%m%d-%H%M%S).log"
exec 1>"$LOG_FILE" 2>&1

echo "[$(date)] Task started"

if ! python /app/script.py; then
  echo "[$(date)] Task failed"
  openclaw run send-alert --message "Task failed"
  exit 1
fi

echo "[$(date)] Task completed successfully"
```

### 4.4 任务设计原则

1. **幂等性**：任务可以安全地多次执行
2. **超时控制**：设置合理的执行超时
3. **资源清理**：任务完成后清理临时资源
4. **错误通知**：失败时及时通知
5. **日志记录**：记录足够的执行信息

### 4.5 监控和告警

```bash
# 创建带监控的任务
openclaw cron add \
  --name "monitored-task" \
  --schedule "0 */6 * * *" \
  --command '
    if ! openclaw run critical-task; then
      openclaw run send-alert --severity high --message "Critical task failed"
      exit 1
    fi
  '
```

### 4.6 时区处理

```bash
# 指定时区（推荐明确指定）
openclaw cron add \
  --name "tz-task" \
  --schedule "0 9 * * *" \
  --command "openclaw run task" \
  --timezone "Asia/Shanghai"
```

---

## 5. 常见错误处理

### 5.1 错误代码表

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Invalid cron expression` | Cron 表达式格式错误 | 检查表达式语法 |
| `Command not found` | 命令不存在 | 使用绝对路径或检查 PATH |
| `Permission denied` | 权限不足 | 检查文件权限和所有者 |
| `Overlapping execution` | 任务执行时间过长 | 增加执行间隔或优化任务 |
| `Task not found` | 任务名称不存在 | 检查任务名称拼写 |
| `Task already exists` | 任务名称已存在 | 使用不同的名称或先删除旧任务 |
| `Execution timeout` | 任务执行超时 | 增加超时设置或优化任务 |

### 5.2 Cron 表达式常见错误

| 错误表达式 | 问题 | 正确表达式 |
|------------|------|------------|
| `* * * *` | 缺少一个字段 | `* * * * *` |
| `60 * * * *` | 分钟超出范围 | `0 * * * *` |
| `0 25 * * *` | 小时超出范围 | `0 23 * * *` |
| `0 0 32 * *` | 日期超出范围 | `0 0 31 * *` |
| `0 0 * 13 *` | 月份超出范围 | `0 0 * 12 *` |
| `*/0 * * * *` | 步长不能为 0 | `*/5 * * * *` |

### 5.3 问题排查流程

```
任务未执行 → 检查任务状态 (cron list)
          → 检查 Cron 表达式是否正确
          → 查看任务日志 (cron logs)
          → 检查命令是否存在
          → 手动执行任务测试 (cron run)
```

### 5.4 调试技巧

#### 测试 Cron 表达式

```bash
# 查看未来执行时间
openclaw cron test --schedule "0 9 * * 1-5" --count 10

输出：
Next 10 executions:
1. 2026-03-02 09:00:00 (Mon)
2. 2026-03-03 09:00:00 (Tue)
3. 2026-03-04 09:00:00 (Wed)
...
```

#### 验证命令

```bash
# 先手动测试命令
openclaw run your-command

# 确认无误后再创建定时任务
openclaw cron add --name "task" --schedule "..." --command "openclaw run your-command"
```

#### 查看系统日志

```bash
# 查看 Cron 服务日志
journalctl -u openclaw-cron -f

# 查看特定任务日志
openclaw cron logs --name "task-name" --lines 100
```

### 5.5 常见场景解决方案

#### 任务执行时间过长

```bash
# 添加超时控制
timeout 300 openclaw run your-command || echo "Task timed out"
```

#### 防止任务重叠

```bash
# 使用 flock 防止重叠执行
flock -n /var/lock/task.lock -c 'openclaw run your-command'
```

#### 环境变量问题

```bash
# 在命令中明确设置环境变量
openclaw cron add \
  --name "env-task" \
  --schedule "0 * * * *" \
  --command 'export PATH=/usr/local/bin:$PATH && export API_KEY=xxx && openclaw run task'
```

#### 输出重定向

```bash
# 将输出保存到文件
openclaw cron add \
  --name "logged-task" \
  --schedule "0 * * * *" \
  --command 'openclaw run task >> /var/log/cron/task.log 2>&1'
```

---

## 附录

### A. 快速参考卡

```bash
# 添加任务
openclaw cron add --name "task" --schedule "0 9 * * *" --command "cmd"

# 列出任务
openclaw cron list

# 查看日志
openclaw cron logs --name "task"

# 立即执行
openclaw cron run --name "task"

# 禁用/启用
openclaw cron disable --name "task"
openclaw cron enable --name "task"

# 删除任务
openclaw cron remove --name "task"
```

### B. Cron 表达式速查表

| 需求 | 表达式 |
|------|--------|
| 每分钟 | `* * * * *` |
| 每 5 分钟 | `*/5 * * * *` |
| 每 15 分钟 | `*/15 * * * *` |
| 每 30 分钟 | `*/30 * * * *` |
| 每小时 | `0 * * * *` |
| 每 2 小时 | `0 */2 * * *` |
| 每天 0 点 | `0 0 * * *` |
| 每天 9 点 | `0 9 * * *` |
| 工作日 9 点 | `0 9 * * 1-5` |
| 每周一 9 点 | `0 9 * * 1` |
| 每月 1 日 0 点 | `0 0 1 * *` |
| 每年 1 月 1 日 | `0 0 1 1 *` |

### C. 相关资源

- [OpenClaw 官方文档](https://docs.openclaw.io)
- [Cron 表达式测试工具](https://crontab.guru)
- [Unix Crontab 手册](https://man7.org/linux/man-pages/man5/crontab.5.html)

---

*文档版本：1.0*  
*最后更新：2026-03-01*
