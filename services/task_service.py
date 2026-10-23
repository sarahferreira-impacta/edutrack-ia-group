import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

XANO_TASKS_URL = "https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks"


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

    return {
        "id": task_id,
        "title": (item.get("title") or item.get("name") or "Sem título").strip() or "Sem título",
        "description": item.get("description") or "",
        "due_date": item.get("due_date") or item.get("deadline") or "",
        "status": normalized_status,
        "subject_id": item.get("subject_id"),
        "user_id": item.get("user_id"),
        "created_at": item.get("created_at") or datetime.now().isoformat(),
    }


def fetch_tasks_from_xano(url: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all academic tasks from the configured Xano endpoint."""
    target_url = url or os.getenv("XANO_TASKS_URL", XANO_TASKS_URL)
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
        task = _normalize_task_record(item)
        if task:
            normalized.append(task)
    return normalized
