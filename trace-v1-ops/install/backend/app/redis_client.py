import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=5
)

def publish_scan_event(data):
    try:
        r.publish("scan_event", json.dumps(data))
        return True
    except Exception as e:
        print(f"Redis publish error: {e}")
        return False
