-- 睿码溯源系统数据库初始化脚本
-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建产品表
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type_code VARCHAR(20) NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建批次表
CREATE TABLE IF NOT EXISTS batch (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,
    batch_no VARCHAR(50) UNIQUE NOT NULL,
    production_date VARCHAR(20),
    count INTEGER DEFAULT 0,
    product_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'processing',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

-- 创建二维码表
CREATE TABLE IF NOT EXISTS trace_code (
    id SERIAL PRIMARY KEY,
    code_id VARCHAR(64) UNIQUE NOT NULL,
    product_id INTEGER,
    batch_id INTEGER,
    is_used BOOLEAN DEFAULT FALSE,
    first_scan_time TIMESTAMP,
    first_scan_ip VARCHAR(50),
    status VARCHAR(20) DEFAULT 'unused',
    scan_count INTEGER DEFAULT 0,
    last_scan_time TIMESTAMP,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    FOREIGN KEY (batch_id) REFERENCES batch(id) ON DELETE CASCADE
);

-- 创建扫码记录表
CREATE TABLE IF NOT EXISTS scan_log (
    id SERIAL PRIMARY KEY,
    code_id VARCHAR(50),
    ip VARCHAR(50),
    user_agent VARCHAR(200),
    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_first BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (code_id) REFERENCES trace_code(code_id) ON DELETE CASCADE
);

-- 创建批次任务表
CREATE TABLE IF NOT EXISTS batch_task (
    id SERIAL PRIMARY KEY,
    batch_no VARCHAR(50),
    task_type VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    total INTEGER DEFAULT 0,
    success INTEGER DEFAULT 0,
    failed INTEGER DEFAULT 0,
    error_msg TEXT,
    result_path VARCHAR(200),
    product_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建管理员表
CREATE TABLE IF NOT EXISTS admin_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建系统参数表
CREATE TABLE IF NOT EXISTS system_param (
    id SERIAL PRIMARY KEY,
    param_key VARCHAR(50) UNIQUE NOT NULL,
    param_value TEXT,
    description VARCHAR(200),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建系统规则表
CREATE TABLE IF NOT EXISTS system_rule (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(50) NOT NULL,
    rule_type VARCHAR(20),
    rule_config TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_trace_code_batch ON trace_code(batch_id);
CREATE INDEX IF NOT EXISTS idx_scan_log_code ON scan_log(code_id);
CREATE INDEX IF NOT EXISTS idx_scan_log_time ON scan_log(scan_time);
CREATE INDEX IF NOT EXISTS idx_batch_task_status ON batch_task(status);
CREATE INDEX IF NOT EXISTS idx_batch_task_type ON batch_task(task_type);

-- 插入默认管理员 (密码: admin123)
INSERT INTO admin_user (username, password_hash) VALUES
('admin', 'pbkdf2:sha256:600000$salt$hash'),
('test', 'pbkdf2:sha256:600000$salt$hash')
ON CONFLICT (username) DO NOTHING;

-- 插入默认系统参数
INSERT INTO system_param (param_key, param_value, description) VALUES
('max_scan_per_hour', '100', '单个IP每小时最大扫码次数'),
('risk_threshold', '50', '风险评分阈值'),
('enable_geo_verify', 'true', '启用地理位置验证'),
('enable_ip_whitelist', 'false', '启用IP白名单')
ON CONFLICT (param_key) DO NOTHING;

-- 插入默认系统规则
INSERT INTO system_rule (rule_name, rule_type, rule_config, enabled) VALUES
('高频扫码检测', 'frequency', '{"max_count": 10, "time_window": 3600}', true),
('异地扫码检测', 'location', '{"enabled": true, "distance_threshold": 500}', true),
('风险IP拦截', 'ip_blacklist', '{"enabled": true}', true)
ON CONFLICT (rule_name) DO NOTHING;