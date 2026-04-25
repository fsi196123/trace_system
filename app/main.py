from fastapi import FastAPI, Depends, Form, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import engine, SessionLocal
from models import Base, TraceCode, Product, Batch, ScanLog
from api.code import router as code_router
from api.verify import router as verify_router
from api.admin import router as admin_router
from websocket_manager import manager
from redis_client import r
from risk_analysis import build_spread_graph, analyze_code_risk, get_high_risk_codes
from ip_geo import ip_to_city, ip_to_province, ip_to_coords, get_heatmap_data
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os
import zipfile
import shutil
import asyncio

def init_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(code_router, prefix="/api/code")
app.include_router(verify_router, prefix="/api/verify")
app.include_router(admin_router, prefix="/api/admin")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"msg": "ok"}

@app.get("/dashboard")
def dashboard():
    return {"message": "Dashboard API", "status": "ok"}

@app.get("/heatmap")
def heatmap():
    return {"message": "Heatmap API", "status": "ok"}

@app.get("/api/stats/heatmap")
def get_heatmap_stats(db: Session = Depends(get_db)):
    logs = db.query(ScanLog).order_by(ScanLog.scan_time.desc()).limit(500).all()

    city_count = {}
    for log in logs:
        city = ip_to_city(log.ip) if log.ip else "未知"
        if city in city_count:
            city_count[city] += 1
        else:
            city_count[city] = 1

    result = []
    for city, count in city_count.items():
        coords = ip_to_coords(log.ip if log.ip else "127.0.0.1")
        result.append({
            "city": city,
            "value": count,
            "coords": coords
        })

    return {"data": result}

@app.get("/api/stats/risk")
def get_risk_stats(db: Session = Depends(get_db)):
    today = datetime.now().date()

    codes_with_scans = db.query(TraceCode).filter(
        TraceCode.last_scan_time >= today
    ).all()

    total = len(codes_with_scans)
    valid = sum(1 for c in codes_with_scans if c.scan_count == 1)
    warn = sum(1 for c in codes_with_scans if 1 < c.scan_count < 3)
    risk = sum(1 for c in codes_with_scans if c.scan_count >= 3)

    return {
        "total": total,
        "valid": valid,
        "warn": warn,
        "risk": risk
    }

@app.websocket("/ws/dashboard")
async def dashboard_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

@app.websocket("/ws/scan")
async def ws_scan(websocket: WebSocket):
    await websocket.accept()
    
    try:
        pubsub = r.pubsub()
        pubsub.subscribe("scan_event")
        
        # 异步监听Redis消息
        for msg in pubsub.listen():
            if msg["type"] == "message":
                await websocket.send_text(msg["data"])
                await asyncio.sleep(0.01)  # 避免阻塞
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        try:
            pubsub.unsubscribe("scan_event")
        except:
            pass

@app.get("/api/trace/{code_id}")
def trace(code_id: str, db: Session = Depends(get_db)):
    data = db.query(TraceCode).filter(TraceCode.code_id == code_id).first()

    if not data:
        return {"status": "invalid", "message": "该码不存在"}

    product = db.query(Product).filter(Product.id == data.product_id).first()
    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()

    is_first = data.scan_count == 0

    trace_list = [
        {"time": data.create_time.strftime("%Y-%m-%d %H:%M") if data.create_time else "", "event": "生产"},
        {"time": data.create_time.strftime("%Y-%m-%d %H:%M") if data.create_time else "", "event": "入库"},
    ]

    if data.first_scan_time:
        trace_list.append({
            "time": data.first_scan_time.strftime("%Y-%m-%d %H:%M"),
            "event": "首次扫码"
        })

    if data.last_scan_time and data.last_scan_time != data.first_scan_time:
        trace_list.append({
            "time": data.last_scan_time.strftime("%Y-%m-%d %H:%M"),
            "event": "最近扫码"
        })

    return {
        "status": "valid",
        "is_first_scan": is_first,
        "scan_count": data.scan_count,
        "code_id": code_id,
        "product": {
            "name": product.name if product else data.product_name,
            "type": product.type_code if product else ""
        },
        "batch": {
            "batch_no": batch.batch_no if batch else data.batch_no,
            "production_date": batch.production_date if batch else ""
        },
        "trace": trace_list,
        "first_scan_time": data.first_scan_time.strftime("%Y-%m-%d %H:%M") if data.first_scan_time else None
    }

