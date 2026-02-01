from app.autenticacion.jwt_handler import crear_token


def login(username: str, password: str) -> str:
    # Demo: usuario fijo. Reemplazar por validación real + hashing.
    if username != "admin" or password != "admin":
        raise ValueError("Credenciales inválidas")

    return crear_token({"sub": username, "role": "admin"})
