from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class CodeReq(BaseModel):
    product_name: str
    batch_no: str

class TraceResponse(BaseModel):
    status: str
    is_first_scan: bool
    scan_count: int
    code_id: str
    product: dict
    batch: dict
    trace: list
    first_scan_time: Optional[str] = None

class TraceInfo(BaseModel):
    time: str
    event: str

class ProductCreate(BaseModel):
    name: str
    type_code: str

class ProductResponse(BaseModel):
    id: int
    name: str
    type_code: str

    class Config:
        from_attributes = True

class BatchCreate(BaseModel):
    product_id: int
    batch_no: str
    production_date: str
    count: int

class BatchResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str] = None
    batch_no: str
    production_date: str
    count: int
    code_count: int = 0
    scan_count: int = 0
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class TraceCodeCreate(BaseModel):
    product_id: int
    batch_id: int
    count: int

class TraceCodeBase(BaseModel):
    code_id: str
    product_name: str
    batch_no: str

class TraceCodeResponse(TraceCodeBase):
    id: int
    scan_count: int
    first_scan_time: Optional[datetime] = None
    last_scan_time: Optional[datetime] = None
    first_scan_ip: Optional[str] = None
    create_time: datetime

    class Config:
        from_attributes = True

class ScanLogResponse(BaseModel):
    id: int
    code_id: str
    ip: Optional[str] = None
    scan_time: datetime
    is_first: bool
    user_agent: Optional[str] = None

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    today_scan: int
    total_codes: int
    total_products: int
    total_batches: int

class BatchCodeReq(BaseModel):
    product_name: str
    batch_no: str
    count: int