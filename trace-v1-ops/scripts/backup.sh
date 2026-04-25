#!/bin/bash

DATE=$(date +%Y%m%d%H%M)

# 创建备份目录
mkdir -p /opt/trace-system/backup

echo "💾 备份数据库..."
docker exec trace_db pg_dump -U trace_user trace_db > /opt/trace-system/backup/db_$DATE.sql

echo "✅ 备份完成：/opt/trace-system/backup/db_$DATE.sql"