@app.get("/api/risk/analyze/{code_id}")
def analyze_risk(code_id: str):
    """分析单个码的风险"""
    return analyze_code_risk(code_id)

@app.get("/api/risk/spread/{code_id}")
def get_spread_graph(code_id: str):
    """获取传播关系图"""
    return build_spread_graph(code_id)

@app.get("/api/risk/high")
def get_high_risk():
    """获取高风险码列表"""
    return get_high_risk_codes()



@app.post("/admin/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin123":
        db = SessionLocal()
        codes = db.query(TraceCode).all()
        result = []
        for code in codes:
            product = db.query(Product).filter(Product.id == code.product_id).first()
            batch = db.query(Batch).filter(Batch.id == code.batch_id).first()
            result.append({
                "code_id": code.code_id,
                "product_name": product.name if product else "未知",
                "batch_no": batch.batch_no if batch else "未知",
                "create_time": code.create_time.strftime("%Y-%m-%d %H:%M") if code.create_time else "-",
                "scan_count": code.scan_count,
                "first_scan_time": code.first_scan_time.strftime("%Y-%m-%d %H:%M") if code.first_scan_time else "-",
                "first_scan_ip": code.first_scan_ip or "-"
            })
        db.close()
        return {
            "status": "success",
            "data": result,
            "message": "登录成功"
        }
    else:
        return {
            "status": "error",
            "message": "用户名或密码错误"
        }

@app.get("/admin/codes")
def codes():
    db = SessionLocal()
    codes = db.query(TraceCode).all()
    result = []
    for code in codes:
        product = db.query(Product).filter(Product.id == code.product_id).first()
        batch = db.query(Batch).filter(Batch.id == code.batch_id).first()
        result.append({
            "code_id": code.code_id,
            "product_name": product.name if product else "未知",
            "batch_no": batch.batch_no if batch else "未知",
            "create_time": code.create_time.strftime("%Y-%m-%d %H:%M") if code.create_time else "-",
            "scan_count": code.scan_count,
            "first_scan_time": code.first_scan_time.strftime("%Y-%m-%d %H:%M") if code.first_scan_time else "-",
            "first_scan_ip": code.first_scan_ip or "-"
        })
    db.close()
    return {
        "status": "success",
        "data": result
    }

@app.get("/admin/logs")
def logs():
    db = SessionLocal()
    logs = db.query(ScanLog).order_by(ScanLog.scan_time.desc()).all()
    result = []
    for log in logs:
        result.append({
            "code_id": log.code_id,
            "ip": log.ip or "-",
            "scan_time": log.scan_time.strftime("%Y-%m-%d %H:%M:%S") if log.scan_time else "-",
            "user_agent": log.user_agent or "-"
        })
    db.close()
    return {
        "status": "success",
        "data": result
    }

@app.get("/admin/export")
def export_excel():
    db = SessionLocal()
    data = db.query(TraceCode).all()

    rows = []
    for item in data:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        batch = db.query(Batch).filter(Batch.id == item.batch_id).first()
        rows.append({
            "编码": item.code_id,
            "产品": product.name if product else "未知",
            "批次": batch.batch_no if batch else "未知"
        })

    df = pd.DataFrame(rows)

    file_path = "codes.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="codes.xlsx")

@app.get("/admin/export/package")
def export_package():
    db = SessionLocal()

    export_dir = "export"
    qr_dir = os.path.join(export_dir, "qrcodes")

    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)

    os.makedirs(qr_dir, exist_ok=True)

    data = db.query(TraceCode).all()

    rows = []

    for item in data:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        batch = db.query(Batch).filter(Batch.id == item.batch_id).first()
        rows.append({
            "编码": item.code_id,
            "产品": product.name if product else "未知",
            "批次": batch.batch_no if batch else "未知",
            "二维码": f"qrcodes/{item.code_id}.png"
        })

        src = f"static/qrcode/{item.code_id}.png"
        dst = os.path.join(qr_dir, f"{item.code_id}.png")

        if os.path.exists(src):
            if not os.path.exists(dst):
                shutil.copy(src, dst)

    excel_path = os.path.join(export_dir, "codes.xlsx")
    df = pd.DataFrame(rows)
    df.to_excel(excel_path, index=False)

    zip_path = "trace_package.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(excel_path, arcname="codes.xlsx")

        for root, dirs, files in os.walk(qr_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, export_dir)
                z.write(full_path, arcname)

    db.close()

    return FileResponse(zip_path, filename="trace_package.zip")

