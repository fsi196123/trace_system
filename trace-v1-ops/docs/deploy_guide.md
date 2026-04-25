# 睿码溯源系统 - 部署指南

## 一、服务器准备

### 1. 系统要求
- **操作系统**：Ubuntu 20.04 LTS 或 CentOS 7+
- **CPU**：2 核及以上
- **内存**：4GB 及以上
- **磁盘**：50GB 及以上
- **网络**：可访问互联网

### 2. 安装 Docker

#### Ubuntu 系统
```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Docker
apt install -y docker.io

# 启动 Docker 服务
systemctl start docker
systemctl enable docker

# 验证 Docker 安装
docker --version
```

#### CentOS 系统
```bash
# 安装 Docker
yum install -y docker

# 启动 Docker 服务
systemctl start docker
systemctl enable docker

# 验证 Docker 安装
docker --version
```

### 3. 安装 Docker Compose
```bash
# 下载 Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 添加执行权限
chmod +x /usr/local/bin/docker-compose

# 验证 Docker Compose 安装
docker-compose --version
```

### 4. 开放端口
```bash
# 开放 80 端口（Nginx）
ufw allow 80

# 开放 8000 端口（后端服务）
ufw allow 8000

# 开放 5432 端口（PostgreSQL，可选）
ufw allow 5432
```

## 二、系统部署

### 1. 上传安装包
将 `trace-v1-ops` 目录上传到服务器的 `/opt` 目录。

### 2. 执行安装脚本
```bash
# 进入脚本目录
cd /opt/trace-v1-ops/scripts

# 执行安装脚本
bash install.sh
```

### 3. 验证部署
安装完成后，脚本会输出访问地址。在浏览器中访问：
```
http://服务器IP
```

## 三、日常维护

### 1. 查看服务状态
```bash
# 进入脚本目录
cd /opt/trace-v1-ops/scripts

# 执行状态检查脚本
bash status.sh
```

### 2. 启动服务
```bash
# 进入脚本目录
cd /opt/trace-v1-ops/scripts

# 执行启动脚本
bash start.sh
```

### 3. 停止服务
```bash
# 进入脚本目录
cd /opt/trace-v1-ops/scripts

# 执行停止脚本
bash stop.sh
```

### 4. 重启服务
```bash
# 进入脚本目录
cd /opt/trace-v1-ops/scripts

# 执行重启脚本
bash restart.sh
```

### 5. 备份数据库
```bash
# 进入脚本目录
cd /opt/trace-v1-ops/scripts

# 执行备份脚本
bash backup.sh
```

### 6. 恢复数据
```bash
# 进入脚本目录
cd /opt/trace-v1-ops/scripts

# 执行恢复脚本（需要指定备份文件路径）
bash restore.sh /opt/trace-system/backup/db_202301010000.sql
```

## 四、常见问题

### 1. 服务无法访问
- 检查 80 端口是否开放
- 检查 Nginx 服务是否运行
- 检查后端服务是否运行

### 2. 数据库连接失败
- 检查 PostgreSQL 服务是否运行
- 检查数据库连接参数是否正确

### 3. 日志查看
- 后端日志：`/opt/trace-system/logs/backend/`
- Nginx 日志：`/opt/trace-system/logs/nginx/`

## 五、注意事项

1. **首次部署**：首次部署时，系统会自动初始化数据库和创建默认数据。

2. **备份策略**：建议定期执行备份脚本，确保数据安全。

3. **端口冲突**：如果服务器上已有其他服务占用 80、8000 或 5432 端口，需要修改配置文件。

4. **性能优化**：根据实际业务量，可以调整服务器配置和 Docker 容器资源限制。

5. **安全加固**：生产环境建议配置防火墙，限制外部访问。
