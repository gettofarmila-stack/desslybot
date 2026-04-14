import json
import hmac
import hashlib
import logging
import base64
from config import SIGN_2328

def generate_sign(data: dict):
    global SIGN_2328
    json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    base64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    sign = hmac.new(key=SIGN_2328.encode('utf-8'), msg=base64_str.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    return sign