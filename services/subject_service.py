"""
Subject service module for EduTrack AI.
Provides CRUD operations for academic subjects (disciplinas),
supporting in-memory session state (Streamlit) and optional Xano REST API backend.
"""

from datetime import datetime
import os
import streamlit as st
from typing import Dict, List, Optional, Any

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
