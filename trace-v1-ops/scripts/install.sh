#!/bin/bash

set -e

echo "========================================="
echo "  睿码溯源系统 V1.0.0 - 自动化安装脚本"
echo "========================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose 未安装"
    echo "请先安装 Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo "[1/5] 检查安装目录..."
cd "$INSTALL_DIR"
echo "安装目录: $INSTALL_DIR"

echo ""
echo "[2/5] 创建必要的目录..."
mkdir -p logs/backend logs/nginx static/qrcode static/export

echo ""
echo "[3/5] 构建并启动容器..."
docker-compose -f install/docker-compose.yml up -d --build

echo ""
echo "[4/5] 等待数据库就绪..."
echo "正在等待数据库服务..."
sleep 10

# 等待数据库健康检查
for i in {1..30}; do
    if docker exec trace_db pg_isready -U trace_user -d trace_db &> /dev/null; then
        echo "数据库已就绪"
        break
    fi
    echo "等待数据库启动... ($i/30)"
    sleep 2
done

echo ""
echo "[5/5] 初始化数据库..."
docker exec -i trace_db psql -U trace_user -d trace_db < init/init.sql 2>/dev/null || true

echo ""
echo "========================================="
echo "  安装完成!"
echo "========================================="
echo ""
echo "访问地址:"
echo "  前端界面: http://localhost"
echo "  后端API:  http://localhost:8000"
echo "  API文档:  http://localhost:8000/docs"
echo ""
echo "默认账号:"
echo "  用户名: admin"
echo "  密码:   admin123"
echo ""
echo "常用命令:"
echo "  查看状态: ./scripts/status.sh"
echo "  查看日志: docker logs -f trace_backend"
echo "  停止服务: ./scripts/stop.sh"
echo "  重启服务: ./scripts/restart.sh"
echo ""
echo "========================================="