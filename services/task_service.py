import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

from services.auth_service import get_config_value

DEFAULT_XANO_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:w0xiZjdk"
DEFAULT_TASKS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks"


def _resolve_xano_url(path: str, explicit_url: Optional[str] = None) -> str:
    """Builds a full Xano URL from the configured base URL or the environment override."""
    if explicit_url:
        return explicit_url.rstrip("/")

    env_value = get_config_value("XANO_TASKS_URL") or get_config_value("XANO_BASE_URL") or get_config_value("XANO_API_URL")
    base_url = env_value or DEFAULT_TASKS_URL
    normalized_path = path.lstrip("/")
    if base_url.rstrip("/").endswith("/academic_tasks") and normalized_path == "academic_tasks":
        return base_url.rstrip("/")
    if base_url.rstrip("/").endswith("/academic_tasks") and normalized_path:
        return f"{base_url.rstrip('/')}/{normalized_path}"
    return f"{base_url.rstrip('/')}/{normalized_path}"


XANO_TASKS_URL = get_config_value("XANO_TASKS_URL") or DEFAULT_TASKS_URL


def _get_tasks_api_url(task_id: Optional[int] = None) -> str:
    """Builds the current academic_tasks endpoint URL using the configured Xano base URL."""
    base_url = get_config_value("XANO_TASKS_URL") or DEFAULT_TASKS_URL
    tasks_url = base_url.rstrip("/")
    if task_id is None:
        return tasks_url
    return f"{tasks_url}/{task_id}"


def _get_xano_auth_headers() -> Dict[str, str]:
    """Builds the Authorization header when a token is configured."""
    token = None
    if "auth_token" in st.session_state:
        token = st.session_state.get("auth_token")
    if not token:
        token = get_config_value("XANO_AUTH_TOKEN")
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
    """Returns the current bearer token from Streamlit session or configuration secrets."""
    if "auth_token" in st.session_state:
        token = st.session_state.get("auth_token")
        if token:
            return str(token)
    token = get_config_value("XANO_AUTH_TOKEN")
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
    target_url = _get_tasks_api_url()
    response = requests.post(
        target_url,
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


def _fetch_task_by_id(task_id: int) -> Dict[str, Any]:
    """Loads the full current task payload from Xano before performing a PATCH update."""
    token = get_auth_token()
    if not token:
        raise PermissionError("Você precisa estar logado para atualizar tarefas.")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(_get_tasks_api_url(task_id=task_id), headers=headers, timeout=15)

    if not response.ok:
        try:
            detail = response.json()
            if isinstance(detail, dict):
                error_msg = detail.get("message") or detail.get("error") or str(detail)
            else:
                error_msg = str(detail)
        except ValueError:
            error_msg = response.text or f"Erro {response.status_code}"
        raise RuntimeError(f"Não foi possível carregar a tarefa: {error_msg}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Resposta inválida ao carregar a tarefa para atualização.") from exc

    if isinstance(payload, dict):
        if payload.get("data") is not None and isinstance(payload.get("data"), dict):
            payload = payload["data"]
        elif payload.get("result") is not None and isinstance(payload.get("result"), dict):
            payload = payload["result"]
    elif isinstance(payload, list):
        if not payload:
            raise RuntimeError("Tarefa não encontrada no Xano.")
        payload = payload[0]

    if not isinstance(payload, dict):
        raise RuntimeError("Resposta inválida ao carregar a tarefa para atualização.")

    return payload


def update_task_in_xano(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    subject_id: Optional[int] = None,
    due_date: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Updates a full task payload in Xano through PATCH while preserving required fields."""
    token = get_auth_token()
    if not token:
        raise PermissionError("Você precisa estar logado para atualizar tarefas.")

    current_task = _fetch_task_by_id(task_id)
    payload = {
        "title": current_task.get("title") or current_task.get("name") or "Sem título",
        "description": current_task.get("description") or "",
        "due_date": current_task.get("due_date") or current_task.get("deadline") or None,
        "subject_id": current_task.get("subject_id"),
        "status": current_task.get("status") or "pending",
    }

    if title is not None:
        payload["title"] = (title or "").strip() or current_task.get("title") or "Sem título"
    if description is not None:
        payload["description"] = description or ""
    if subject_id is not None:
        payload["subject_id"] = subject_id
    if due_date is not None:
        # Se foi fornecida string vazia ou None, limpa a data
        payload["due_date"] = due_date if due_date else None
    if status is not None:
        payload["status"] = status

    if not payload["title"]:
        raise ValueError("O título da tarefa é obrigatório.")
    if payload["subject_id"] is None:
        raise RuntimeError("A tarefa não possui disciplina vinculada e não pode ser atualizada.")

    target_url = _get_tasks_api_url(task_id=task_id)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.patch(
        target_url,
        json=payload,
        headers=headers,
        timeout=15,
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
        raise RuntimeError(f"Não foi possível atualizar a tarefa: {error_msg}")

    try:
        return response.json()
    except ValueError:
        return {"id": task_id, "status": payload["status"]}


def update_task_status_in_xano(task_id: int, status: str) -> Dict[str, Any]:
    """Updates the status of an academic task in Xano via PATCH using the full required payload."""
    return update_task_in_xano(
        task_id=task_id,
        status=status,
    )


def delete_task_in_xano(task_id: int) -> Dict[str, Any]:
    """Deletes an academic task from Xano after validating ownership."""
    token = get_auth_token()
    if not token:
        raise PermissionError("Você precisa estar logado para excluir tarefas.")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    target_url = _get_tasks_api_url(task_id=task_id)
    response = requests.delete(target_url, headers=headers, timeout=15)

    if not response.ok:
        try:
            detail = response.json()
            if isinstance(detail, dict):
                error_msg = detail.get("message") or detail.get("error") or str(detail)
            else:
                error_msg = str(detail)
        except ValueError:
            error_msg = response.text or f"Erro {response.status_code}"
        raise RuntimeError(f"Não foi possível excluir a tarefa: {error_msg}")

    try:
        return response.json()
    except ValueError:
        return {"success": True, "deleted_id": task_id}


def fetch_tasks_from_xano(
    url: Optional[str] = None,
    subject_id: Optional[int] = None,
    user_subjects: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Fetches academic tasks from the configured Xano endpoint with fallback for subject_id requirements."""
    target_url = url or get_config_value("XANO_TASKS_URL") or _resolve_xano_url("academic_tasks")
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
