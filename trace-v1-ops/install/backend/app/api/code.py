from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Product, Batch, TraceCode, ScanLog
from utils.security import generate_signature
from schemas import CodeReq, TraceResponse, TraceInfo, BatchCodeReq
from pydantic import BaseModel

class ExportReq(BaseModel):
    batch_no: str
from datetime import datetime
import qrcode
import os
import pandas as pd
import zipfile
import shutil

router = APIRouter()

BASE_URL = "http://localhost:8000"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list")
def list_codes(db: Session = Depends(get_db)):
    codes = db.query(TraceCode).all()
    result = []
    for i in codes:
        product = db.query(Product).filter(Product.id == i.product_id).first()
        batch = db.query(Batch).filter(Batch.id == i.batch_id).first()
        result.append({
            "code_id": i.code_id,
            "product_name": product.name if product else "未知",
            "batch_no": batch.batch_no if batch else "未知",
            "scan_count": i.scan_count
        })
    return result

@router.post("/generate")
def generate(req: CodeReq, db: Session = Depends(get_db)):
    code_service = None
    from service.code_service import generate_code as gen_code
    from service.qrcode_service import generate_qrcode

    code_id = gen_code(req.product_name, req.batch_no)
    sig = generate_signature(code_id)
    url = f"{BASE_URL}/api/verify?code={code_id}&sig={sig}"

    os.makedirs("static/qrcode", exist_ok=True)
    qr_path = f"static/qrcode/{code_id}.png"
    img = qrcode.make(url)
    img.save(qr_path)

    # 先查找或创建产品
    product = db.query(Product).filter(Product.name == req.product_name).first()
    if not product:
        product = Product(name=req.product_name, type_code="default")
        db.add(product)
        db.flush()

    # 先查找或创建批次
    batch = db.query(Batch).filter(Batch.batch_no == req.batch_no).first()
    if not batch:
        batch = Batch(product_id=product.id, batch_no=req.batch_no, production_date=datetime.now().strftime("%Y-%m-%d"))
        db.add(batch)
        db.flush()

    data = TraceCode(
        code_id=code_id, 
        product_id=product.id, 
        batch_id=batch.id
    )
    db.add(data)
    db.commit()

    return {"code_id": code_id, "qr_url": url}

from models import BatchTask

from worker import enqueue_task

