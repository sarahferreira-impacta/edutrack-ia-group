#!/usr/bin/env python3
"""
calculate_progress.py

Calculates academic progress percentage (completed / total) for a given subject
or all subjects based on academic tasks retrieved via CRUD endpoints, returning structured JSON.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import requests
from services.auth_service import load_dotenv

load_dotenv()

DEFAULT_SUBJECTS_URL = os.getenv("XANO_SUBJECTS_URL") or "https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects"
DEFAULT_TASKS_URL = os.getenv("XANO_TASKS_URL") or "https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks"


def _get_auth_headers(token: Optional[str] = None) -> Dict[str, str]:
    """Builds Authorization header using explicit token or environment variable."""
    auth_token = token or os.getenv("XANO_AUTH_TOKEN")
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    return headers


def fetch_subject_details(
    subject_id: int,
    subjects_url: Optional[str] = None,
    token: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Retrieves subject details from the CRUD endpoint or returns None if not found."""
    target_url = subjects_url or DEFAULT_SUBJECTS_URL
    headers = _get_auth_headers(token)

    try:
        # Try fetching specific subject endpoint: GET /subjects/{id}
        detail_url = f"{target_url.rstrip('/')}/{subject_id}"
        response = requests.get(detail_url, headers=headers, timeout=10)
        if response.ok:
            data = response.json()
            if isinstance(data, dict) and data.get("id") == subject_id:
                return data
    except requests.RequestException:
        pass

    try:
        # Fallback to list endpoint: GET /subjects
        response = requests.get(target_url, headers=headers, timeout=10)
        if response.ok:
            data = response.json()
            if isinstance(data, dict):
                data = data.get("data") or data.get("result") or [data]
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("id") == subject_id:
                        return item
    except requests.RequestException:
        pass

    return None


def fetch_subject_tasks(
    subject_id: int,
    tasks_url: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Retrieves tasks associated with the specified subject from the tasks CRUD endpoint."""
    target_url = tasks_url or DEFAULT_TASKS_URL
    headers = _get_auth_headers(token)
    params = {"subject_id": subject_id}

    try:
        response = requests.get(target_url, headers=headers, params=params, timeout=10)
        if response.ok:
            payload = response.json()
            if isinstance(payload, dict):
                payload = payload.get("data") or payload.get("result") or [payload]
            if isinstance(payload, list):
                # Filter specifically for subject_id
                return [
                    t for t in payload
                    if isinstance(t, dict) and str(t.get("subject_id")) == str(subject_id)
                ]
    except requests.RequestException:
        pass

    return []


def calculate_progress_data(
    subject_id: int,
    subject_name: Optional[str] = None,
    tasks: Optional[List[Dict[str, Any]]] = None,
    token: Optional[str] = None,
    subjects_url: Optional[str] = None,
    tasks_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Computes the progress data dictionary for a given subject.
    If tasks or subject_name are not passed, fetches them from the CRUD endpoints.
    """
    resolved_subject_name = subject_name
    if resolved_subject_name is None:
        subject_data = fetch_subject_details(subject_id, subjects_url=subjects_url, token=token)
        if subject_data:
            resolved_subject_name = subject_data.get("name") or subject_data.get("title") or f"Disciplina #{subject_id}"
        else:
            resolved_subject_name = f"Disciplina #{subject_id}"

    task_list = tasks
    if task_list is None:
        task_list = fetch_subject_tasks(subject_id, tasks_url=tasks_url, token=token)

    total_tasks = len(task_list)
    completed_tasks = sum(
        1 for t in task_list
        if str(t.get("status") or "").strip().lower() in {"completed", "done", "concluída", "concluida"}
    )

    if total_tasks > 0:
        progress_percentage = round((completed_tasks / total_tasks) * 100, 2)
    else:
        progress_percentage = 0.0

    return {
        "subject_id": subject_id,
        "subject_name": resolved_subject_name,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress_percentage": progress_percentage,
    }


def calculate_subject_progress(
    subject_id: int,
    subject_name: Optional[str] = None,
    tasks: Optional[List[Dict[str, Any]]] = None,
    token: Optional[str] = None,
    indent: Optional[int] = 2,
) -> str:
    """
    Calculates progress percentage for a subject and returns the result formatted as a JSON string.
    """
    data = calculate_progress_data(
        subject_id=subject_id,
        subject_name=subject_name,
        tasks=tasks,
        token=token,
    )
    return json.dumps(data, indent=indent, ensure_ascii=False)


def calculate_all_subjects_progress(
    token: Optional[str] = None,
    subjects_url: Optional[str] = None,
    tasks_url: Optional[str] = None,
    indent: Optional[int] = 2,
) -> str:
    """
    Calculates progress for all registered subjects and returns a JSON array.
    """
    headers = _get_auth_headers(token)
    target_url = subjects_url or DEFAULT_SUBJECTS_URL

    subjects: List[Dict[str, Any]] = []
    try:
        res = requests.get(target_url, headers=headers, timeout=10)
        if res.ok:
            data = res.json()
            if isinstance(data, dict):
                data = data.get("data") or data.get("result") or [data]
            if isinstance(data, list):
                subjects = [s for s in data if isinstance(s, dict) and s.get("id") is not None]
    except Exception:
        subjects = []

    results = []
    for s in subjects:
        sid = s["id"]
        sname = s.get("name") or s.get("title") or f"Disciplina #{sid}"
        data = calculate_progress_data(
            subject_id=sid,
            subject_name=sname,
            token=token,
            subjects_url=subjects_url,
            tasks_url=tasks_url,
        )
        results.append(data)

    return json.dumps(results, indent=indent, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calcula a porcentagem de progresso (concluídas / total) de disciplinas e retorna JSON."
    )
    parser.add_argument(
        "subject_id",
        type=int,
        nargs="?",
        default=None,
        help="ID da disciplina para cálculo do progresso (opcional). Se omitido, calcula para todas as disciplinas.",
    )
    parser.add_argument("--token", type=str, default=None, help="Token Bearer de autenticação para as chamadas à API")
    parser.add_argument("--compact", action="store_true", help="Retorna o JSON em linha única sem identação")

    args = parser.parse_args()

    indent = None if args.compact else 2
    if args.subject_id is not None:
        result_json = calculate_subject_progress(subject_id=args.subject_id, token=args.token, indent=indent)
    else:
        result_json = calculate_all_subjects_progress(token=args.token, indent=indent)

    print(result_json)


if __name__ == "__main__":
    main()
