#!/bin/bash

echo "🚀 开始部署睿码溯源系统 V1"

# 1. 进入安装目录
echo "进入安装目录..."
cd ../install

# 2. 复制初始化数据
cp -r ../init/* .

# 3. 启动服务
echo "启动服务..."
docker-compose up -d --build

# 4. 等待数据库
echo "等待数据库初始化..."
sleep 10

# 5. 初始化数据
echo "初始化数据..."
docker exec -i trace_db psql -U trace_user -d trace_db < init.sql

echo "✅ 部署完成"
echo "访问地址： http://服务器IP"
