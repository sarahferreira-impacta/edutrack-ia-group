from datetime import datetime

import streamlit as st

from services.subject_service import fetch_subjects_from_xano, get_auth_token
from services.task_service import create_task_in_xano, fetch_tasks_from_xano


STATUS_OPTIONS = ["Todos", "Pendente", "Em andamento", "Concluída"]
STATUS_MAP = {
    "Todos": "all",
    "Pendente": "pending",
    "Em andamento": "in_progress",
    "Concluída": "completed",
}


def _normalize_status(value):
    text = str(value or "").strip().lower()
    if text in {"done", "completed"}:
        return "completed"
    if text in {"in_progress", "in-progress", "em andamento"}:
        return "in_progress"
    return "pending" if text else "pending"


def _status_label(value):
    return {
        "pending": "Pendente",
        "in_progress": "Em andamento",
        "completed": "Concluída",
        "done": "Concluída",
    }.get(_normalize_status(value), "Pendente")


def _format_due_date(value):
    if not value:
        return "Sem prazo"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return value


if not get_auth_token():
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login na página de perfil para continuar.")
    st.page_link("pages/3_👤_Perfil.py", label="Ir para Login")
    st.stop()

st.title("Minhas Tarefas")

with st.form("form_new_task", clear_on_submit=True):
    title = st.text_input("Título da tarefa", key="task_title")
    description = st.text_area("Descrição", key="task_description")
    subject_id = st.number_input("ID da disciplina", min_value=1, step=1, key="task_subject_id")
    due_date = st.date_input("Prazo", key="task_due_date")
    status = st.selectbox("Status", ["pending", "in_progress", "completed"], key="task_status")
    submitted = st.form_submit_button("Salvar tarefa", use_container_width=True)
    if submitted:
        try:
            with st.spinner("Salvando tarefa..."):
                created = create_task_in_xano(
                    title=title,
                    subject_id=int(subject_id),
                    description=description,
                    due_date=due_date.isoformat(),
                    status=status,
                )
            st.success(f"Tarefa {created.get('title') or title} cadastrada com sucesso!")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))

col1, col2 = st.columns([3, 1])

with col1:
    search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas", key="task_search")

with col2:
    filtro = st.selectbox("Status", STATUS_OPTIONS, index=0, key="task_filter")

st.markdown("---")

try:
    with st.spinner("Carregando suas tarefas do Xano..."):
        tasks = fetch_tasks_from_xano()
        subjects = fetch_subjects_from_xano()
    load_error = None
except Exception as exc:
    tasks = []
    subjects = []
    load_error = exc

if load_error:
    st.error(f"Não foi possível carregar as tarefas do Xano. Verifique a conexão ou a autenticação. Detalhe: {load_error}")
    if st.button("Tentar novamente"):
        st.rerun()

subject_lookup = {
    str(subject.get("id")): subject.get("name") or "Disciplina"
    for subject in subjects
    if isinstance(subject, dict)
}

filtered_tasks = tasks
selected_status = STATUS_MAP.get(filtro, "all")
if selected_status != "all":
    filtered_tasks = [
        task for task in filtered_tasks
        if _normalize_status(task.get("status")) == selected_status
    ]

if search:
    search_term = search.lower()
    filtered_tasks = [
        task for task in filtered_tasks
        if search_term in (task.get("title") or "").lower()
    ]

if not load_error and not filtered_tasks:
    st.info("Você ainda não possui nenhuma tarefa cadastrada. Clique no botão + para adicionar.")
elif filtered_tasks:
    for task in filtered_tasks:
        task_status = _normalize_status(task.get("status"))
        label = _status_label(task.get("status"))
        subject_name = subject_lookup.get(str(task.get("subject_id")), "Disciplina não vinculada")
        with st.expander(
            f"📌 {task.get('title') or 'Tarefa sem título'}",
            expanded=True,
        ):
            st.write(f"**Disciplina:** {subject_name}")
            st.write(f"**Prazo:** {_format_due_date(task.get('due_date'))}")
            st.write(f"**Status:** {label}")
            if task.get("description"):
                st.write(f"**Descrição:** {task.get('description')}")
            st.checkbox("Marcar como Concluída", value=task_status in {"completed", "done"})