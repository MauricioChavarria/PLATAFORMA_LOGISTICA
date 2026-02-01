from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


_ALG = "sha256"
_ITERATIONS = 210_000


def hash_password(password: str) -> str:
    if not isinstance(password, str) or len(password) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres")

    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac(_ALG, password.encode("utf-8"), salt, _ITERATIONS)
    salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
    dk_b64 = base64.urlsafe_b64encode(dk).decode("ascii").rstrip("=")
    return f"pbkdf2_{_ALG}${_ITERATIONS}${salt_b64}${dk_b64}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        scheme, iter_s, salt_b64, dk_b64 = password_hash.split("$", 3)
        if not scheme.startswith("pbkdf2_"):
            return False
        alg = scheme.replace("pbkdf2_", "", 1)
        iterations = int(iter_s)

        salt = _b64decode_nopad(salt_b64)
        expected = _b64decode_nopad(dk_b64)

        dk = hashlib.pbkdf2_hmac(alg, password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def _b64decode_nopad(s: str) -> bytes:
    pad = "=" * ((4 - (len(s) % 4)) % 4)
    return base64.urlsafe_b64decode(s + pad)
