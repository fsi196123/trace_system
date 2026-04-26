# 睿码溯源系统 V1.0.0

## 产品简介

睿码溯源系统（RuiTrace Platform）是一款企业级工业防伪溯源解决方案，为企业提供从产品生产、流通到消费的全流程溯源管理能力。

## 核心功能

- **二维码管理**：批量生成、导出、管理唯一二维码
- **批次管理**：批次创建、状态跟踪、产品关联
- **扫码溯源**：扫码记录、地理位置分析、风险预警
- **任务中心**：统一的异步任务管理（生成任务、导出任务）
- **数据统计**：多维度数据统计和可视化展示

## 技术架构

- **前端**：Vue 3 + Element Plus + Vite
- **后端**：FastAPI + Python 3.10
- **数据库**：PostgreSQL 14
- **容器化**：Docker + Docker Compose
- **反向代理**：Nginx

## 目录结构

```
trace-v1-ops/
├── install/                 # 安装包
│   ├── docker-compose.yml  # 容器编排配置
│   ├── backend/            # 后端服务
│   │   ├── Dockerfile      # 后端构建文件
│   │   ├── requirements.txt
│   │   └── app/            # 后端源码
│   ├── frontend/           # 前端服务
│   │   ├── Dockerfile      # 前端构建文件
│   │   ├── nginx.conf      # Nginx配置
│   │   ├── vite.config.js
│   │   ├── package.json
│   │   └── src/            # 前端源码
│   └── env.example         # 环境变量模板
├── scripts/                # 运维脚本
│   ├── install.sh          # 一键安装
│   ├── start.sh            # 启动服务
│   ├── stop.sh             # 停止服务
│   ├── restart.sh          # 重启服务
│   ├── status.sh           # 状态检查
│   ├── backup.sh           # 数据库备份
│   └── restore.sh          # 数据恢复
├── init/                   # 初始化数据
│   ├── init.sql            # 数据库初始化
│   └── demo_data.sql       # 演示数据
├── logs/                   # 日志目录
├── docs/                   # 运维文档
└── README.md              # 说明文档
```

## 快速部署

### 环境要求

- Linux 服务器（Ubuntu 20.04+ / CentOS 7+）
- Docker 20.10+
- Docker Compose 2.0+

### 安装步骤

1. **上传安装包到服务器**
   ```bash
   scp -r trace-v1-ops.tar.gz user@server:/opt/
   ```

2. **解压安装包**
   ```bash
   cd /opt
   tar -xzf trace-v1-ops.tar.gz
   cd trace-v1-ops
   ```

3. **执行安装**
   ```bash
   cd scripts
   bash install.sh
   ```

4. **访问系统**
   - 前端界面：http://服务器IP
   - 后端API：http://服务器IP:8000
   - API文档：http://服务器IP:8000/docs

### 默认账号

- 用户名：admin
- 密码：admin123

## 常用运维命令

```bash
# 查看服务状态
./scripts/status.sh

# 查看后端日志
docker logs -f trace_backend

# 查看前端日志
docker logs -f trace_frontend

# 重启服务
./scripts/restart.sh

# 停止服务
./scripts/stop.sh

# 启动服务
./scripts/start.sh

# 备份数据库
./scripts/backup.sh

# 恢复数据库
./scripts/restore.sh backup/db_backup_20240419.sql
```

## 端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| 80   | Nginx/前端 | Web服务端口 |
| 8000 | FastAPI/后端 | API服务端口 |
| 5432 | PostgreSQL | 数据库端口（可选开放）|

## 目录说明

- `static/qrcode/` - 二维码图片存储
- `static/export/` - 导出文件存储
- `logs/backend/` - 后端日志
- `logs/nginx/` - Nginx日志
- `backup/` - 数据库备份

## 故障排查

### 服务无法启动

1. 检查 Docker 服务状态：`systemctl status docker`
2. 检查端口占用：`netstat -tlnp | grep 80`
3. 查看容器日志：`docker logs trace_backend`

### 数据库连接失败

1. 检查数据库容器：`docker ps | grep trace_db`
2. 等待数据库就绪：`docker logs trace_db`
3. 手动初始化数据库：
   ```bash
   docker exec -i trace_db psql -U trace_user -d trace_db < init/init.sql
   ```

### 前端无法访问

1. 检查 Nginx 容器：`docker ps | grep trace_nginx`
2. 查看 Nginx 日志：`docker logs trace_nginx`
3. 检查代理配置：是否正确转发到后端

## 联系方式

技术支持：support@ruitrace.com
官方网站：https://www.ruitrace.com

## 版本历史

- **V1.0.0** (2024-04-25)
  - 初始版本发布
  - 支持二维码生成、批次管理、扫码溯源
  - 企业级部署架构
