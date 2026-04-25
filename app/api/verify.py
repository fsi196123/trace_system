from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from db import SessionLocal
from models import Product, Batch, TraceCode, ScanLog
from utils.security import verify_signature
from redis_client import publish_scan_event
from ip_geo import ip_to_coords
from datetime import datetime
import asyncio

router = APIRouter()

async def broadcast_scan_event(data):
    try:
        from main import manager
        from ip_geo import ip_to_city

        city = ip_to_city(data.get('ip', '')) if data.get('ip') else '未知'

        await manager.broadcast({
            "code_id": data.get('code_id'),
            "ip": data.get('ip'),
            "city": city,
            "count": data.get('scan_count', 1),
            "status": data.get('status'),
            "risk_level": data.get('risk_level', 'low')
        })
    except Exception as e:
        print(f"WebSocket broadcast error: {e}")

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(coro)
        else:
            loop.run_until_complete(coro)
    except RuntimeError:
        asyncio.run(coro)

@router.get("")
def verify(code: str = Query(...), sig: str = Query(...), request: Request = None):
    db = SessionLocal()

    try:
        if not verify_signature(code, sig):
            return HTMLResponse(content="<h1 style='color:red'>❌ 防伪校验失败</h1>")

        data = db.query(TraceCode).filter(
            TraceCode.code_id == code
        ).first()

        if not data:
            return HTMLResponse(content="<h1>❌ 该码不存在</h1>")

        ip = request.client.host if request.client else None
        ua = request.headers.get("user-agent", "") if request else ""

        logs = db.query(ScanLog).filter(
            ScanLog.code_id == code
        ).all()

        ips = set([log.ip for log in logs if log.ip])

        status = "✅ 正品"
        color = "green"
        msg = "首次扫码，验证通过"
        risk_level = "low"

        if not data.is_used:
            data.is_used = True
            data.first_scan_time = datetime.utcnow()
            data.first_scan_ip = ip
            status = "✅ 正品"
            color = "green"
            msg = "首次扫码，验证通过"
            risk_level = "low"

        elif ip in ips:
            status = "⚠️ 重复扫码"
            color = "orange"
            msg = "该码已验证过，请勿重复扫描"
            risk_level = "low"

        elif len(ips) < 3:
            status = "⚠️ 可疑"
            color = "orange"
            msg = "该码在多个设备上被扫描，请注意"
            risk_level = "medium"

        else:
            status = "❌ 高风险"
            color = "red"
            msg = "该码被多地扫描，疑似假货"
            risk_level = "high"

        log = ScanLog(
            code_id=code,
            ip=ip,
            user_agent=ua
        )
        db.add(log)

        data.scan_count += 1
        data.last_scan_time = datetime.utcnow()
        data.status = "used"

        db.commit()

        product = db.query(Product).filter(Product.id == data.product_id).first()
        batch = db.query(Batch).filter(Batch.id == data.batch_id).first()

        product_name = product.name if product else "未知产品"
        batch_no = batch.batch_no if batch else "未知批次"

        # 获取经纬度
        coords = ip_to_coords(ip) if ip else {"lat": 0, "lng": 0}
        
        scan_data = {
            "code_id": code,
            "ip": ip,
            "lat": coords.get("lat", 0),
            "lng": coords.get("lng", 0),
            "city": city,
            "scan_count": data.scan_count,
            "status": status,
            "risk_level": risk_level
        }
        run_async(broadcast_scan_event(scan_data))
        
        # Redis发布实时事件
        publish_scan_event(scan_data)

        return HTMLResponse(content=f"""
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>防伪结果</title>
        </head>
        <body style="font-family: Arial; text-align:center; padding:40px;">
            <h1 style="color:{color}">{status}</h1>
            <p>{msg}</p>
            <hr>
            <p>产品：{product_name}</p>
            <p>批次：{batch_no}</p>
            <p>编码：{code}</p>
            <p>首次扫码IP：{data.first_scan_ip or "-"}</p>
            <p>首次扫码时间：{data.first_scan_time.strftime('%Y-%m-%d %H:%M:%S') if data.first_scan_time else "-"}</p>
            <p>累计扫码次数：{data.scan_count}</p>
            <p>已在 {len(ips) + 1} 个设备上扫码</p>
        </body>
        </html>
        """)

    finally:
        db.close()


