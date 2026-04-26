from queue import Queue
import threading
import time
from app.db import SessionLocal
from app.models import BatchTask, TraceCode, Batch, Product
import qrcode
import hashlib
import base64
import os
from datetime import datetime

# 全局任务队列
task_queue = Queue()
BASE_URL = "http://localhost:8000"

def generate_code(product_name: str, batch_no: str) -> str:
    """生成唯一码"""
    timestamp = str(int(time.time() * 1000000))
    data = f"{product_name}-{batch_no}-{timestamp}"
    return hashlib.md5(data.encode()).hexdigest()

def generate_signature(code_id: str) -> str:
    """生成签名"""
    secret = "your-secret-key"
    data = f"{code_id}-{secret}"
    return base64.b64encode(hashlib.sha256(data.encode()).digest()).decode()

def save_code(code_data):
    """保存单个码"""
    code_id, product_name, batch_no, batch_id, product_id = code_data
    sig = generate_signature(code_id)
    url = f"{BASE_URL}/api/verify?code={code_id}&sig={sig}"
    
    # 生成二维码
    img = qrcode.make(url)
    os.makedirs("static/qrcode", exist_ok=True)
    img.save(f"static/qrcode/{code_id}.png")
    
    # 保存到数据库
    db = SessionLocal()
    try:
        trace_code = TraceCode(
            code_id=code_id,
            product_id=product_id,
            batch_id=batch_id,
            status="unused",
            scan_count=0
        )
        db.add(trace_code)
        db.commit()
    finally:
        db.close()

def generate_excel(codes, batch_no):
    """生成Excel文件"""
    import pandas as pd
    
    data = []
    for c in codes:
        # 获取产品信息
        db = SessionLocal()
        try:
            product = db.query(Product).filter(Product.id == c.product_id).first()
            product_name = product.name if product else "未知产品"
            
            # 获取批次信息
            batch = db.query(Batch).filter(Batch.id == c.batch_id).first()
            batch_no = batch.batch_no if batch else "未知批次"
        finally:
            db.close()
        
        data.append({
            "code_id": c.code_id,
            "product": product_name,
            "batch": batch_no
        })
    
    df = pd.DataFrame(data)
    
    os.makedirs("static/export", exist_ok=True)
    path = f"static/export/{batch_no}.xlsx"
    df.to_excel(path, index=False)
    
    return path

def make_zip(excel_path, codes):
    """打包ZIP文件"""
    import zipfile
    
    zip_path = excel_path.replace(".xlsx", ".zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # 添加Excel文件
        z.write(excel_path, arcname=os.path.basename(excel_path))
        
        # 添加二维码图片
        for c in codes:
            qr_path = f"static/qrcode/{c.code_id}.png"
            if os.path.exists(qr_path):
                z.write(qr_path, arcname=f"qrcode/{os.path.basename(qr_path)}")
    
    return zip_path

def run_export(task):
    """执行导出任务"""
    db = SessionLocal()
    
    try:
        task.status = "running"
        task.progress = 10
        db.commit()
        
        # 1️⃣ 查数据
        codes = db.query(TraceCode).join(Batch).filter(
            Batch.batch_no == task.batch_no
        ).all()
        
        if not codes:
            task.status = "failed"
            task.error_msg = "该批次没有二维码数据"
            db.commit()
            return
        
        task.progress = 30
        db.commit()
        
        # 2️⃣ 生成Excel
        excel_path = generate_excel(codes, task.batch_no)
        
        task.progress = 60
        db.commit()
        
        # 3️⃣ 打包ZIP
        zip_path = make_zip(excel_path, codes)
        
        task.progress = 90
        db.commit()
        
        # 4️⃣ 写结果
        task.status = "success"
        task.progress = 100
        task.result_path = zip_path
        task.success = 1
        
        db.commit()
        
    except Exception as e:
        print(f"处理导出任务失败: {e}")
        task.status = "failed"
        task.error_msg = str(e)
        db.commit()
    finally:
        db.close()

def run_generate(task):
    """执行生成任务"""
    db = SessionLocal()
    
    try:
        # 检查是否存在对应的Batch记录
        batch = db.query(Batch).filter(Batch.batch_no == task.batch_no).first()
        if not batch:
            # 创建批次记录
            product = db.query(Product).first()
            product_id = product.id if product else 1
            
            batch = Batch(
                product_id=product_id,
                batch_no=task.batch_no,
                production_date=datetime.now().strftime("%Y-%m-%d"),
                count=task.total,
                product_name=task.product_name,
                status="processing"
            )
            db.add(batch)
            db.commit()
            db.refresh(batch)
        
        # 生成所有code_id
        code_ids = []
        for i in range(task.total):
            code_id = generate_code(task.product_name, task.batch_no)
            code_ids.append((code_id, task.product_name, task.batch_no, batch.id, batch.product_id))
        
        # 执行任务
        for i, code_data in enumerate(code_ids):
            try:
                save_code(code_data)
                task.success += 1
            except Exception as e:
                task.failed += 1
                print(f"处理码失败: {e}")
            
            # 更新进度
            task.progress = int((i+1)/task.total * 100)
            if i % 10 == 0:  # 每10条更新一次数据库
                db.commit()
        
        # 更新批次信息
        batch.count = task.success
        batch.status = "done"
        db.commit()
        
        # 任务完成
        if task.failed > 0:
            task.status = "partial"
        else:
            task.status = "success"
        db.commit()
        
    except Exception as e:
        print(f"处理生成任务失败: {e}")
        task.status = "failed"
        task.error_msg = str(e)
        db.commit()
    finally:
        db.close()

def run_task(task_id):
    """执行任务"""
    db = SessionLocal()
    
    try:
        task = db.query(BatchTask).get(task_id)
        if not task or task.status != "pending":
            return
        
        task.status = "running"
        db.commit()
        
        # 根据任务类型执行不同的处理
        if task.task_type == "generate":
            run_generate(task)
        elif task.task_type == "export":
            run_export(task)
        else:
            task.status = "failed"
            task.error_msg = f"不支持的任务类型: {task.task_type}"
            db.commit()
        
    except Exception as e:
        print(f"处理任务失败: {e}")
        task.status = "failed"
        task.error_msg = str(e)
        db.commit()
    finally:
        db.close()

def worker_loop():
    """worker循环"""
    while True:
        try:
            task_id = task_queue.get()
            print(f"开始处理任务: {task_id}")
            run_task(task_id)
            print(f"任务处理完成: {task_id}")
            task_queue.task_done()
        except Exception as e:
            print(f"Worker错误: {e}")
        
        time.sleep(0.1)

def enqueue_task(task_id):
    """入队任务"""
    task_queue.put(task_id)

def start_worker():
    """启动worker"""
    threading.Thread(target=worker_loop, daemon=True).start()
    print("后台Worker已启动")