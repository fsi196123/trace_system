#!/bin/bash

echo "========================================="
echo "  睿码溯源系统 - 服务状态检查"
echo "========================================="
echo ""

echo "【容器状态】"
docker ps --filter "name=trace_" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "【服务健康检查】"

# 检查后端
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✓ 后端服务: 正常 (http://localhost:8000)"
else
    echo "✗ 后端服务: 异常"
fi

# 检查前端
if curl -s http://localhost/ > /dev/null 2>&1; then
    echo "✓ 前端服务: 正常 (http://localhost)"
else
    echo "✗ 前端服务: 异常"
fi

# 检查数据库
if docker exec trace_db pg_isready -U trace_user -d trace_db > /dev/null 2>&1; then
    echo "✓ 数据库: 正常"
else
    echo "✗ 数据库: 异常"
fi

echo ""
echo "【资源使用】"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" \
    $(docker ps --filter "name=trace_" -q)

echo ""
echo "========================================="