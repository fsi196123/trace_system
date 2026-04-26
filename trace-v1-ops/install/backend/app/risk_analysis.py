from db import SessionLocal
from models import ScanLog
from datetime import datetime, timedelta

def build_spread_graph(code_id):
    """构建传播关系图"""
    db = SessionLocal()
    try:
        logs = db.query(ScanLog).filter_by(code_id=code_id).all()
        
        graph = {}
        graph[code_id] = []
        
        for log in logs:
            if log.ip:
                graph[code_id].append({
                    "ip": log.ip,
                    "scan_time": log.scan_time.isoformat() if log.scan_time else None,
                    "city": "未知"  # 可以从IP获取
                })
        
        return graph
    finally:
        db.close()

def spread_risk(logs):
    """风险传播模型"""
    risk = 0
    ip_map = {}
    
    for l in logs:
        if l.ip:
            ip_map[l.ip] = ip_map.get(l.ip, 0) + 1
    
    # 高频IP = 克隆攻击
    for ip, cnt in ip_map.items():
        if cnt > 3:
            risk += 40
    
    # 多地传播
    cities = set()
    for l in logs:
        # 这里可以从IP获取城市信息
        cities.add("未知")
    if len(cities) > 2:
        risk += 30
    
    # 快速扩散（短时间多次扫码）
    if len(logs) > 10:
        risk += 20
    
    return min(risk, 100)

def get_risk_level(risk_score):
    """根据风险分数获取风险等级"""
    if risk_score >= 70:
        return "high"
    elif risk_score >= 40:
        return "medium"
    else:
        return "low"

def analyze_code_risk(code_id):
    """分析单个码的风险"""
    db = SessionLocal()
    try:
        logs = db.query(ScanLog).filter_by(code_id=code_id).all()
        
        if not logs:
            return {
                "code_id": code_id,
                "risk_score": 0,
                "risk_level": "low",
                "scan_count": 0,
                "ip_count": 0
            }
        
        risk_score = spread_risk(logs)
        risk_level = get_risk_level(risk_score)
        
        ip_set = set()
        for log in logs:
            if log.ip:
                ip_set.add(log.ip)
        
        return {
            "code_id": code_id,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "scan_count": len(logs),
            "ip_count": len(ip_set)
        }
    finally:
        db.close()

def get_high_risk_codes(limit=10):
    """获取高风险码列表"""
    db = SessionLocal()
    try:
        # 获取所有有扫描记录的码
        codes = db.query(ScanLog.code_id).distinct().all()
        
        risk_list = []
        for (code_id,) in codes:
            risk_data = analyze_code_risk(code_id)
            if risk_data["risk_level"] in ["high", "medium"]:
                risk_list.append(risk_data)
        
        # 按风险分数排序
        risk_list.sort(key=lambda x: x["risk_score"], reverse=True)
        
        return risk_list[:limit]
    finally:
        db.close()
