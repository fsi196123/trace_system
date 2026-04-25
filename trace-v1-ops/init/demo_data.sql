-- 睿码溯源系统演示数据

-- 插入更多批次数据
INSERT INTO batch (batch_no, product_name, total_count, status) VALUES
('BATCH002', '电子产品', 500, 'done'),
('BATCH003', '食品', 1000, 'done'),
('BATCH004', '药品', 200, 'done')
ON CONFLICT (batch_no) DO NOTHING;

-- 插入更多溯源码数据
INSERT INTO trace_code (code_id, product_name, batch_no, qr_path) VALUES
('CODE004', '电子产品', 'BATCH002', 'static/qrcode/CODE004.png'),
('CODE005', '电子产品', 'BATCH002', 'static/qrcode/CODE005.png'),
('CODE006', '食品', 'BATCH003', 'static/qrcode/CODE006.png'),
('CODE007', '食品', 'BATCH003', 'static/qrcode/CODE007.png'),
('CODE008', '药品', 'BATCH004', 'static/qrcode/CODE008.png')
ON CONFLICT (code_id) DO NOTHING;

-- 插入更多扫码记录
INSERT INTO scan_record (code_id, ip_address, location, is_first) VALUES
('CODE004', '192.168.1.4', '深圳市', TRUE),
('CODE005', '192.168.1.5', '杭州市', TRUE),
('CODE006', '192.168.1.6', '成都市', TRUE),
('CODE007', '192.168.1.7', '武汉市', TRUE),
('CODE008', '192.168.1.8', '重庆市', TRUE)
ON CONFLICT DO NOTHING;

-- 插入任务数据
INSERT INTO batch_task (batch_no, task_type, status, progress, total, success, failed, product_name) VALUES
('BATCH001', 'generate', 'success', 100, 100, 100, 0, '测试产品'),
('BATCH002', 'generate', 'success', 100, 500, 500, 0, '电子产品'),
('BATCH003', 'export', 'success', 100, 1, 1, 0, '食品')
ON CONFLICT DO NOTHING;
