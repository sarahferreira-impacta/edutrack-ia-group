import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests


def load_dotenv() -> Dict[str, str]:
    """Loads environment variables from the project root .env file when present."""
    env_path = Path(__file__).resolve().parents[1] / ".env"
    values: Dict[str, str] = {}

    if not env_path.exists():
        return values

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value
        os.environ.setdefault(key, value)

    return values


def get_xano_base_url() -> str:
    """Returns the configured Xano base URL from env or .env file."""
    load_dotenv()
    base_url = os.getenv("XANO_BASE_URL") or os.getenv("XANO_API_URL") or ""
    return base_url.rstrip("/")


def build_xano_url(path: str) -> str:
    """Builds a full endpoint URL from the configured Xano base URL."""
    base_url = get_xano_base_url()
    if not base_url:
        raise ValueError("XANO_BASE_URL is not configured. Add it to the project .env file.")
    normalized_path = path.lstrip("/")
    return f"{base_url}/{normalized_path}"


def _request_json(method: str, path: str, payload: Optional[Dict[str, Any]] = None, token: Optional[str] = None):
    """Ensures consistent JSON requests to the Xano API."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = build_xano_url(path)
    method_name = method.upper()

    if method_name == "GET":
        response = requests.get(url, headers=headers, timeout=20)
    elif method_name == "POST":
        response = requests.post(url, json=payload, headers=headers, timeout=20)
    else:
        response = requests.request(method_name, url, json=payload, headers=headers, timeout=20)

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Xano request failed ({response.status_code}): {detail}")

    try:
        return response.json()
    except ValueError:
        return {}


def signup_user(name: str, email: str, password: str) -> Dict[str, Any]:
    """Registers a new user and returns the auth token payload from Xano."""
    payload = {
        "name": (name or "").strip(),
        "email": (email or "").strip().lower(),
        "password": password or "",
    }
    if not payload["name"] or not payload["email"] or not payload["password"]:
        raise ValueError("Nome, e-mail e senha são obrigatórios.")
    return _request_json("POST", "auth/signup", payload)


def login_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticates a user and returns the auth token payload from Xano."""
    payload = {
        "email": (email or "").strip().lower(),
        "password": password or "",
    }
    if not payload["email"] or not payload["password"]:
        raise ValueError("E-mail e senha são obrigatórios.")
    return _request_json("POST", "auth/login", payload)


def get_current_user(token: str) -> Dict[str, Any]:
    """Fetches the authenticated user profile using auth/me."""
    if not token:
        raise ValueError("Token de autenticação ausente.")
    return _request_json("GET", "auth/me", token=token)
