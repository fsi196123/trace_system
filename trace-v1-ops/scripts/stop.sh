#!/bin/bash

echo "🛑 停止睿码溯源系统"

cd /opt/trace-system

docker-compose down

echo "✅ 系统已停止"
