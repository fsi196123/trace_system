import hmac
import hashlib

SECRET_KEY = "trace_secret_2026"


def generate_signature(code_id: str) -> str:
    msg = code_id.encode()
    key = SECRET_KEY.encode()

    sig = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return sig[:6].upper()   # 取前6位


def verify_signature(code_id: str, sig: str) -> bool:
    expected = generate_signature(code_id)
    return expected == sig