from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type_code = Column(String(20), nullable=False)
    create_time = Column(DateTime(timezone=True), server_default=func.now())

class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    batch_no = Column(String(50), nullable=False)
    production_date = Column(String(20))
    count = Column(Integer, default=0)
    product_name = Column(String(100))
    status = Column(String(20), default="processing")  # processing / done
    create_time = Column(DateTime(timezone=True), server_default=func.now())

class ScanLog(Base):
    __tablename__ = "scan_log"

    id = Column(Integer, primary_key=True)
    code_id = Column(String)
    ip = Column(String)
    user_agent = Column(String)
    scan_time = Column(DateTime, default=datetime.utcnow)
    is_first = Column(Boolean, default=False)

class TraceCode(Base):
    __tablename__ = "trace_code"

    id = Column(Integer, primary_key=True, index=True)
    code_id = Column(String(64), unique=True, index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("batch.id"), nullable=False)

    # ⭐ 核心字段：是否已被使用
    is_used = Column(Boolean, default=False)
    first_scan_time = Column(DateTime, nullable=True)
    first_scan_ip = Column(String, nullable=True)

    # 保留旧字段以兼容
    status = Column(String(20), default="unused")
    scan_count = Column(Integer, default=0)
    last_scan_time = Column(DateTime, nullable=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now())

class BatchTask(Base):
    __tablename__ = "batch_task"

    id = Column(Integer, primary_key=True)
    batch_no = Column(String(50), index=True)
    task_type = Column(String(20))  # generate/export
    status = Column(String(20), default="pending")  # pending/running/success/failed/partial
    progress = Column(Integer, default=0)  # 0-100
    total = Column(Integer)
    success = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    error_msg = Column(String, nullable=True)
    result_path = Column(String, nullable=True)  # 导出结果路径
    product_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())