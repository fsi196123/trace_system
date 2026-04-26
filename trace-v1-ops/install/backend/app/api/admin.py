from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Product, Batch, TraceCode, ScanLog
from schemas import (
    ProductCreate, ProductResponse,
    BatchCreate, BatchResponse,
    TraceCodeCreate, TraceCodeResponse,
    ScanLogResponse, DashboardStats
)
from datetime import datetime, date
from typing import List
import random
import string

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_code_id(product_type: str, batch_no: str) -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    seq = ''.join(random.choices(string.digits, k=6))
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{product_type}-{date_str}-{seq}-{rand}"

@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())

    today_scan = db.query(ScanLog).filter(ScanLog.scan_time >= today_start).count()
    total_codes = db.query(TraceCode).count()
    total_products = db.query(Product).count()
    total_batches = db.query(Batch).count()

    return DashboardStats(
        today_scan=today_scan,
        total_codes=total_codes,
        total_products=total_products,
        total_batches=total_batches
    )

@router.get("/products", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).order_by(Product.id.desc()).all()
    return products

@router.post("/products", response_model=ProductResponse)
def create_product(req: ProductCreate, db: Session = Depends(get_db)):
    product = Product(name=req.name, type_code=req.type_code)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, req: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    product.name = req.name
    product.type_code = req.type_code
    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    db.delete(product)
    db.commit()
    return {"message": "删除成功"}

@router.get("/batches", response_model=List[BatchResponse])
def list_batches(db: Session = Depends(get_db)):
    batches = db.query(Batch).order_by(Batch.id.desc()).all()
    result = []
    for batch in batches:
        product = db.query(Product).filter(Product.id == batch.product_id).first()
        code_count = db.query(TraceCode).filter(TraceCode.batch_id == batch.id).count()
        scan_count = db.query(ScanLog).join(TraceCode, ScanLog.code_id == TraceCode.code_id).filter(TraceCode.batch_id == batch.id).count()
        result.append(BatchResponse(
            id=batch.id,
            product_id=batch.product_id,
            product_name=product.name if product else "未知",
            batch_no=batch.batch_no,
            production_date=batch.production_date,
            count=batch.count,
            code_count=code_count,
            scan_count=scan_count,
            create_time=batch.create_time
        ))
    return result

@router.post("/batches", response_model=BatchResponse)
def create_batch(req: BatchCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")

    batch = Batch(
        product_id=req.product_id,
        batch_no=req.batch_no,
        production_date=req.production_date,
        count=req.count
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch

@router.put("/batches/{batch_id}", response_model=BatchResponse)
def update_batch(batch_id: int, req: BatchCreate, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="批次不存在")
    batch.product_id = req.product_id
    batch.batch_no = req.batch_no
    batch.production_date = req.production_date
    batch.count = req.count
    db.commit()
    db.refresh(batch)
    return batch

@router.delete("/batches/{batch_id}")
def delete_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="批次不存在")
    db.delete(batch)
    db.commit()
    return {"message": "删除成功"}

@router.get("/codes", response_model=List[TraceCodeResponse])
def list_codes(product_id: int = None, status: str = None, db: Session = Depends(get_db)):
    query = db.query(TraceCode)
    if product_id:
        query = query.filter(TraceCode.product_id == product_id)
    if status == "unused":
        query = query.filter(TraceCode.scan_count == 0)
    elif status == "used":
        query = query.filter(TraceCode.scan_count > 0)
    codes = query.order_by(TraceCode.id.desc()).limit(100).all()
    return codes

@router.post("/codes/generate")
def generate_codes(req: TraceCodeCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")

    batch = db.query(Batch).filter(Batch.id == req.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="批次不存在")

    codes = []
    for _ in range(req.count):
        code_id = generate_code_id(product.type_code, batch.batch_no)
        trace_code = TraceCode(
            code_id=code_id,
            product_id=req.product_id,
            batch_id=req.batch_id,
            status="unused"
        )
        db.add(trace_code)
        codes.append(code_id)

    db.commit()
    return {"count": len(codes), "codes": codes[:10], "message": f"成功生成 {len(codes)} 个溯源码"}

@router.get("/codes/export")
def export_codes(batch_id: int = None, db: Session = Depends(get_db)):
    query = db.query(TraceCode)
    if batch_id:
        query = query.filter(TraceCode.batch_id == batch_id)
    codes = query.all()
    return {"count": len(codes), "message": "导出功能需要实现文件压缩"}

@router.get("/scan-logs", response_model=List[ScanLogResponse])
def list_scan_logs(code_id: str = None, db: Session = Depends(get_db)):
    query = db.query(ScanLog)
    if code_id:
        query = query.filter(ScanLog.code_id == code_id)
    logs = query.order_by(ScanLog.id.desc()).limit(100).all()
    return logs

@router.get("/recent-scans")
def recent_scans(db: Session = Depends(get_db)):
    logs = db.query(ScanLog).order_by(ScanLog.id.desc()).limit(10).all()
    result = []
    for log in logs:
        code = db.query(TraceCode).filter(TraceCode.code_id == log.code_id).first()
        product_name = "未知产品"
        if code:
            product = db.query(Product).filter(Product.id == code.product_id).first()
            if product:
                product_name = product.name
        result.append({
            "code_id": log.code_id,
            "product_name": product_name,
            "scan_time": log.scan_time.strftime("%Y-%m-%d %H:%M"),
            "is_first": log.is_first
        })
    return result
