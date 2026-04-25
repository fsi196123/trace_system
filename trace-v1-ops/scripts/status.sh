#!/bin/bash

echo "=== 系统状态 ==="
docker ps | grep trace

echo "\n=== 后端健康 ==="
curl -s http://localhost:8000/ || echo "后端服务可能未启动"

echo "\n=== 数据库状态 ==="
docker exec -t trace_db pg_isready -U trace_user -d trace_db || echo "数据库可能未启动"

echo "\n=== Nginx状态 ==="
docker exec -t trace_nginx nginx -t || echo "Nginx可能未启动"
