from datetime import datetime

import streamlit as st

from scripts.calculate_progress import calculate_progress_data
from services.subject_service import fetch_subjects_from_xano, get_auth_token
from services.task_service import (
    create_task_in_xano,
    fetch_tasks_from_xano,
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
    if isinstance(value, (int, float)):
        try:
            # Xano timestamp in milliseconds
            dt = datetime.fromtimestamp(value / 1000 if value > 10000000000 else value)
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return str(value)
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return str(value)


if not get_auth_token():
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login na página de perfil para continuar.")
    st.page_link("pages/3_👤_Perfil.py", label="Ir para Login")
    st.stop()

st.title("Minhas Tarefas")

if "task_success_message" in st.session_state:
    st.success(st.session_state.pop("task_success_message"))

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
        format_func=lambda s: {"pending": "Pendente", "in_progress": "Em andamento", "completed": "Concluída"}.get(s, s),
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
                with st.spinner("Salvando tarefa..."):
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
    with st.spinner("Carregando suas tarefas do Xano..."):
        tasks = fetch_tasks_from_xano(user_subjects=user_subjects)
    load_error = None
except Exception as exc:
    tasks = []
    load_error = exc

if load_error:
    st.error(f"Não foi possível carregar as tarefas do Xano: {load_error}")
    if st.button("Tentar novamente"):
        st.rerun()

# Seção de Progresso Acadêmico por Disciplina (sempre calculada com dados reloaded do banco)
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

if not load_error and not tasks:
    st.info("Você ainda não possui nenhuma tarefa cadastrada.")
elif not load_error and not filtered_tasks:
    st.info("Nenhuma tarefa encontrada com os filtros selecionados.")
elif filtered_tasks:
    for task in filtered_tasks:
        task_status = _normalize_status(task.get("status"))
        label = _status_label(task.get("status"))
        task_subject_id = task.get("subject_id")
        subject_name = (
            task.get("subject_name")
            or subject_lookup.get(task_subject_id)
            or (f"Disciplina #{task_subject_id}" if task_subject_id else "Disciplina não vinculada")
        )
        task_id = task.get("id") or task.get("title")
        with st.expander(
            f"📌 {task.get('title') or 'Tarefa sem título'}",
            expanded=True,
        ):
            st.write(f"**Disciplina:** {subject_name}")
            st.write(f"**Prazo:** {_format_due_date(task.get('due_date'))}")
            st.write(f"**Status:** {label}")
            if task.get("description"):
                st.write(f"**Descrição:** {task.get('description')}")

            is_completed = task_status in {"completed", "done"}
            checkbox_key = f"done_{task.get('id')}"
            checked = st.checkbox(
                "Marcar como Concluída",
                value=is_completed,
                key=checkbox_key,
            )

            # Só chamar o PATCH quando o usuário marcar o checkbox em uma tarefa que ainda NÃO está completed
            if checked and not is_completed and task.get("id"):
                try:
                    with st.spinner("Concluindo tarefa..."):
                        update_task_status_in_xano(task_id=int(task["id"]), status="completed")
                    st.session_state["task_success_message"] = "Tarefa marcada como concluída!"
                    st.rerun()
                except Exception as exc:
                    st.session_state[checkbox_key] = False
                    st.error(f"Não foi possível concluir a tarefa: {exc}")
