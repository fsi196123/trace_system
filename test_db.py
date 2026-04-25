from app.db import engine, SessionLocal
from app.models import Base, Product, Batch, TraceCode, ScanLog, BatchTask

# 测试数据库连接
print("Testing database connection...")
try:
    # 测试创建表
    Base.metadata.create_all(bind=engine)
    print("✓ Database connection successful")
    
    # 测试Session
    db = SessionLocal()
    print("✓ Session created successfully")
    
    # 测试查询
    count = db.query(Product).count()
    print(f"✓ Product count: {count}")
    
    db.close()
    print("✓ All tests passed")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()