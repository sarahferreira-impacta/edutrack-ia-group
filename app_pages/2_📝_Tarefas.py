import streamlit as st

from app_pages.task_helpers import format_due_date, normalize_status, parse_xano_date, status_label
from scripts.calculate_progress import calculate_progress_data
from services.subject_service import fetch_subjects_from_xano, get_auth_token
from services.task_service import (
    create_task_in_xano,
    delete_task_in_xano,
    fetch_tasks_from_xano,
    update_task_in_xano,
    update_task_status_in_xano,
)

STATUS_OPTIONS = ["Todos", "Pendente", "Em andamento", "Concluída"]
STATUS_MAP = {
    "Todos": "all",
    "Pendente": "pending",
    "Em andamento": "in_progress",
    "Concluída": "completed",
}


def _normalize_status(value):
    return normalize_status(value)


def _status_label(value):
    return status_label(value)


def _format_due_date(value):
    return format_due_date(value)


if not get_auth_token():
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login na página de perfil para continuar.")
    st.stop()

st.title("📝 Minhas Tarefas")

if "task_success_message" in st.session_state:
    st.success(st.session_state.pop("task_success_message"))
if "task_error_message" in st.session_state:
    st.error(st.session_state.pop("task_error_message"))


def _handle_task_checkbox(task_id: int) -> None:
    checkbox_key = f"done_{task_id}"
    desired_state = bool(st.session_state.get(checkbox_key))
    target_status = "completed" if desired_state else "pending"
    try:
        update_task_status_in_xano(task_id=int(task_id), status=target_status)
        st.session_state["task_success_message"] = (
            "Tarefa marcada como concluída!" if desired_state else "Tarefa reaberta e progresso recalculado."
        )
        st.rerun()
    except Exception as exc:
        st.session_state["task_error_message"] = f"Não foi possível atualizar a tarefa: {exc}"
        st.rerun()


try:
    user_subjects = fetch_subjects_from_xano()
except Exception:
    user_subjects = []

subject_options = {
    s["id"]: s.get("name") or f"Disciplina #{s['id']}"
    for s in user_subjects
    if isinstance(s, dict) and s.get("id")
}

with st.form("form_new_task", clear_on_submit=True):
    title = st.text_input("Título da tarefa", key="task_title")
    description = st.text_area("Descrição", key="task_description")
    if subject_options:
        selected_subject_id = st.selectbox(
            "Disciplina",
            options=list(subject_options.keys()),
            format_func=lambda sid: subject_options.get(sid, f"Disciplina #{sid}"),
            key="task_subject_select",
        )
    else:
        st.warning("Você ainda não possui disciplinas cadastradas. Cadastre uma disciplina primeiro para poder vinculá-la à tarefa.")
        selected_subject_id = None
    due_date = st.date_input("Prazo", key="task_due_date")
    status = st.selectbox(
        "Status",
        ["pending", "in_progress", "completed"],
        format_func=lambda item: {"pending": "Pendente", "in_progress": "Em andamento", "completed": "Concluída"}.get(item, item),
        key="task_status",
    )
    submitted = st.form_submit_button("Salvar tarefa", use_container_width=True)

    if submitted:
        if not selected_subject_id:
            st.error("Selecione uma disciplina cadastrada para vincular a tarefa.")
        elif not (title or "").strip():
            st.error("O título da tarefa é obrigatório.")
        else:
            try:
                create_task_in_xano(
                    title=title,
                    subject_id=int(selected_subject_id),
                    description=description,
                    due_date=due_date.isoformat() if due_date else None,
                    status=status,
                )
                st.session_state["task_success_message"] = "Tarefa cadastrada com sucesso!"
                st.rerun()
            except Exception as exc:
                st.error(f"Não foi possível cadastrar a tarefa: {exc}")

st.markdown("---")

try:
    tasks = fetch_tasks_from_xano(user_subjects=user_subjects)
    load_error = None
except Exception as exc:
    tasks = []
    load_error = exc

if load_error:
    st.error(f"Não foi possível carregar as tarefas do Xano: {load_error}")
    if st.button("Tentar novamente"):
        st.rerun()

if user_subjects and not load_error:
    with st.expander("📊 Progresso Acadêmico por Disciplina", expanded=True):
        cols_count = min(max(len(user_subjects), 1), 3)
        prog_cols = st.columns(cols_count)
        for idx, s in enumerate(user_subjects):
            sid = s.get("id")
            sname = s.get("name") or f"Disciplina #{sid}"
            sub_tasks = [t for t in tasks if str(t.get("subject_id")) == str(sid)]
            prog_data = calculate_progress_data(subject_id=sid, subject_name=sname, tasks=sub_tasks)
            pct = prog_data["progress_percentage"]
            total = prog_data["total_tasks"]
            done = prog_data["completed_tasks"]
            col_target = prog_cols[idx % cols_count]
            with col_target:
                st.markdown(f"**{sname}**")
                st.progress(min(max(pct / 100.0, 0.0), 1.0))
                st.caption(f"{done} de {total} tarefas concluídas ({pct}%)")

