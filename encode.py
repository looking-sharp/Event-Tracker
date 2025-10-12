import base64

def encode(_id: str) -> str:
    return base64.urlsafe_b64encode(_id.encode()).decode().rstrip("=")

def decode(encoded: str) -> str:
    padded = encoded + "=" * (-len(encoded) % 4)
    return base64.urlsafe_b64decode(padded).decode()
