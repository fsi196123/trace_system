#!/bin/bash

echo "🔄 重启睿码溯源系统"

cd /opt/trace-system

docker-compose down
docker-compose up -d

echo "✅ 系统已重启"
echo "访问地址： http://服务器IP"
