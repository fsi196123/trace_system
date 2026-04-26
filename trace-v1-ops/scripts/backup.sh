#!/bin/bash

set -e

echo "========================================="
echo "  睿码溯源系统 - 数据库备份"
echo "========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$INSTALL_DIR/backup"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 生成时间戳
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

echo ""
echo "正在备份数据库..."
echo "备份文件: $BACKUP_FILE"

# 执行备份
docker exec trace_db pg_dump -U trace_user -d trace_db > "$BACKUP_FILE"

# 检查备份是否成功
if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo ""
    echo "✓ 备份成功!"
    echo "  文件: $BACKUP_FILE"
    echo "  大小: $SIZE"

    # 清理30天前的备份
    find "$BACKUP_DIR" -name "db_backup_*.sql" -mtime +30 -delete
    echo "  已清理30天前的旧备份"
else
    echo ""
    echo "✗ 备份失败!"
    exit 1
fi

echo ""
echo "========================================="