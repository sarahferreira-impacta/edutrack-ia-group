"""
Subject service module for EduTrack AI.
Provides CRUD operations for academic subjects (disciplinas),
supporting in-memory session state (Streamlit) and optional Xano REST API backend.
"""

from datetime import datetime
import os
from typing import Dict, List, Optional, Any

import requests
import streamlit as st

from services.auth_service import load_dotenv

load_dotenv()

DEFAULT_SAMPLE_SUBJECTS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Inteligência Artificial e Machine Learning",
        "code": "IA-401",
        "professor": "Dr. Roberto Silva",
        "semester": "2026.1",
        "color": "#4F46E5",  # Indigo
        "status": "active",
        "created_at": "2026-02-15T09:00:00"
    },
    {
        "id": 2,
        "name": "Engenharia de Software e DevOps",
        "code": "ES-302",
        "professor": "Profa. Mariana Costa",
        "semester": "2026.1",
        "color": "#059669",  # Emerald
        "status": "active",
        "created_at": "2026-02-16T10:30:00"
    },
    {
        "id": 3,
        "name": "Banco de Dados e Modelagem Avançada",
        "code": "BD-201",
        "professor": "Prof. Carlos Eduardo",
        "semester": "2025.2",
        "color": "#D97706",  # Amber
        "status": "completed",
        "created_at": "2025-08-10T14:00:00"
    }
]


def init_session_subjects() -> None:
    """Initializes subjects list in st.session_state if not already present."""
    if "subjects" not in st.session_state:
        # Clone sample data so mutations do not affect the constant
        st.session_state.subjects = [dict(s) for s in DEFAULT_SAMPLE_SUBJECTS]


def _get_next_id() -> int:
    """Generates the next unique integer ID for a subject."""
    subjects = st.session_state.get("subjects", [])
    if not subjects:
        return 1
    return max(s["id"] for s in subjects) + 1


def get_all_subjects() -> List[Dict[str, Any]]:
    """Returns all registered subjects."""
    init_session_subjects()
    return st.session_state.subjects


def get_active_subjects() -> List[Dict[str, Any]]:
    """Returns only subjects with active status."""
    init_session_subjects()
    return [s for s in st.session_state.subjects if s.get("status") == "active"]


def count_active_subjects() -> int:
    """Returns total count of active subjects."""
    return len(get_active_subjects())


def get_subject_by_id(subject_id: int) -> Optional[Dict[str, Any]]:
    """Returns a subject by its unique ID, or None if not found."""
    init_session_subjects()
    for s in st.session_state.subjects:
        if s["id"] == subject_id:
            return s
    return None


def create_subject(
    name: str,
    code: str = "",
    professor: str = "",
    semester: str = "",
    color: str = "#4F46E5",
    status: str = "active"
) -> Dict[str, Any]:
    """
    Creates a new subject and appends it to state.
    Raises ValueError if name is empty.
    """
    name = (name or "").strip()
    if not name:
        raise ValueError("O nome da disciplina é obrigatório.")

    init_session_subjects()
    new_id = _get_next_id()
    new_subject: Dict[str, Any] = {
        "id": new_id,
        "name": name,
        "code": (code or "").strip(),
        "professor": (professor or "").strip(),
        "semester": (semester or "").strip(),
        "color": color or "#4F46E5",
        "status": status if status in ["active", "completed", "archived"] else "active",
        "created_at": datetime.now().isoformat()
    }
    st.session_state.subjects.append(new_subject)
    return new_subject


