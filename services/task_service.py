import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

from services.auth_service import load_dotenv

load_dotenv()

DEFAULT_XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:w0xiZjdk"


def _resolve_xano_url(path: str, explicit_url: Optional[str] = None) -> str:
    """Builds a full Xano URL from the configured base URL or the environment override."""
    if explicit_url:
        return explicit_url.rstrip("/")

    base_url = os.getenv("XANO_BASE_URL") or os.getenv("XANO_API_URL") or DEFAULT_XANO_BASE_URL
    normalized_path = path.lstrip("/")
    return f"{base_url.rstrip('/')}/{normalized_path}"


XANO_TASKS_URL = _resolve_xano_url("academic_tasks")


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


def _normalize_task_record(item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes a raw Xano task payload into a stable app format."""
    if not isinstance(item, dict):
        return {}

    task_id = item.get("id")
    if task_id is None:
        return {}

    normalized_status = item.get("status") or "pending"
    if normalized_status == "in_progress":
        normalized_status = "in_progress"
    elif normalized_status == "done":
        normalized_status = "completed"

    subject_name = item.get("subject_name")
    if not subject_name and isinstance(item.get("_subjects"), dict):
        subject_name = item.get("_subjects", {}).get("name")

    return {
        "id": task_id,
        "title": (item.get("title") or item.get("name") or "Sem título").strip() or "Sem título",
        "description": item.get("description") or "",
        "due_date": item.get("due_date") or item.get("deadline") or "",
        "status": normalized_status,
        "subject_id": item.get("subject_id"),
        "subject_name": subject_name,
        "user_id": item.get("user_id"),
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


def create_task_in_xano(
    title: str,
    subject_id: Optional[int] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    status: str = "pending",
) -> Dict[str, Any]:
    """Creates a new academic task through the authenticated Xano tasks endpoint."""
    token = get_auth_token()
    if not token:
        raise PermissionError("Você precisa estar logado para cadastrar tarefas.")

    payload = {
        "title": (title or "").strip(),
        "description": (description or "").strip() or None,
        "due_date": due_date,
        "status": status or "pending",
        "subject_id": subject_id,
    }

    if not payload["title"]:
        raise ValueError("O título da tarefa é obrigatório.")

    if not payload["subject_id"]:
        raise ValueError("A disciplina da tarefa é obrigatória.")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(
        "https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks",
        json=payload,
        headers=headers,
        timeout=20,
    )

    if not response.ok:
        try:
            detail = response.json()
            if isinstance(detail, dict):
                error_msg = detail.get("message") or detail.get("error") or str(detail)
            else:
                error_msg = str(detail)
        except ValueError:
            error_msg = response.text or f"Erro {response.status_code}"
        raise RuntimeError(f"{error_msg}")

    try:
        return response.json()
    except ValueError:
        return {"title": payload["title"], "status": payload["status"], "subject_id": payload["subject_id"]}


def fetch_tasks_from_xano(
    url: Optional[str] = None,
    subject_id: Optional[int] = None,
    user_subjects: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Fetches academic tasks from the configured Xano endpoint with fallback for subject_id requirements."""
    target_url = url or os.getenv("XANO_TASKS_URL") or _resolve_xano_url("academic_tasks")
    headers = _get_xano_auth_headers()
    params = {"subject_id": subject_id} if subject_id is not None else None

    try:
        response = requests.get(target_url, headers=headers, params=params, timeout=15)
    except requests.RequestException as exc:
        raise RuntimeError(f"Erro de conexão com o servidor Xano: {exc}")

    if not response.ok:
        msg = ""
        is_missing_subject = False
        try:
            detail = response.json()
            if isinstance(detail, dict):
                msg = detail.get("message") or str(detail)
            else:
                msg = str(detail)
            if "subject_id" in msg or "Missing param" in msg:
                is_missing_subject = True
        except ValueError:
            msg = response.text or f"Código de status {response.status_code}"
            if "subject_id" in msg:
                is_missing_subject = True

        # Fallback resiliente: se o endpoint no servidor Xano exigir subject_id
        if response.status_code == 400 and is_missing_subject and subject_id is None:
            subjects_list = user_subjects
            if subjects_list is None:
                from services.subject_service import fetch_subjects_from_xano
                subjects_list = fetch_subjects_from_xano()

            if not subjects_list:
                return []

            all_tasks: List[Dict[str, Any]] = []
            seen_ids = set()
            for s in subjects_list:
                sid = s.get("id")
                if sid is None:
                    continue
                try:
                    sub_res = requests.get(target_url, headers=headers, params={"subject_id": sid}, timeout=15)
                    if sub_res.ok:
                        sub_payload = sub_res.json()
                        if isinstance(sub_payload, dict):
                            sub_payload = sub_payload.get("data") or sub_payload.get("result") or [sub_payload]
                        if isinstance(sub_payload, list):
                            for item in sub_payload:
                                norm = _normalize_task_record(item)
                                if norm and norm.get("id") not in seen_ids:
                                    seen_ids.add(norm.get("id"))
                                    all_tasks.append(norm)
                except Exception:
                    continue
            return all_tasks

        raise RuntimeError(f"Erro ao buscar tarefas (HTTP {response.status_code}): {msg}")

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
        task = _normalize_task_record(item)
        if task:
            normalized.append(task)
    return normalized
