import json
from django.contrib.auth.hashers import make_password

from .redis_client import redis_client

PENDING_REGISTRATION_TTL = 120


def normalize_email(email: str) -> str:
    return email.strip().lower()


def get_pending_user_key(email: str) -> str:
    return f"pending_user:{normalize_email(email)}"


def save_pending_registration(email: str, full_name: str, password: str) -> None:
    email = normalize_email(email)
    full_name = full_name.strip()

    hashed_password = make_password(password)

    data = {
        "email": email,
        "full_name": full_name,
        "password": hashed_password,
    }

    redis_client.setex(
        get_pending_user_key(email),
        PENDING_REGISTRATION_TTL,
        json.dumps(data),
    )


def get_pending_registration(email: str) -> dict | None:
    email = normalize_email(email)

    data = redis_client.get(get_pending_user_key(email))
    if not data:
        return None

    return json.loads(data)


def delete_pending_registration(email: str) -> None:
    email = normalize_email(email)
    redis_client.delete(get_pending_user_key(email))