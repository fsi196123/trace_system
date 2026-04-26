import random
import string
from datetime import datetime

def generate_code(product_name: str, batch_no: str):
    prefix = product_name[:3].upper()
    date_str = datetime.now().strftime("%Y%m%d")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    return f"{prefix}-{date_str}-{batch_no}-{rand}"