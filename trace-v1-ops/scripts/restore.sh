#!/bin/bash

FILE=$1

if [ -z "$FILE" ]; then
    echo "❌ 请提供备份文件路径"
    echo "用法：bash restore.sh <备份文件路径>"
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "❌ 备份文件不存在：$FILE"
    exit 1
fi

echo "🔄 恢复数据库..."
docker exec -i trace_db psql -U trace_user trace_db < $FILE

echo "✅ 数据库恢复完成"