@app.get("/admin/print/a4")
def print_a4():
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    db = SessionLocal()
    data = db.query(TraceCode).limit(48).all()

    file_path = "qrcode_a4.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    elements = []
    styles = getSampleStyleSheet()

    table_data = []
    row = []

    count_per_row = 6

    for i, item in enumerate(data):
        img_path = f"static/qrcode/{item.code_id}.png"

        if not os.path.exists(img_path):
            continue

        product = db.query(Product).filter(Product.id == item.product_id).first()
        batch = db.query(Batch).filter(Batch.id == item.batch_id).first()

        img = Image(img_path, width=70, height=70)

        text = Paragraph(
            f"{product.name if product else item.product_name}<br/>{batch.batch_no if batch else item.batch_no}<br/>{item.code_id}",
            styles["Normal"]
        )

        cell = [img, text]
        row.append(cell)

        if len(row) == count_per_row:
            table_data.append(row)
            row = []

    if row:
        while len(row) < count_per_row:
            empty_img = Paragraph("", styles["Normal"])
            empty_text = Paragraph("", styles["Normal"])
            row.append([empty_img, empty_text])
        table_data.append(row)

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))

    elements.append(table)

    doc.build(elements)

    db.close()

    return FileResponse(file_path, filename="二维码A4打印.pdf")

@app.get("/admin/print/a4/industrial")
def print_a4_industrial(
    batch_no: str = Query(None),
    cols: int = 6
):
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer, PageBreak
    )
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    db = SessionLocal()

    query = db.query(TraceCode)

    if batch_no:
        batch = db.query(Batch).filter(Batch.batch_no == batch_no).first()
        if batch:
            query = query.filter(TraceCode.batch_id == batch.id)

    data = query.all()

    file_path = "industrial_qr_print.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    styles = getSampleStyleSheet()

    elements = []

    header = Paragraph(
        f"""
        <b style='font-size:16px'>防伪二维码批量打印</b><br/>
        批次号：{batch_no if batch_no else '全部'}<br/>
        共 {len(data)} 个二维码
        """,
        styles["Normal"]
    )

    elements.append(header)
    elements.append(Spacer(1, 10))

    rows_per_page = 48
    per_page = rows_per_page

    chunked = [data[i:i+per_page] for i in range(0, len(data), per_page)]

    for page_index, page_data in enumerate(chunked):

        table_data = []
        row = []

        for i, item in enumerate(page_data):

            img_path = f"static/qrcode/{item.code_id}.png"

            if not os.path.exists(img_path):
                continue

            qr = Image(img_path, width=70, height=70)

            product = db.query(Product).filter(Product.id == item.product_id).first()
            batch = db.query(Batch).filter(Batch.id == item.batch_id).first()

            text = Paragraph(
                f"""
                <b>{product.name if product else '未知产品'}</b><br/>
                批次：{batch.batch_no if batch else '未知批次'}<br/>
                编码：{item.code_id}
                """,
                styles["Normal"]
            )

            cell = [qr, text]
            row.append(cell)

            if len(row) == cols:
                table_data.append(row)
                row = []

        if row:
            while len(row) < cols:
                empty_img = Paragraph("", styles["Normal"])
                empty_text = Paragraph("", styles["Normal"])
                row.append([empty_img, empty_text])
            table_data.append(row)

        table = Table(table_data)

        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))

        elements.append(table)

        footer = Paragraph(
            """
            <br/>
            <b>防伪说明：</b><br/>
            本二维码为唯一标识，扫描可验证产品真伪。<br/>
            如发现异常扫码记录，请联系官方渠道。
            """,
            styles["Normal"]
        )

        elements.append(Spacer(1, 10))
        elements.append(footer)

        if page_index < len(chunked) - 1:
            elements.append(PageBreak())

    doc.build(elements)

    db.close()

    return FileResponse(
        file_path,
        filename=f"工业级二维码打印_{batch_no or 'ALL'}.pdf"
    )

from worker import start_worker, enqueue_task

@app.on_event("startup")
def startup():
    init_db()
    # 启动后台worker
    start_worker()
    print("后台Worker已启动")