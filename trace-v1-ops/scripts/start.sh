#!/bin/bash

echo "========================================="
echo "  睿码溯源系统 - 启动服务"
echo "========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$(dirname "$SCRIPT_DIR")"
cd "$INSTALL_DIR"

echo "正在启动服务..."
docker-compose -f install/docker-compose.yml start

echo ""
echo "等待服务启动..."
sleep 5

echo ""
echo "服务状态:"
docker-compose -f install/docker-compose.yml ps

echo ""
echo "启动完成!"