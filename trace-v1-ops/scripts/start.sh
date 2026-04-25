#!/bin/bash

echo "🚀 启动睿码溯源系统"

cd /opt/trace-system

docker-compose up -d

echo "✅ 系统已启动"
echo "访问地址： http://服务器IP"
