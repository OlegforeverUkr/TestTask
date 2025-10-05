import re


def validate_password(password: str) -> bool:
    """Validate password."""
    if not 8 <= len(password) <= 72:
        raise ValueError("Password must be 8–72 characters long")

    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter (A–Z)")

    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter (a–z)")

    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number (0–9)")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\;/]", password):
        raise ValueError("Password must contain at least one special character")

    return True
