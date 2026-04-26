#!/bin/bash

echo "========================================="
echo "  睿码溯源系统 - 停止服务"
echo "========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$(dirname "$SCRIPT_DIR")"
cd "$INSTALL_DIR"

echo "正在停止服务..."
docker-compose -f install/docker-compose.yml stop

echo ""
echo "服务已停止"
echo "注意: 数据已保存在 Docker 卷中，下次启动时会自动恢复"