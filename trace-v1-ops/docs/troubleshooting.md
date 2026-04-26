# 睿码溯源系统 - 故障排查指南

## 一、服务无法启动

### 1.1 Docker 服务异常

**症状**：执行安装脚本时报错 "Docker 未安装"

**解决方案**：

#### CentOS/RHEL
```bash
# 检查Docker状态
systemctl status docker

# 启动Docker服务
sudo systemctl start docker

# 设置Docker开机自启
sudo systemctl enable docker
```

#### Ubuntu/Debian
```bash
# 检查Docker状态
systemctl status docker

# 启动Docker服务
sudo systemctl start docker

# 设置Docker开机自启
sudo systemctl enable docker
```

### 1.2 端口被占用

**症状**：容器启动失败，提示端口已被占用

**解决方案**：
```bash
# 查看端口占用情况
netstat -tlnp | grep 80
netstat -tlnp | grep 8000
netstat -tlnp | grep 5432

# 释放端口（停止占用该端口的服务）
sudo systemctl stop nginx  # 如果是Nginx占用
sudo fuser -k 80/tcp       # 强制释放80端口

# 或修改docker-compose.yml中的端口映射
```

### 1.3 磁盘空间不足

**症状**：镜像构建或容器启动失败

**解决方案**：
```bash
# 查看磁盘空间
df -h

# 清理Docker资源
docker system prune -a

# 清理旧镜像
docker image prune -a

# 清理未使用的容器
docker container prune
```

## 二、数据库问题

### 2.1 数据库连接失败

**症状**：后端服务日志显示 "connection refused"

**解决方案**：
```bash
# 检查数据库容器状态
docker ps | grep trace_db

# 查看数据库日志
docker logs trace_db

# 等待数据库就绪后重试
sleep 30

# 手动测试连接
docker exec -it trace_db psql -U trace_user -d trace_db -c "SELECT 1"
```

### 2.2 数据库初始化失败

**症状**：表不存在或数据异常

**解决方案**：
```bash
# 重新初始化数据库
docker exec -i trace_db psql -U trace_user -d trace_db < init/init.sql

# 如需重新创建数据库
docker-compose -f install/docker-compose.yml down -v
docker-compose -f install/docker-compose.yml up -d
```

### 2.3 数据丢失

**症状**：重启后数据丢失

**原因**：未使用持久化存储

**解决方案**：
```bash
# 使用Docker卷持久化（默认已配置）
# 检查卷是否存在
docker volume ls | grep pgdata

# 如需重新配置持久化
docker-compose -f install/docker-compose.yml down
docker volume create trace-v1-ops_pgdata
docker-compose -f install/docker-compose.yml up -d
```

## 三、后端服务问题

### 3.1 后端启动失败

**症状**：trace_backend 容器状态为 "Exited"

**解决方案**：
```bash
# 查看错误日志
docker logs trace_backend

# 常见错误及解决：

# 1. 缺少依赖
# 重新构建镜像
docker-compose -f install/docker-compose.yml build backend
docker-compose -f install/docker-compose.yml up -d

# 2. 端口冲突
# 修改 docker-compose.yml 中的端口映射

# 3. 权限问题
docker exec trace_backend chown -R app:app /app
```

### 3.2 API 请求超时

**症状**：前端请求后端API超时

**解决方案**：
```bash
# 检查后端负载
docker stats trace_backend --no-stream

# 增加超时时间（修改nginx.conf）
proxy_connect_timeout 60s;
proxy_read_timeout 120s;

# 重启Nginx
docker-compose -f install/docker-compose.yml restart nginx
```

### 3.3 二维码生成失败

**症状**：生成二维码时出错

**解决方案**：
```bash
# 检查存储目录权限
docker exec trace_backend ls -la /app/static/qrcode

# 修复权限
docker exec trace_backend mkdir -p /app/static/qrcode /app/static/export
docker exec trace_backend chmod -R 777 /app/static

# 检查磁盘空间
df -h /app
```

## 四、前端服务问题

### 4.1 前端页面无法访问

**症状**：访问 http://localhost 显示 502 或 404