@router.get("/json")
def verify_json(code: str = Query(...), sig: str = Query(...), request: Request = None):
    if not verify_signature(code, sig):
        return JSONResponse(content={
            "status": "invalid",
            "message": "防伪校验失败"
        })

    db = SessionLocal()
    try:
        data = db.query(TraceCode).filter(TraceCode.code_id == code).first()
        if not data:
            return JSONResponse(content={
                "status": "invalid",
                "message": "该码不存在"
            })

        product = db.query(Product).filter(Product.id == data.product_id).first()
        batch = db.query(Batch).filter(Batch.id == data.batch_id).first()

        ip = request.client.host if request.client else None
        ua = request.headers.get("user-agent", "") if request else ""

        logs = db.query(ScanLog).filter(ScanLog.code_id == code).all()
        ips = set([log.ip for log in logs if log.ip])

        is_first_scan = False
        risk_level = "low"
        message = "验证通过"

        if not data.is_used:
            data.is_used = True
            data.first_scan_time = datetime.utcnow()
            data.first_scan_ip = ip
            is_first_scan = True
            risk_level = "low"
            message = "首次扫码，验证通过"

        elif ip in ips:
            risk_level = "low"
            message = "该码已验证过，请勿重复扫描"

        elif len(ips) < 3:
            risk_level = "medium"
            message = "该码在多个设备上被扫描，请注意"

        else:
            risk_level = "high"
            message = "该码被多地扫描，疑似假货"

        log = ScanLog(code_id=code, ip=ip, user_agent=ua)
        db.add(log)

        data.scan_count += 1
        data.last_scan_time = datetime.utcnow()
        data.status = "used"

        db.commit()

        product_name = product.name if product else ""
        product_type = product.type_code if product else ""
        batch_no = batch.batch_no if batch else ""
        production_date = batch.production_date if batch else ""

        trace_list = [
            {"time": data.create_time.strftime("%Y-%m-%d %H:%M") if data.create_time else "", "event": "生产"},
            {"time": data.first_scan_time.strftime("%Y-%m-%d %H:%M") if data.first_scan_time else "", "event": "首次扫码", "location": data.first_scan_ip or ""},
        ]

        if data.last_scan_time and data.last_scan_time != data.first_scan_time:
            trace_list.append({
                "time": data.last_scan_time.strftime("%Y-%m-%d %H:%M"),
                "event": "最近扫码",
                "location": ip or ""
            })

        # 获取经纬度
        coords = ip_to_coords(ip) if ip else {"lat": 0, "lng": 0}
        city = "未知"  # 简化处理
        
        scan_data = {
            "code_id": code,
            "ip": ip,
            "lat": coords.get("lat", 0),
            "lng": coords.get("lng", 0),
            "city": city,
            "scan_count": data.scan_count,
            "status": "valid" if is_first_scan else ("warning" if risk_level == "medium" else "danger"),
            "risk_level": risk_level
        }
        run_async(broadcast_scan_event(scan_data))
        
        # Redis发布实时事件
        publish_scan_event(scan_data)

        return JSONResponse(content={
            "status": "valid",
            "is_first_scan": is_first_scan,
            "scan_count": data.scan_count,
            "code_id": code,
            "product": {
                "name": product_name,
                "type": product_type
            },
            "batch": {
                "batch_no": batch_no,
                "production_date": production_date
            },
            "trace": trace_list,
            "first_scan_time": data.first_scan_time.strftime("%Y-%m-%d %H:%M") if data.first_scan_time else None,
            "first_scan_ip": data.first_scan_ip,
            "risk_level": risk_level,
            "message": message,
            "device_count": len(ips) + 1
        })
    finally:
        db.close()