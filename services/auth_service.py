import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import streamlit as st


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


def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """Reads configuration from Streamlit secrets first, then environment, then .env fallback."""
    try:
        secrets = getattr(st, "secrets", None)
        if secrets is not None and hasattr(secrets, "get"):
            value = secrets.get(key)
            if value not in (None, ""):
                return str(value)
    except Exception:
        pass

    value = os.getenv(key)
    if value not in (None, ""):
        return value

    env_values = load_dotenv()
    value = env_values.get(key)
    if value not in (None, ""):
        return value

    return default


def get_xano_base_url() -> str:
    """Returns the configured Xano auth base URL from Streamlit secrets or the environment."""
    base_url = (
        get_config_value("XANO_AUTH_BASE_URL")
        or get_config_value("XANO_BASE_URL")
        or get_config_value("XANO_API_URL")
        or ""
    )
    return base_url.rstrip("/")


def build_xano_url(path: str) -> str:
    """Builds a full endpoint URL from the configured Xano base URL."""
    base_url = get_xano_base_url()
    if not base_url:
        raise ValueError("XANO_BASE_URL is not configured. Add it to Streamlit secrets or the project .env file.")
    normalized_path = path.lstrip("/")
    return f"{base_url}/{normalized_path}"


def _unpack_xano_payload(value: Any) -> Any:
    """Normalizes common Xano wrappers such as {data: ...} or {result: ...}."""
    if isinstance(value, dict):
        for key in ("data", "result", "user", "profile"):
            if key in value and isinstance(value[key], (dict, list)):
                return value[key]
    return value


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
        return _unpack_xano_payload(response.json())
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
    user = _request_json("GET", "auth/me", token=token)
    if isinstance(user, list):
        return user[0] if user else {}
    if isinstance(user, dict):
        return user
    return {}


def update_current_user_profile(name: Optional[str] = None, email: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
    """Attempts to update the authenticated user profile via the user endpoint when available."""
    token = token or get_config_value("XANO_AUTH_TOKEN") or (os.environ.get("auth_token") if "auth_token" in os.environ else None)
    if not token:
        raise ValueError("Token de autenticação ausente.")

    user = get_current_user(token)
    user_id = user.get("id")
    if user_id is None:
        raise ValueError("Não foi possível identificar o usuário autenticado.")

    payload: Dict[str, Any] = {}
    if name is not None:
        value = (name or "").strip()
        if not value:
            raise ValueError("O nome completo não pode ficar vazio.")
        payload["name"] = value
    if email is not None:
        value = (email or "").strip().lower()
        if not value or "@" not in value:
            raise ValueError("Informe um e-mail válido.")
        payload["email"] = value

    if not payload:
        return user

    urls = [
        build_xano_url(f"user/{user_id}"),
        build_xano_url("user"),
    ]
    last_error = None
    for url in urls:
        try:
            response = requests.patch(url, json=payload, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=20)
        except requests.RequestException as exc:
            last_error = exc
            continue

        if response.ok:
            try:
                return _unpack_xano_payload(response.json())
            except ValueError:
                return {"success": True, "id": user_id, **payload}

        last_error = response.text or f"Erro HTTP {response.status_code}"
        if response.status_code not in {404, 405}:
            break

    raise RuntimeError(
        "Não foi possível atualizar as informações do perfil no Xano. "
        "Verifique se a rota de edição do usuário está habilitada no Xano e se o token do usuário é válido. "
        f"Detalhes: {last_error}"
    )


def change_password(current_password: str, new_password: str, confirm_password: str, token: Optional[str] = None) -> Dict[str, Any]:
    """Changes the authenticated user's password using the Xano reset endpoint."""
    token = token or get_config_value("XANO_AUTH_TOKEN")
    if not token:
        raise ValueError("Token de autenticação ausente.")

    if not current_password or not new_password or not confirm_password:
        raise ValueError("Informe a senha atual, a nova senha e a confirmação.")
    if len(new_password) < 8:
        raise ValueError("A nova senha deve conter pelo menos 8 caracteres.")
    if new_password != confirm_password:
        raise ValueError("A nova senha e a confirmação não coincidem.")

    url = build_xano_url("reset/update_password")
    payload = {"password": new_password, "confirm_password": confirm_password}
    response = requests.post(url, json=payload, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=20)
    if not response.ok:
        detail = response.text or "Não foi possível alterar a senha."
        raise RuntimeError(f"Não foi possível alterar a senha: {detail}")

    try:
        return response.json()
    except ValueError:
        return {"success": True}
