#!/bin/bash
# 自动备份脚本 - 备份重要文件到 GitHub

BACKUP_DIR="/root/.openclaw/workspace"
GITHUB_REPO="https://github.com/GFishpp/kimi-report-GFish.git"
DATE=$(date +%Y%m%d_%H%M)

echo "=== 开始备份 ${DATE} ==="

# 1. 创建本地备份压缩包
cd ${BACKUP_DIR}

tar -czf "auto_backup_${DATE}.tar.gz" \
    *.md \
    *.docx \
    *.py \
    *.yml \
    *.yaml \
    *.sh \
    *.txt \
    --exclude='*.tar.gz' \
    2>/dev/null

echo "✓ 本地备份创建完成: auto_backup_${DATE}.tar.gz"

# 2. 同步到 GitHub
cd ${BACKUP_DIR}

# 添加所有新文件
git add -A

# 提交更改
git commit -m "Auto backup ${DATE} - reports and configs" 2>/dev/null || echo "没有新文件需要提交"

# 推送到 GitHub
git push origin master 2>/dev/null && echo "✓ 已同步到 GitHub" || echo "✗ GitHub 同步失败"

echo "=== 备份完成 ==="
echo "备份文件: ${BACKUP_DIR}/auto_backup_${DATE}.tar.gz"
