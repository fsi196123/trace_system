#!/bin/bash

set -e

echo "========================================="
echo "  睿码溯源系统 - 数据库恢复"
echo "========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$INSTALL_DIR/backup"

# 检查参数
if [ -z "$1" ]; then
    echo ""
    echo "用法: $0 <备份文件路径>"
    echo ""
    echo "可用备份文件:"
    if [ -d "$BACKUP_DIR" ]; then
        ls -lh "$BACKUP_DIR"/db_backup_*.sql 2>/dev/null || echo "  无可用备份文件"
    else
        echo "  无可用备份文件"
    fi
    exit 1
fi

BACKUP_FILE="$1"

# 检查文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "错误: 备份文件不存在: $BACKUP_FILE"
    exit 1
fi

echo ""
echo "警告: 此操作将覆盖当前数据库!"
echo "备份文件: $BACKUP_FILE"
read -p "确认继续? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "正在恢复数据库..."

# 恢复数据库
docker exec -i trace_db psql -U trace_user -d trace_db < "$BACKUP_FILE"

echo ""
echo "✓ 数据库恢复成功!"

echo ""
echo "建议执行: ./scripts/restart.sh 重启服务"
echo ""
echo "========================================="