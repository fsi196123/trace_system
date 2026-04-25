# 睿码溯源系统 - 运维交付包 V1

## 一、项目概览

睿码溯源系统是一款企业级防伪溯源解决方案，基于现代化的技术栈构建，提供二维码生成、批次管理、扫码溯源等核心功能。本运维交付包旨在为运维人员提供标准化的部署和管理流程，确保系统的稳定运行。

### 系统特点
- **企业级架构**：基于 Docker 容器化部署，确保系统的可扩展性和可靠性
- **任务化管理**：所有耗时操作（如批量生成二维码、导出文件）均采用任务化管理
- **完整的业务闭环**：创建批次 → 批量生成二维码 → 导出 Excel/ZIP → A4 打印 → 贴标生产 → 扫码溯源
- **可观测性**：完善的日志系统和状态检查机制
- **易于维护**：标准化的运维脚本，简化日常管理

## 二、目录结构

```
trace-v1-ops/
│
├── install/                 # 安装包（核心）
│   ├── docker-compose.yml   # Docker Compose 配置文件
│   ├── nginx.conf           # Nginx 配置文件
│   ├── env.example          # 环境变量模板
│
├── scripts/                # 运维脚本（关键）
│   ├── install.sh          # 安装脚本
│   ├── start.sh            # 启动脚本
│   ├── stop.sh             # 停止脚本
│   ├── restart.sh          # 重启脚本
│   ├── status.sh           # 状态检查脚本
│   ├── backup.sh           # 备份数据库脚本
│   ├── restore.sh          # 恢复数据脚本
│
├── init/                   # 初始化数据
│   ├── init.sql            # 初始化数据库表结构
│   ├── demo_data.sql       # 演示数据
│
├── logs/                   # 日志目录（挂载）
│   ├── backend/            # 后端服务日志
│   ├── nginx/              # Nginx 日志
│
├── docs/                   # 运维手册
│   ├── deploy_guide.md     # 部署指南
│   ├── troubleshooting.md  # 故障排查指南
│   ├── architecture.md     # 架构说明
│
└── README.md               # 运维入口说明
```

## 三、快速开始

### 1. 服务器准备
- 安装 Docker 和 Docker Compose
- 开放端口：80 / 8000 / 5432（可选）

### 2. 安装系统
```bash
# 进入脚本目录
cd trace-v1-ops/scripts

# 执行安装脚本
bash install.sh
```

### 3. 访问系统
安装完成后，在浏览器中访问：
```
http://服务器IP
```

## 四、日常操作

### 1. 查看系统状态
```bash
bash status.sh
```

### 2. 启动系统
```bash
bash start.sh
```

### 3. 停止系统
```bash
bash stop.sh
```

### 4. 重启系统
```bash
bash restart.sh
```

### 5. 备份数据库
```bash
bash backup.sh
```

### 6. 恢复数据
```bash
bash restore.sh <备份文件路径>
```

## 五、技术栈

### 前端
- Vue 3 + Element Plus + Vue Router + Pinia
- Vite 构建工具

### 后端
- FastAPI + Python 3.9+
- PostgreSQL 14
- SQLAlchemy ORM

### 容器化
- Docker + Docker Compose
- Nginx 反向代理

## 六、系统架构

系统采用三层架构：
1. **前端层**：Vue 3 应用，提供用户界面
2. **后端层**：FastAPI 服务，处理业务逻辑
3. **数据层**：PostgreSQL 数据库，存储系统数据

## 七、常见问题

### 1. 服务无法访问
- 检查 80 端口是否开放
- 检查 Nginx 服务是否运行
- 检查后端服务是否运行

### 2. 数据库连接失败
- 检查 PostgreSQL 服务是否运行
- 检查数据库连接参数是否正确

### 3. 二维码生成失败
- 检查服务器磁盘空间是否充足
- 检查后端服务日志

### 4. 导出功能失败
- 检查服务器磁盘空间是否充足
- 检查后端服务日志

## 八、监控与维护

### 1. 日志查看
- 后端日志：`/opt/trace-system/logs/backend/`
- Nginx 日志：`/opt/trace-system/logs/nginx/`

### 2. 性能监控
- 使用 `docker stats` 监控容器资源使用情况
- 使用 `top` 或 `htop` 监控服务器资源使用情况

### 3. 安全加固
- 配置防火墙，限制外部访问
- 定期更新系统和依赖包
- 定期备份数据库

## 九、版本管理

### 版本号格式
`v<主版本>.<次版本>.<修订版本>`

### 当前版本
V1.0.0

### 升级说明
- 升级前请备份数据库
- 按照部署指南执行升级流程

## 十、技术支持

### 联系信息
- **技术支持邮箱**：support@ruitrace.com
- **技术支持电话**：400-123-4567
- **工作时间**：周一至周五 9:00-18:00

### 支持范围
- 系统部署和配置
- 系统故障排查
- 系统性能优化
- 系统升级和迁移

## 十一、许可证

© 2026 睿码溯源系统. All rights reserved.

## 十二、免责声明

本系统仅供企业内部使用，请勿用于非法用途。使用本系统产生的一切后果由使用者自行承担。