col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("Buscar tarefa...", placeholder="Ex: Estudar Pandas", key="task_search")
with col2:
    filtro = st.selectbox("Status", STATUS_OPTIONS, index=0, key="task_filter")

subject_lookup = {
    s["id"]: s.get("name") or "Disciplina"
    for s in user_subjects
    if isinstance(s, dict) and s.get("id")
}

filtered_tasks = tasks
selected_status = STATUS_MAP.get(filtro, "all")
if selected_status != "all":
    filtered_tasks = [task for task in filtered_tasks if _normalize_status(task.get("status")) == selected_status]
if search:
    term = search.lower()
    filtered_tasks = [task for task in filtered_tasks if term in (task.get("title") or "").lower()]

if not load_error and not tasks:
    st.info("Você ainda não possui nenhuma tarefa cadastrada.")
elif not load_error and not filtered_tasks:
    st.info("Nenhuma tarefa encontrada com os filtros selecionados.")
elif filtered_tasks:
    for task in filtered_tasks:
        task_id = task.get("id")
        if task_id is None:
            continue
        task_subject_id = task.get("subject_id")
        subject_name = task.get("subject_name") or subject_lookup.get(task_subject_id) or f"Disciplina #{task_subject_id}"
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{task.get('title') or 'Tarefa sem título'}**")
                st.caption(f"Disciplina: {subject_name}")
                st.caption(f"Prazo: {_format_due_date(task.get('due_date'))}")
                st.caption(f"Status: {_status_label(task.get('status'))}")
                if task.get("description"):
                    st.write(task["description"])
            with c2:
                with st.popover("✏️ Editar", use_container_width=True):
                    with st.form(f"edit_task_form_{task_id}"):
                        edited_title = st.text_input("Título", value=task.get("title") or "", key=f"task_title_edit_{task_id}")
                        edited_description = st.text_area("Descrição", value=task.get("description") or "", key=f"task_description_edit_{task_id}")
                        edited_subject_id = st.selectbox(
                            "Disciplina",
                            options=[subject.get("id") for subject in user_subjects if isinstance(subject, dict) and subject.get("id") is not None],
                            index=next((idx for idx, subject in enumerate(user_subjects) if str(subject.get("id")) == str(task_subject_id)), 0),
                            format_func=lambda sid: next((subject.get("name") or f"Disciplina #{sid}" for subject in user_subjects if str(subject.get("id")) == str(sid)), f"Disciplina #{sid}"),
                            key=f"task_subject_edit_{task_id}",
                        )
                        safe_due_date = parse_xano_date(task.get("due_date"))
                        edited_due_date = st.date_input("Prazo", value=safe_due_date, key=f"task_due_edit_{task_id}")
                        edited_status = st.selectbox(
                            "Status",
                            ["pending", "in_progress", "completed"],
                            index=["pending", "in_progress", "completed"].index(_normalize_status(task.get("status"))),
                            format_func=lambda item: {"pending": "Pendente", "in_progress": "Em andamento", "completed": "Concluída"}.get(item, item),
                            key=f"task_status_edit_{task_id}",
                        )
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            submitted = st.form_submit_button("Salvar alterações", type="primary")
                        with col_cancel:
                            cancel_clicked = st.form_submit_button("Cancelar", type="secondary")
                        if cancel_clicked:
                            st.rerun()
                        if submitted:
                            try:
                                update_task_in_xano(
                                    task_id=int(task_id),
                                    title=edited_title,
                                    description=edited_description,
                                    subject_id=int(edited_subject_id),
                                    due_date=edited_due_date.isoformat() if edited_due_date else None,
                                    status=edited_status,
                                )
                                st.success("Tarefa atualizada com sucesso!")
                                st.rerun()
                            except Exception as exc:
                                st.error(f"Não foi possível atualizar a tarefa: {exc}")
                with st.popover("🗑️ Excluir", use_container_width=True):
                    st.warning(f"Deseja excluir a tarefa '{task.get('title') or 'Sem título'}'?")
                    if st.button("Confirmar exclusão", key=f"delete_task_confirm_{task_id}", type="secondary"):
                        try:
                            delete_task_in_xano(int(task_id))
                            st.success("Tarefa excluída com sucesso!")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Não foi possível excluir a tarefa: {exc}")
                checkbox_value = st.checkbox("Marcar como concluída", value=_normalize_status(task.get("status")) == "completed", key=f"done_{task_id}")
                if checkbox_value != (_normalize_status(task.get("status")) == "completed"):
                    try:
                        update_task_status_in_xano(task_id=int(task_id), status="completed" if checkbox_value else "pending")
                        st.success("Status da tarefa atualizado com sucesso!")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Não foi possível atualizar a tarefa: {exc}")

