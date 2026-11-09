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
from styles.theme import inject_css

inject_css()

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border: 1px solid #D0DCE8 !important;
        background: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(12, 30, 51, 0.06) !important;
        margin-bottom: 1.25rem !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 12px rgba(12, 30, 51, 0.1) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 1.25rem !important;
        gap: 0.75rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
        height: 2.3rem !important;
        padding: 0 0.75rem !important;
        font-size: 0.85rem !important;
        border-radius: 8px !important;
        border: 1px solid #D0DCE8 !important;
        background: #FFFFFF !important;
        color: #0C1E33 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
        background: #DFE7EE !important;
        border-color: #0C1E33 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stCheckbox"] {
        margin-top: 0.25rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

STATUS_OPTIONS = ["Todos", "Pendente", "Em andamento", "Concluída"]
STATUS_MAP = {
    "Todos": "all",
    "Pendente": "pending",
    "Em andamento": "in_progress",
    "Concluída": "completed",
}

STATUS_COLORS = {
    "completed":   {"border": "#CCEFBF", "badge_bg": "#CCEFBF", "badge_fg": "#2D6A1F", "label": "Concluída"},
    "in_progress": {"border": "#E1D2FF", "badge_bg": "#E1D2FF", "badge_fg": "#4B2D9A", "label": "Em andamento"},
    "pending":     {"border": "#FDE1AC", "badge_bg": "#FDE1AC", "badge_fg": "#7A5000", "label": "Pendente"},
}


def _normalize_status(value):
    return normalize_status(value)


def _format_due_date(value):
    return format_due_date(value)


if not get_auth_token():
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login na página de perfil para continuar.")
    st.stop()

st.markdown(
    "<h1 style='color:#0C1E33;font-size:1.75rem;font-weight:800;margin-bottom:0.25rem;'>"
    "📝 Minhas Tarefas</h1>",
    unsafe_allow_html=True,
)

if "task_success_message" in st.session_state:
    st.success(st.session_state.pop("task_success_message"))
if "task_error_message" in st.session_state:
    st.error(st.session_state.pop("task_error_message"))


