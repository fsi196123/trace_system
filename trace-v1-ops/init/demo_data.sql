-- 睿码溯源系统演示数据

-- 插入测试批次
INSERT INTO batch (batch_no, product_name, total_count, status) VALUES
('BATCH20240419001', '睿码测试产品A', 100, 'done'),
('BATCH20240419002', '智能测试产品', 50, 'done'),
('BATCH20240418001', '测试产品', 20, 'done');

-- 插入测试二维码 (示例)
INSERT INTO trace_code (code_id, batch_no, product_name, qr_path, signature) VALUES
('TEST-20240419-00001', 'BATCH20240419001', '睿码测试产品A', '/static/qrcode/TEST-20240419-00001.png', 'sig_001'),
('TEST-20240419-00002', 'BATCH20240419001', '睿码测试产品A', '/static/qrcode/TEST-20240419-00002.png', 'sig_002'),
('TEST-20240419-00003', 'BATCH20240419002', '智能测试产品', '/static/qrcode/TEST-20240419-00003.png', 'sig_003');

-- 插入扫码记录
INSERT INTO scan_log (code_id, ip, city, province, country, scan_time, verify_result, risk_level, scan_count) VALUES
('TEST-20240419-00001', '114.114.114.114', '南京', '江苏省', '中国', '2024-04-19 10:00:00', 'success', 'low', 1),
('TEST-20240419-00001', '8.8.8.8', 'Los Angeles', 'California', '美国', '2024-04-19 11:00:00', 'success', 'medium', 2),
('TEST-20240419-00002', '114.114.114.114', '上海', '上海市', '中国', '2024-04-19 12:00:00', 'success', 'low', 1);

-- 插入测试任务
INSERT INTO batch_task (batch_no, task_type, status, progress, total, success, failed, product_name) VALUES
('BATCH20240419001', 'generate', 'success', 100, 100, 100, 0, '睿码测试产品A'),
('BATCH20240419002', 'generate', 'success', 100, 50, 50, 0, '智能测试产品');