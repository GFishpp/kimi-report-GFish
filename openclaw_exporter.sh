#!/bin/bash
# OpenClaw Exporter for Prometheus
# 暴露OpenClaw特定指标

OUTPUT_FILE="/var/lib/node_exporter/textfile_collector/openclaw.prom"
mkdir -p /var/lib/node_exporter/textfile_collector

# 获取OpenClaw状态
OPENCLAW_STATUS=$(openclaw status 2>/dev/null)

# 会话数
SESSIONS=$(echo "$OPENCLAW_STATUS" | grep -oP 'sessions \d+' | awk '{print $2}')
SESSIONS=${SESSIONS:-0}

# 活跃会话详情
ACTIVE_SESSIONS=$(openclaw sessions list 2>/dev/null | jq -r '.count // 0')
ACTIVE_SESSIONS=${ACTIVE_SESSIONS:-0}

# Cron任务数
CRON_JOBS=$(openclaw cron list 2>/dev/null | jq '.jobs | length')
CRON_JOBS=${CRON_JOBS:-0}

# 获取Token使用情况（从会话历史估算）
TOTAL_TOKENS=0
for session_file in /root/.openclaw/agents/main/sessions/*.jsonl; do
    if [ -f "$session_file" ]; then
        # 简单估算：每行约100 tokens
        lines=$(wc -l < "$session_file" 2>/dev/null)
        TOTAL_TOKENS=$((TOTAL_TOKENS + lines * 100))
    fi
done

# 获取系统资源
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_USAGE=${CPU_USAGE:-0}

MEM_TOTAL=$(free -m | awk 'NR==2{print $2}')
MEM_USED=$(free -m | awk 'NR==2{print $3}')
MEM_USAGE=$((MEM_USED * 100 / MEM_TOTAL))

DISK_USAGE=$(df -h / | awk 'NR==2{print $5}' | cut -d'%' -f1)
DISK_USAGE=${DISK_USAGE:-0}

# 网络流量（需要安装iftop或vnstat）
NET_RX=$(cat /sys/class/net/eth0/statistics/rx_bytes 2>/dev/null || echo 0)
NET_TX=$(cat /sys/class/net/eth0/statistics/tx_bytes 2>/dev/null || echo 0)

# 写入Prometheus格式
cat > $OUTPUT_FILE << EOF
# HELP openclaw_sessions_total Total number of sessions
# TYPE openclaw_sessions_total gauge
openclaw_sessions_total $SESSIONS

# HELP openclaw_sessions_active Active sessions
# TYPE openclaw_sessions_active gauge
openclaw_sessions_active $ACTIVE_SESSIONS

# HELP openclaw_cron_jobs_total Total cron jobs
# TYPE openclaw_cron_jobs_total gauge
openclaw_cron_jobs_total $CRON_JOBS

# HELP openclaw_tokens_total Estimated total tokens used
# TYPE openclaw_tokens_total counter
openclaw_tokens_total $TOTAL_TOKENS

# HELP node_cpu_usage_percent CPU usage percentage
# TYPE node_cpu_usage_percent gauge
node_cpu_usage_percent $CPU_USAGE

# HELP node_memory_usage_percent Memory usage percentage
# TYPE node_memory_usage_percent gauge
node_memory_usage_percent $MEM_USAGE

# HELP node_disk_usage_percent Disk usage percentage
# TYPE node_disk_usage_percent gauge
node_disk_usage_percent $DISK_USAGE

# HELP node_network_rx_bytes Network received bytes
# TYPE node_network_rx_bytes counter
node_network_rx_bytes $NET_RX

# HELP node_network_tx_bytes Network transmitted bytes
# TYPE node_network_tx_bytes counter
node_network_tx_bytes $NET_TX
EOF

echo "Metrics exported to $OUTPUT_FILE"