@router.post("/batch_generate")
def batch_generate(req: BatchCodeReq, db: Session = Depends(get_db)):
    # 创建任务
    task = BatchTask(
        batch_no=req.batch_no,
        task_type="generate",
        status="pending",
        total=req.count,
        product_name=req.product_name
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # 丢给worker
    enqueue_task(task.id)

    return {
        "task_id": task.id,
        "message": "任务已提交，后台处理中"
    }

@router.post("/export/create")
def create_export(req: ExportReq, db: Session = Depends(get_db)):
    # 创建导出任务
    task = BatchTask(
        batch_no=req.batch_no,
        task_type="export",
        status="pending",
        total=1,
        progress=0
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # 丢给worker
    enqueue_task(task.id)

    return {
        "task_id": task.id,
        "message": "导出任务已提交，后台处理中"
    }

@router.delete("/{code_id}")
def delete_code(code_id: str, db: Session = Depends(get_db)):
    db.query(TraceCode).filter(TraceCode.code_id == code_id).delete()
    db.commit()
    return {"msg": "deleted"}

@router.get("/export/excel")
def export_codes_excel(batch_no: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(TraceCode)
    
    if batch_no:
        batch = db.query(Batch).filter(Batch.batch_no == batch_no).first()
        if batch:
            query = query.filter(TraceCode.batch_id == batch.id)

    data = query.all()

    rows = []
    for item in data:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        batch = db.query(Batch).filter(Batch.id == item.batch_id).first()
        sig = generate_signature(item.code_id)
        url = f"{BASE_URL}/api/verify?code={item.code_id}&sig={sig}"
        rows.append({
            "code_id": item.code_id,
            "产品": product.name if product else "未知",
            "批次": batch.batch_no if batch else "未知",
            "验证URL": url,
            "状态": "正常" if item.scan_count == 0 else "已扫码"
        })

    df = pd.DataFrame(rows)

    os.makedirs("static/export", exist_ok=True)
    file_path = f"static/export/{batch_no or 'all'}.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename=f"trace_codes_{batch_no or 'all'}.xlsx")

@router.get("/export/zip")
def export_codes_zip(batch_no: str = Query(None), db: Session = Depends(get_db)):
    export_dir = "static/export"
    qr_dir = os.path.join(export_dir, "qrcodes")

    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)

    os.makedirs(qr_dir, exist_ok=True)

    query = db.query(TraceCode)
    
    if batch_no:
        batch = db.query(Batch).filter(Batch.batch_no == batch_no).first()
        if batch:
            query = query.filter(TraceCode.batch_id == batch.id)

    data = query.all()

    rows = []

    for item in data:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        batch = db.query(Batch).filter(Batch.id == item.batch_id).first()
        rows.append({
            "code_id": item.code_id,
            "产品": product.name if product else "未知",
            "批次": batch.batch_no if batch else "未知"
        })

        src = f"static/qrcode/{item.code_id}.png"
        dst = os.path.join(qr_dir, f"{item.code_id}.png")

        if os.path.exists(src):
            if not os.path.exists(dst):
                shutil.copy(src, dst)

    excel_path = os.path.join(export_dir, f"{batch_no or 'all'}.xlsx")
    df = pd.DataFrame(rows)
    df.to_excel(excel_path, index=False)

    zip_path = f"static/export/{batch_no or 'all'}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(excel_path, arcname=f"{batch_no or 'all'}.xlsx")

        for root, dirs, files in os.walk(qr_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, export_dir)
                z.write(full_path, arcname)

    return FileResponse(zip_path, filename=f"qrcodes_{batch_no or 'all'}.zip")

@router.get("/task/{id}")
def task_status(id: int, db: Session = Depends(get_db)):
    task = db.query(BatchTask).get(id)
    
    if not task:
        return {"error": "任务不存在"}
    
    return {
        "status": task.status,
        "progress": task.progress,
        "success": task.success,
        "failed": task.failed,
        "total": task.total,
        "error_msg": task.error_msg,
        "result_path": task.result_path
    }

@router.get("/download/{file_path:path}")
def download_file(file_path: str):
    """下载文件"""
    # 安全检查，确保文件路径在static目录内
    if not file_path.startswith("static/"):
        return {"error": "非法文件路径"}
    
    if not os.path.exists(file_path):
        return {"error": "文件不存在"}
    
    return FileResponse(file_path, filename=os.path.basename(file_path))

@router.get("/task/list")
def task_list(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    """获取任务列表"""
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 查询任务列表
    tasks = db.query(BatchTask).order_by(BatchTask.created_at.desc()).offset(offset).limit(page_size).all()
    total = db.query(BatchTask).count()
    
    # 统计数据
    running = db.query(BatchTask).filter(BatchTask.status == "running").count()
    success = db.query(BatchTask).filter(BatchTask.status == "success").count()
    failed = db.query(BatchTask).filter(BatchTask.status == "failed").count()
    
    # 格式化任务数据
    task_list = []
    for task in tasks:
        task_list.append({
            "id": task.id,
            "batch_no": task.batch_no,
            "task_type": task.task_type,
            "status": task.status,
            "progress": task.progress,
            "total": task.total,
            "success": task.success,
            "failed": task.failed,
            "result_path": task.result_path,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        })
    
    return {
        "items": task_list,
        "total": total,
        "stats": {
            "running": running,
            "success": success,
            "failed": failed,
            "total": total
        }
    }

@router.post("/task/retry")
def retry_task(req: dict, db: Session = Depends(get_db)):
    """重试任务"""
    task_id = req.get("task_id")
    if not task_id:
        return {"error": "缺少任务ID"}
    
    task = db.query(BatchTask).get(task_id)
    if not task:
        return {"error": "任务不存在"}
    
    if task.status not in ["failed", "partial"]:
        return {"error": "只有失败或部分成功的任务可以重试"}
    
    # 创建新任务
    new_task = BatchTask(
        batch_no=task.batch_no,
        task_type=task.task_type,
        status="pending",
        total=task.total,
        product_name=task.product_name
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # 丢给worker
    enqueue_task(new_task.id)
    
    return {
        "task_id": new_task.id,
        "message": "任务已重新提交"
    }