# 睿码溯源系统 - 部署指南

## 一、环境准备

### 1.1 服务器要求

- **配置建议**：
  - CPU：2核+
  - 内存：4GB+
  - 硬盘：50GB+

- **操作系统**：
  - CentOS 7+
  - RHEL 7+
  - Ubuntu 20.04 LTS+
  - Debian 11+

### 1.2 安装依赖

#### CentOS/RHEL 安装 Docker

```bash
# 安装依赖
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加 Docker 源
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker 并设置开机自启
sudo systemctl start docker
sudo systemctl enable docker
```

#### Ubuntu/Debian 安装 Docker

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#### 安装 Docker Compose

```bash
# 下载 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 赋予执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker-compose --version
```

### 1.3 防火墙配置

#### CentOS/RHEL 防火墙

```bash
# 开放必要端口
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --reload

# 查看开放的端口
sudo firewall-cmd --list-ports
```

#### Ubuntu/Debian 防火墙

```bash
# 开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS（可选）
sudo ufw allow 8000  # 后端API（可选）

sudo ufw enable
```

## 二、安装部署

### 2.1 上传安装包

```bash
# 使用 scp 上传
scp -r trace-v1-ops user@your-server:/opt/

# 或使用 FTP/SFTP 工具上传
```

### 2.2 解压安装包

```bash
cd /opt
tar -xzf trace-v1-ops.tar.gz
cd trace-v1-ops
```

### 2.3 执行安装

```bash
cd scripts
bash install.sh
```

安装脚本会自动：
1. 检查 Docker 环境
2. 创建必要目录
3. 构建 Docker 镜像
4. 启动容器服务
5. 初始化数据库
6. 验证服务状态

### 2.4 验证部署

```bash
# 检查服务状态
./scripts/status.sh

# 访问前端界面
curl http://localhost

# 访问后端API
curl http://localhost:8000

# 查看API文档
curl http://localhost:8000/docs
```

## 三、配置说明

### 3.1 环境变量配置

复制环境变量模板并修改：

```bash
cd install
cp env.example .env
nano .env
```

主要配置项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| POSTGRES_PASSWORD | 数据库密码 | trace_pass_2024 |
| JWT_SECRET_KEY | JWT密钥 | 生产环境请修改 |
| DEBUG_MODE | 调试模式 | false |

### 3.2 端口配置

如需修改默认端口，编辑 `install/docker-compose.yml`：

```yaml
services:
  nginx:
    ports:
      - "8080:80"  # 修改前端端口
  backend:
    ports:
      - "8081:8000"  # 修改后端端口
```

### 3.3 存储路径配置

默认数据存储在 Docker 卷中，如需修改为本地路径：

```yaml
volumes:
  - /data/trace/pgdata:/var/lib/postgresql/data  # PostgreSQL数据
  - ./static:/app/static  # 二维码文件
```

## 四、数据管理

### 4.1 数据库备份

```bash
# 自动备份
./scripts/backup.sh

# 备份文件保存在 backup/ 目录
# 文件名格式：db_backup_YYYYMMDD_HHMMSS.sql
```

### 4.2 数据恢复

```bash
# 查看可用备份
ls -lh backup/

# 恢复指定备份
./scripts/restore.sh backup/db_backup_20240419.sql
```

### 4.3 日志管理

```bash
# 查看后端日志
docker logs -f trace_backend

# 查看Nginx日志
docker logs -f trace_nginx

# 清理30天前的日志（可添加到crontab）
find logs -name "*.log" -mtime +30 -delete
```

## 五、系统维护

### 5.1 日常检查

```bash
# 检查服务状态
./scripts/status.sh

# 检查资源使用
docker stats

# 检查磁盘空间
df -h
```

### 5.2 版本升级

1. 备份当前数据
2. 停止服务：`./scripts/stop.sh`
3. 备份原安装目录
4. 解压新版本
5. 执行安装：`./scripts/install.sh`
6. 恢复数据（如需要）

### 5.3 卸载系统

```bash
# 停止并删除容器
docker-compose -f install/docker-compose.yml down -v

# 删除镜像
docker rmi $(docker images | grep trace)

# 删除数据卷（谨慎操作，会删除所有数据）
docker volume rm trace-v1-ops_pgdata
```

## 六、故障排查

### 6.1 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 安装脚本执行失败 | Docker未安装 | 重新安装Docker |
| 数据库连接失败 | 容器启动顺序问题 | 等待10秒后重试 |
| 前端无法访问 | Nginx未启动 | 重启服务 |
| 二维码生成失败 | 权限问题 | 检查static目录权限 |

### 6.2 日志分析

```bash
# 查看错误日志
docker logs trace_backend 2>&1 | grep ERROR

# 查看访问日志
docker exec trace_nginx tail -f /var/log/nginx/access.log

# 查看数据库日志
docker exec trace_db tail -f /var/log/postgresql/postgresql.log
```

### 6.3 紧急恢复

如遇系统故障无法恢复：

1. 备份数据目录
2. 执行全新安装
3. 恢复备份数据
4. 如仍无法解决，联系技术支持

## 七、安全建议

1. **修改默认密码**：首次部署后立即修改 admin 密码
2. **修改JWT密钥**：生产环境使用随机字符串
3. **关闭不需要的端口**：仅开放 80/443
4. **定期备份数据**：建议每日自动备份
5. **启用SSL**：生产环境建议启用 HTTPS
6. **限制数据库访问**：如无特殊需求，不开放5432端口