def update_subject(
    subject_id: int,
    name: Optional[str] = None,
    code: Optional[str] = None,
    professor: Optional[str] = None,
    semester: Optional[str] = None,
    color: Optional[str] = None,
    status: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Updates an existing subject by ID.
    Raises ValueError if updating name to an empty string.
    """
    init_session_subjects()
    for s in st.session_state.subjects:
        if s["id"] == subject_id:
            if name is not None:
                cleaned_name = name.strip()
                if not cleaned_name:
                    raise ValueError("O nome da disciplina não pode ser vazio.")
                s["name"] = cleaned_name
            if code is not None:
                s["code"] = code.strip()
            if professor is not None:
                s["professor"] = professor.strip()
            if semester is not None:
                s["semester"] = semester.strip()
            if color is not None:
                s["color"] = color
            if status is not None and status in ["active", "completed", "archived"]:
                s["status"] = status
            return s
    return None


def delete_subject(subject_id: int) -> bool:
    """
    Deletes a subject by ID from state.
    Returns True if deleted, False if not found.
    """
    init_session_subjects()
    initial_len = len(st.session_state.subjects)
    st.session_state.subjects = [s for s in st.session_state.subjects if s["id"] != subject_id]
    return len(st.session_state.subjects) < initial_len


DEFAULT_XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:w0xiZjdk"
DEFAULT_SUBJECTS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects"


def _resolve_xano_url(path: str, explicit_url: Optional[str] = None) -> str:
    """Builds a full Xano URL from the configured base URL or the environment override."""
    if explicit_url:
        return explicit_url.rstrip("/")

    env_value = os.getenv("XANO_SUBJECTS_URL") or os.getenv("XANO_BASE_URL") or os.getenv("XANO_API_URL")
    base_url = env_value or DEFAULT_SUBJECTS_URL
    normalized_path = path.lstrip("/")
    if base_url.rstrip("/").endswith("/subjects") and normalized_path == "subjects":
        return base_url.rstrip("/")
    if base_url.rstrip("/").endswith("/subjects") and normalized_path:
        return f"{base_url.rstrip('/')}/{normalized_path}"
    return f"{base_url.rstrip('/')}/{normalized_path}"


XANO_SUBJECTS_URL = os.getenv("XANO_SUBJECTS_URL") or DEFAULT_SUBJECTS_URL


def _get_subjects_api_url(subject_id: Optional[int] = None) -> str:
    """Builds the current subjects endpoint URL using the configured Xano base URL."""
    base_url = os.getenv("XANO_SUBJECTS_URL") or DEFAULT_SUBJECTS_URL
    subjects_url = base_url.rstrip("/")
    if subject_id is None:
        return subjects_url
    return f"{subjects_url}/{subject_id}"


def _get_xano_auth_headers() -> Dict[str, str]:
    """Builds the Authorization header when a token is configured."""
    token = None
    if "auth_token" in st.session_state:
        token = st.session_state.get("auth_token")
    if not token:
        token = os.getenv("XANO_AUTH_TOKEN")
    if not token and hasattr(st, "secrets"):
        try:
            token = st.secrets.get("XANO_AUTH_TOKEN")
        except Exception:
            token = None
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def _normalize_subject_record(item: Dict[str, Any]) -> Dict[str, Any]:
    """Converts a raw Xano subject payload into the internal app format."""
    if not isinstance(item, dict):
        return {}

    subject_id = item.get("id")
    if subject_id is None:
        return {}

    teacher_name = (
        item.get("teacher")
        or item.get("professor")
        or item.get("professor_name")
        or item.get("responsible")
        or ""
    )
    hours_value = item.get("hours")
    if hours_value is None:
        for alt_key in ("total_hours", "credit_hours", "hour_count", "workload_hours"):
            if alt_key in item:
                hours_value = item.get(alt_key)
                break

    return {
        "id": subject_id,
        "name": (item.get("name") or item.get("title") or "Sem nome").strip() or "Sem nome",
        "code": item.get("code") or item.get("subject_code") or "",
        "teacher": teacher_name,
        "hours": hours_value if hours_value is not None else 0,
        "professor": teacher_name,
        "semester": item.get("semester") or item.get("period") or "",
        "color": item.get("color") or "#4F46E5",
        "status": item.get("status") or "active",
        "created_at": item.get("created_at") or datetime.now().isoformat(),
    }


def get_auth_token() -> Optional[str]:
    """Returns the current bearer token from Streamlit session or environment."""
    if "auth_token" in st.session_state:
        token = st.session_state.get("auth_token")
        if token:
            return str(token)
    token = os.getenv("XANO_AUTH_TOKEN")
    if token:
        return str(token)
    return None


def create_subject_in_xano(name: str, teacher: Optional[str] = None, hours: Optional[int] = None) -> Dict[str, Any]:
    """Creates a new subject through the authenticated Xano subjects endpoint."""
    token = get_auth_token()
    if not token:
        raise PermissionError("Você precisa estar logado para cadastrar disciplinas.")

    payload = {
        "name": (name or "").strip(),
        "teacher": (teacher or "").strip() or None,
        "hours": hours if hours is not None else None,
    }
    if not payload["name"]:
        raise ValueError("O nome da disciplina é obrigatório.")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(
        _get_subjects_api_url(),
        json=payload,
        headers=headers,
        timeout=20,
    )

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Não foi possível cadastrar a disciplina: {detail}")

    try:
        return response.json()
    except ValueError:
        return {"name": payload["name"], "teacher": payload["teacher"], "hours": payload["hours"]}


def update_subject_in_xano(subject_id: int, name: Optional[str] = None, teacher: Optional[str] = None, hours: Optional[int] = None) -> Dict[str, Any]:
    """Updates an existing subject through the Xano PATCH endpoint."""
    token = get_auth_token()
    if not token:
        raise PermissionError("Você precisa estar logado para atualizar disciplinas.")

    payload = {}
    if name is not None:
        payload["name"] = (name or "").strip()
    if teacher is not None:
        payload["teacher"] = (teacher or "").strip() or None
    if hours is not None:
        payload["hours"] = hours

    if not payload:
        return {"id": subject_id}

    if payload.get("name") == "":
        raise ValueError("O nome da disciplina não pode ser vazio.")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.patch(
        _get_subjects_api_url(subject_id),
        json=payload,
        headers=headers,
        timeout=15,
    )

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Não foi possível atualizar a disciplina: {detail}")

    try:
        return response.json()
    except ValueError:
        return {"id": subject_id, **payload}


def delete_subject_in_xano(subject_id: int) -> Dict[str, Any]:
    """Deletes a subject from Xano after validating ownership."""
    token = get_auth_token()
    if not token:
        raise PermissionError("Você precisa estar logado para excluir disciplinas.")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.delete(_get_subjects_api_url(subject_id), headers=headers, timeout=15)

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Não foi possível excluir a disciplina: {detail}")

    try:
        return response.json()
    except ValueError:
        return {"success": True, "deleted_id": subject_id}


def fetch_subjects_from_xano(url: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all subjects from the configured Xano endpoint."""
    target_url = url or os.getenv("XANO_SUBJECTS_URL") or _resolve_xano_url("subjects") or _get_subjects_api_url()
    headers = _get_xano_auth_headers()

    try:
        response = requests.get(target_url, headers=headers, timeout=15)
    except requests.RequestException:
        return []

    if not response.ok:
        return []

    try:
        payload = response.json()
    except ValueError:
        return []

    if isinstance(payload, dict):
        if isinstance(payload.get("data"), list):
            payload = payload["data"]
        elif isinstance(payload.get("result"), list):
            payload = payload["result"]
        else:
            payload = [payload]

    if not isinstance(payload, list):
        return []

    normalized: List[Dict[str, Any]] = []
    for item in payload:
        normalized_item = _normalize_subject_record(item)
        if normalized_item:
            normalized.append(normalized_item)
    return normalized
