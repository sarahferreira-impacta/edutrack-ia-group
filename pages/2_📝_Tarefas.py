from datetime import datetime

import streamlit as st

from services.subject_service import fetch_subjects_from_xano
from services.task_service import fetch_tasks_from_xano


def _format_due_date(value):
    if not value:
        return "Sem prazo"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return value


st.title("Minhas Tarefas")

col1, col2 = st.columns([3, 1])

with col1:
    search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas")

with col2:
    filtro = st.selectbox("Status", ["Todas", "Pendente", "Em andamento", "Concluída"])

st.markdown("---")

try:
    tasks = fetch_tasks_from_xano()
    subjects = fetch_subjects_from_xano()
except Exception:
    tasks = []
    subjects = []
    st.error("Não foi possível carregar as tarefas do Xano. Verifique a conexão ou a autenticação.")

subject_lookup = {
    str(subject.get("id")): subject.get("name") or "Disciplina"
    for subject in subjects
    if isinstance(subject, dict)
}

status_labels = {
    "pending": "Pendente",
    "in_progress": "Em andamento",
    "completed": "Concluída",
    "done": "Concluída",
}

filtered_tasks = tasks
if filtro != "Todas":
    normalized_filter = {
        "Pendente": "pending",
        "Em andamento": "in_progress",
        "Concluída": "completed",
    }.get(filtro, "")
    filtered_tasks = [
        task for task in filtered_tasks
        if str(task.get("status") or "pending").lower() == normalized_filter
    ]

if search:
    search_term = search.lower()
    filtered_tasks = [
        task for task in filtered_tasks
        if search_term in (task.get("title") or "").lower()
    ]

if not filtered_tasks:
    st.info("Nenhuma tarefa corresponde aos critérios atuais.")
else:
    for task in filtered_tasks:
        task_status = str(task.get("status") or "pending").lower()
        label = status_labels.get(task_status, "Pendente")
        with st.expander(
            f"📌 {task.get('title') or 'Tarefa sem título'}",
            expanded=True,
        ):
            st.write(f"**Disciplina:** {subject_lookup.get(str(task.get('subject_id')), 'Disciplina não vinculada')}")
            st.write(f"**Prazo:** {_format_due_date(task.get('due_date'))}")
            st.write(f"**Status:** {label}")
            if task.get("description"):
                st.write(f"**Descrição:** {task.get('description')}")
            st.checkbox("Marcar como Concluída", value=task_status in {"completed", "done"})