**解决方案**：
```bash
# 检查Nginx容器状态
docker ps | grep trace_nginx

# 查看Nginx日志
docker logs trace_nginx

# 检查前端构建文件是否存在
docker exec trace_nginx ls -la /usr/share/nginx/html

# 重新构建前端
docker-compose -f install/docker-compose.yml build frontend
docker-compose -f install/docker-compose.yml up -d
```

### 4.2 前端无法访问后端API

**症状**：前端显示 "网络错误" 或 "API请求失败"

**解决方案**：
```bash
# 检查代理配置
docker exec trace_nginx cat /etc/nginx/conf.d/default.conf

# 测试API转发
curl -I http://localhost/api/

# 重启Nginx
docker-compose -f install/docker-compose.yml restart nginx
```

## 五、性能问题

### 5.1 服务响应缓慢

**解决方案**：
```bash
# 检查资源使用
docker stats

# 增加资源限制（修改docker-compose.yml）
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G

# 优化数据库查询
docker exec trace_db psql -U trace_user -d trace_db -c "SELECT * FROM pg_stat_activity;"
```

### 5.2 内存不足 (OOM)

**解决方案**：

#### CentOS/RHEL
```bash
# 增加Swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永久启用swap
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

#### Ubuntu/Debian
```bash
# 增加Swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永久启用swap
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
```

```bash
# 或限制Docker内存使用
docker-compose -f install/docker-compose.yml up -d --memory="2g"
```

## 六、数据备份与恢复

### 6.1 备份失败

**症状**：执行 backup.sh 失败

**解决方案**：
```bash
# 检查备份目录权限
ls -la backup/

# 手动创建备份目录
mkdir -p backup
chmod 777 backup

# 手动执行备份
docker exec trace_db pg_dump -U trace_user -d trace_db > backup/db_backup_$(date +%Y%m%d).sql
```

### 6.2 恢复失败

**症状**：恢复数据后服务异常

**解决方案**：
```bash
# 确保备份文件完整
ls -lh backup/db_backup_*.sql

# 检查备份文件内容
head -20 backup/db_backup_20240419.sql

# 恢复前先清空现有数据
docker exec -i trace_db psql -U trace_user -d trace_db < backup/db_backup_20240419.sql
```

## 七、紧急恢复流程

### 7.1 系统完全崩溃

1. **备份当前状态**
   ```bash
   docker ps > containers_status.txt
   docker images > images_list.txt
   ```

2. **清理环境**
   ```bash
   docker-compose -f install/docker-compose.yml down -v
   docker system prune -a
   ```

3. **重新安装**
   ```bash
   ./scripts/install.sh
   ```

4. **恢复数据**
   ```bash
   ./scripts/restore.sh backup/db_backup_latest.sql
   ```

### 7.2 仅数据库问题

1. **备份当前数据库**
   ```bash
   docker exec trace_db pg_dump -U trace_user -d trace_db > emergency_backup.sql
   ```

2. **重建数据库容器**
   ```bash
   docker-compose -f install/docker-compose.yml stop db
   docker volume rm trace-v1-ops_pgdata
   docker-compose -f install/docker-compose.yml up -d
   ```

3. **恢复数据**
   ```bash
   sleep 10
   docker exec -i trace_db psql -U trace_user -d trace_db < emergency_backup.sql
   ```

## 八、日志收集

### 8.1 收集诊断信息

```bash
# 创建诊断目录
mkdir -p diagnostics
cd diagnostics

# 收集系统信息
uname -a > system_info.txt
df -h > disk_info.txt
docker ps > containers.txt
docker stats --no-stream > stats.txt

# 收集日志
docker logs trace_backend > backend_logs.txt 2>&1
docker logs trace_nginx > nginx_logs.txt 2>&1
docker logs trace_db > db_logs.txt 2>&1

# 打包
tar -czf diagnostics_$(date +%Y%m%d).tar.gz *.txt
```

### 8.2 联系技术支持

收集完诊断信息后，请联系技术支持并提供：
- 诊断包：`diagnostics_YYYYMMDD.tar.gz`
- 问题描述
- 问题发生时间
- 已尝试的解决方案