def _handle_task_checkbox(task_id: int) -> None:
    desired = bool(st.session_state.get(f"done_{task_id}"))
    target  = "completed" if desired else "pending"
    try:
        update_task_status_in_xano(task_id=int(task_id), status=target)
        st.session_state["task_success_message"] = (
            "Tarefa marcada como concluída!" if desired else "Tarefa reaberta e progresso recalculado."
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
    title_input   = st.text_input("Título da tarefa", key="task_title")
    desc_input    = st.text_area("Descrição", key="task_description")
    if subject_options:
        sel_subject_id = st.selectbox(
            "Disciplina",
            options=list(subject_options.keys()),
            format_func=lambda sid: subject_options.get(sid, f"Disciplina #{sid}"),
            key="task_subject_select",
        )
    else:
        st.warning(
            "Você ainda não possui disciplinas cadastradas. "
            "Cadastre uma disciplina primeiro para poder vinculá-la à tarefa."
        )
        sel_subject_id = None
    due_date_input = st.date_input("Prazo", key="task_due_date")
    status_input   = st.selectbox(
        "Status",
        ["pending", "in_progress", "completed"],
        format_func=lambda i: {"pending": "Pendente", "in_progress": "Em andamento", "completed": "Concluída"}.get(i, i),
        key="task_status",
    )
    new_task_submitted = st.form_submit_button("Salvar tarefa", use_container_width=True)

    if new_task_submitted:
        if not sel_subject_id:
            st.error("Selecione uma disciplina cadastrada para vincular a tarefa.")
        elif not (title_input or "").strip():
            st.error("O título da tarefa é obrigatório.")
        else:
            try:
                create_task_in_xano(
                    title=title_input,
                    subject_id=int(sel_subject_id),
                    description=desc_input,
                    due_date=due_date_input.isoformat() if due_date_input else None,
                    status=status_input,
                )
                st.session_state["task_success_message"] = "Tarefa cadastrada com sucesso!"
                st.rerun()
            except Exception as exc:
                st.error(f"Não foi possível cadastrar a tarefa: {exc}")

st.markdown("---")

try:
    tasks      = fetch_tasks_from_xano(user_subjects=user_subjects)
    load_error = None
except Exception as exc:
    tasks      = []
    load_error = exc

if load_error:
    st.error(f"Não foi possível carregar as tarefas do Xano: {load_error}")
    if st.button("Tentar novamente"):
        st.rerun()

if user_subjects and not load_error:
    with st.expander("📊 Progresso Acadêmico por Disciplina", expanded=True):
        cols_count = min(max(len(user_subjects), 1), 3)
        prog_cols  = st.columns(cols_count)
        for idx, s in enumerate(user_subjects):
            sid   = s.get("id")
            sname = s.get("name") or f"Disciplina #{sid}"
            sub_tasks = [t for t in tasks if str(t.get("subject_id")) == str(sid)]
            prog_data = calculate_progress_data(subject_id=sid, subject_name=sname, tasks=sub_tasks)
            with prog_cols[idx % cols_count]:
                st.markdown(f"**{sname}**")
                st.progress(min(max(prog_data["progress_percentage"] / 100.0, 0.0), 1.0))
                st.caption(
                    f"{prog_data['completed_tasks']} de {prog_data['total_tasks']} "
                    f"tarefas concluídas ({prog_data['progress_percentage']}%)"
                )

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

filtered_tasks = list(tasks)
sel_status = STATUS_MAP.get(filtro, "all")
if sel_status != "all":
    filtered_tasks = [t for t in filtered_tasks if _normalize_status(t.get("status")) == sel_status]
if search:
    term = search.lower()
    filtered_tasks = [t for t in filtered_tasks if term in (t.get("title") or "").lower()]

if not load_error and not tasks:
    st.info("Você ainda não possui nenhuma tarefa cadastrada.")
elif not load_error and not filtered_tasks:
    st.info("Nenhuma tarefa encontrada com os filtros selecionados.")
elif filtered_tasks:
    TASK_COLS = 2
    rows = [filtered_tasks[i:i + TASK_COLS] for i in range(0, len(filtered_tasks), TASK_COLS)]

    for row in rows:
        grid_cols = st.columns(TASK_COLS)

        for col_idx, task in enumerate(row):
            task_id = task.get("id")
            if task_id is None:
                continue

            task_subject_id = task.get("subject_id")
            subject_name    = (
                task.get("subject_name")
                or subject_lookup.get(task_subject_id)
                or f"Disciplina #{task_subject_id}"
            )
            norm_status = _normalize_status(task.get("status"))
            sc = STATUS_COLORS.get(
                norm_status,
                {"border": "#D0DCE8", "badge_bg": "#DFE7EE", "badge_fg": "#0C1E33", "label": norm_status},
            )

            edit_key = f"show_edit_{task_id}"
            del_key  = f"show_del_{task_id}"
            if edit_key not in st.session_state:
                st.session_state[edit_key] = False
            if del_key not in st.session_state:
                st.session_state[del_key] = False

            desc_html = (
                f"<p style='margin:8px 0 0 0;color:#5A7084;font-size:0.84rem;"
                f"line-height:1.4;'>{task.get('description', '')}</p>"
                if task.get("description") else ""
            )

            with grid_cols[col_idx]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div style="
                            border-left: 4px solid {sc['border']};
                            padding-left: 10px;
                            margin-bottom: 8px;
                        ">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:6px;">
                                <span style="color:#0C1E33;font-weight:700;font-size:1.02rem;line-height:1.35;flex:1;">
                                    {task.get('title') or 'Tarefa sem título'}
                                </span>
                                <span style="
                                    display:inline-block;padding:3px 12px;
                                    border-radius:999px;font-size:0.75rem;font-weight:700;
                                    white-space:nowrap;
                                    background:{sc['badge_bg']};color:{sc['badge_fg']};
                                ">{sc['label']}</span>
                            </div>
                            <p style="color:#5A7084;font-size:0.84rem;margin:3px 0;">
                                📚 Disciplina: <strong style="color:#0C1E33;">{subject_name}</strong>
                            </p>
                            <p style="color:#5A7084;font-size:0.84rem;margin:3px 0;">
                                📅 Prazo: {_format_due_date(task.get('due_date'))}
                            </p>
                            {desc_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("<hr style='margin: 0.5rem 0 0.5rem 0; border: none; border-top: 1px solid #E8EFF5;'/>", unsafe_allow_html=True)

                    a1, a2, a3 = st.columns([1.6, 1, 1], vertical_alignment="center")
                    with a1:
                        is_completed = norm_status == "completed"
                        st.checkbox(
                            "Marcar como concluída",
                            value=is_completed,
                            key=f"done_{task_id}",
                            on_change=_handle_task_checkbox,
                            args=(task_id,),
                        )
                    with a2:
                        if st.button("✏️ Editar", key=f"btn_edit_{task_id}", use_container_width=True):
                            st.session_state[edit_key] = not st.session_state[edit_key]
                            st.session_state[del_key]  = False
                            st.rerun()
                    with a3:
                        if st.button("🗑️ Excluir", key=f"btn_del_{task_id}", use_container_width=True):
                            st.session_state[del_key]  = not st.session_state[del_key]
                            st.session_state[edit_key] = False
                            st.rerun()

                    if st.session_state.get(edit_key):
                        st.markdown("<hr style='margin: 0.5rem 0; border: none; border-top: 1px dashed #D0DCE8;'/>", unsafe_allow_html=True)
                        with st.form(f"edit_task_form_{task_id}"):
                            st.markdown(
                                "<p style='color:#0C1E33;font-weight:700;margin-bottom:4px;'>"
                                "✏️ Editar Tarefa</p>",
                                unsafe_allow_html=True,
                            )
                            edited_title = st.text_input(
                                "Título", value=task.get("title") or "",
                                key=f"task_title_edit_{task_id}",
                            )
                            edited_desc = st.text_area(
                                "Descrição", value=task.get("description") or "",
                                key=f"task_description_edit_{task_id}",
                            )
                            edited_subject_id = st.selectbox(
                                "Disciplina",
                                options=[
                                    s.get("id") for s in user_subjects
                                    if isinstance(s, dict) and s.get("id") is not None
                                ],
                                index=next(
                                    (i for i, s in enumerate(user_subjects)
                                     if str(s.get("id")) == str(task_subject_id)), 0
                                ),
                                format_func=lambda sid: next(
                                    (s.get("name") or f"Disciplina #{sid}"
                                     for s in user_subjects if str(s.get("id")) == str(sid)),
                                    f"Disciplina #{sid}",
                                ),
                                key=f"task_subject_edit_{task_id}",
                            )
                            safe_due = parse_xano_date(task.get("due_date"))
                            edited_due = st.date_input("Prazo", value=safe_due, key=f"task_due_edit_{task_id}")
                            edited_status = st.selectbox(
                                "Status",
                                ["pending", "in_progress", "completed"],
                                index=["pending", "in_progress", "completed"].index(
                                    _normalize_status(task.get("status"))
                                ),
                                format_func=lambda i: {
                                    "pending": "Pendente",
                                    "in_progress": "Em andamento",
                                    "completed": "Concluída",
                                }.get(i, i),
                                key=f"task_status_edit_{task_id}",
                            )
                            c_save, c_cancel = st.columns(2)
                            with c_save:
                                form_ok = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                            with c_cancel:
                                form_cancel = st.form_submit_button("Cancelar", type="secondary", use_container_width=True)
                            if form_cancel:
                                st.session_state[edit_key] = False
                                st.rerun()
                            if form_ok:
                                try:
                                    update_task_in_xano(
                                        task_id=int(task_id),
                                        title=edited_title,
                                        description=edited_desc,
                                        subject_id=int(edited_subject_id),
                                        due_date=edited_due.isoformat() if edited_due else None,
                                        status=edited_status,
                                    )
                                    if f"done_{task_id}" in st.session_state:
                                        st.session_state[f"done_{task_id}"] = (edited_status == "completed")
                                    st.session_state[edit_key] = False
                                    st.session_state["task_success_message"] = "Tarefa atualizada com sucesso!"
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Não foi possível atualizar a tarefa: {exc}")

                    if st.session_state.get(del_key):
                        st.markdown("<hr style='margin: 0.5rem 0; border: none; border-top: 1px dashed #D0DCE8;'/>", unsafe_allow_html=True)
                        st.warning(f"⚠️ Deseja excluir '{task.get('title') or 'esta tarefa'}'?")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button(
                                "Confirmar exclusão",
                                key=f"delete_task_confirm_{task_id}",
                                type="secondary",
                                use_container_width=True,
                            ):
                                try:
                                    delete_task_in_xano(int(task_id))
                                    st.session_state.pop(f"done_{task_id}", None)
                                    st.session_state[del_key] = False
                                    st.session_state["task_success_message"] = "Tarefa excluída com sucesso!"
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Não foi possível excluir a tarefa: {exc}")
                        with c2:
                            if st.button("Cancelar", key=f"cancel_del_{task_id}", use_container_width=True):
                                st.session_state[del_key] = False
                                st.rerun()
