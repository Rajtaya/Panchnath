import hashlib
import hmac
import json
import time
import base64
import secrets
from starlette.requests import Request

SECRET_KEY = "panchnad-shodh-sansthan-2025-secret-key"


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    h = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}${h}"


def verify_password(password: str, hashed: str) -> bool:
    salt, h = hashed.split("$", 1)
    return hmac.compare_digest(
        hashlib.sha256(f"{salt}{password}".encode()).hexdigest(), h
    )


def create_token(username: str) -> str:
    payload = json.dumps({"user": username, "exp": time.time() + 86400})
    encoded = base64.urlsafe_b64encode(payload.encode()).decode()
    sig = hmac.new(SECRET_KEY.encode(), encoded.encode(), "sha256").hexdigest()
    return f"{encoded}.{sig}"


def verify_token(token: str) -> dict | None:
    try:
        encoded, sig = token.rsplit(".", 1)
        expected = hmac.new(SECRET_KEY.encode(), encoded.encode(), "sha256").hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        data = json.loads(base64.urlsafe_b64decode(encoded))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None


def check_admin(request: Request) -> dict | None:
    token = request.cookies.get("admin_session")
    if token:
        return verify_token(token)
    return None
