-- 睿码溯源系统初始化脚本

-- 创建批次表
CREATE TABLE IF NOT EXISTS batch (
    id SERIAL PRIMARY KEY,
    batch_no VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    total_count INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'processing',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建批次任务表
CREATE TABLE IF NOT EXISTS batch_task (
    id SERIAL PRIMARY KEY,
    batch_no VARCHAR(50) REFERENCES batch(batch_no),
    task_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    total INTEGER,
    success INTEGER DEFAULT 0,
    failed INTEGER DEFAULT 0,
    error_msg TEXT,
    result_path TEXT,
    product_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建溯源码表
CREATE TABLE IF NOT EXISTS trace_code (
    id SERIAL PRIMARY KEY,
    code_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    batch_no VARCHAR(50) REFERENCES batch(batch_no),
    qr_path TEXT,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建扫码记录表
CREATE TABLE IF NOT EXISTS scan_record (
    id SERIAL PRIMARY KEY,
    code_id VARCHAR(50) REFERENCES trace_code(code_id),
    scan_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address VARCHAR(50),
    location TEXT,
    is_first BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_batch_no ON batch(batch_no);
CREATE INDEX IF NOT EXISTS idx_task_batch_no ON batch_task(batch_no);
CREATE INDEX IF NOT EXISTS idx_trace_code_id ON trace_code(code_id);
CREATE INDEX IF NOT EXISTS idx_trace_batch_no ON trace_code(batch_no);
CREATE INDEX IF NOT EXISTS idx_scan_code_id ON scan_record(code_id);
CREATE INDEX IF NOT EXISTS idx_scan_time ON scan_record(scan_time);

-- 插入默认批次数据
INSERT INTO batch (batch_no, product_name, total_count, status) VALUES
('BATCH001', '测试产品', 100, 'done')
ON CONFLICT (batch_no) DO NOTHING;

-- 插入默认溯源码数据
INSERT INTO trace_code (code_id, product_name, batch_no, qr_path) VALUES
('CODE001', '测试产品', 'BATCH001', 'static/qrcode/CODE001.png'),
('CODE002', '测试产品', 'BATCH001', 'static/qrcode/CODE002.png'),
('CODE003', '测试产品', 'BATCH001', 'static/qrcode/CODE003.png')
ON CONFLICT (code_id) DO NOTHING;

-- 插入默认扫码记录
INSERT INTO scan_record (code_id, ip_address, location, is_first) VALUES
('CODE001', '192.168.1.1', '北京市', TRUE),
('CODE002', '192.168.1.2', '上海市', TRUE),
('CODE003', '192.168.1.3', '广州市', TRUE)
ON CONFLICT DO NOTHING;
