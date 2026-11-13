import pandas as pd
import streamlit as st
from datetime import datetime

from gerar_relatorio import generate_report_pdf
from services.subject_service import count_active_subjects, fetch_subjects_from_xano, get_all_subjects, get_auth_token
from services.task_service import fetch_tasks_from_xano
from styles.theme import inject_css

inject_css()


def _normalize_task_status(value):
    text = str(value or "").strip().lower()
    if text in {"completed", "done", "concluida", "concluída"}:
        return "completed"
    if text in {"in_progress", "in-progress", "em andamento"}:
        return "in_progress"
    return "pending" if text else "pending"


def summarize_dashboard(subjects, tasks):
    tasks = tasks or []
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if _normalize_task_status(task.get("status")) == "completed")
    pending_tasks = sum(1 for task in tasks if _normalize_task_status(task.get("status")) == "pending")
    in_progress_tasks = sum(1 for task in tasks if _normalize_task_status(task.get("status")) == "in_progress")
    overall_completion = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0.0
    return {
        "total_disciplines": len(subjects or []),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overall_completion": overall_completion,
    }


def summarize_subject_progress(subjects, tasks):
    results = []
    for subject in subjects or []:
        subject_id = subject.get("id")
        if subject_id is None:
            continue
        subject_tasks = [task for task in tasks or [] if str(task.get("subject_id")) == str(subject_id)]
        total_tasks = len(subject_tasks)
        completed = sum(1 for task in subject_tasks if _normalize_task_status(task.get("status")) == "completed")
        pending = sum(1 for task in subject_tasks if _normalize_task_status(task.get("status")) == "pending")
        in_progress = sum(1 for task in subject_tasks if _normalize_task_status(task.get("status")) == "in_progress")
        progress_percentage = round((completed / total_tasks) * 100, 2) if total_tasks else 0.0
        results.append(
            {
                "subject_id": subject_id,
                "subject_name": subject.get("name") or f"Disciplina #{subject_id}",
                "teacher": subject.get("teacher") or subject.get("professor") or "Não informado",
                "hours": subject.get("hours") or 0,
                "total_tasks": total_tasks,
                "completed_tasks": completed,
                "pending_tasks": pending,
                "in_progress_tasks": in_progress,
                "progress_percentage": progress_percentage,
            }
        )
    return sorted(results, key=lambda item: item["subject_name"].lower())


def _build_report_data(user, subjects, tasks, dashboard):
    """Build the data dict expected by generate_report_pdf using real session data."""
    subject_progress = summarize_subject_progress(subjects, tasks)
    report_subjects = []
    for sp in subject_progress:
        report_subjects.append({
            "name": sp["subject_name"],
            "teacher": sp.get("teacher", ""),
            "hours": sp.get("hours", 0),
            "total_tasks": sp["total_tasks"],
            "completed": sp["completed_tasks"],
            "pending": sp["pending_tasks"],
            "progress": sp["progress_percentage"],
        })

    # Build subject name lookup for tasks
    subject_names = {}
    for s in subjects or []:
        subject_names[str(s.get("id", ""))] = s.get("name") or "Sem disciplina"

    report_tasks = []
    for t in tasks or []:
        report_tasks.append({
            "title": t.get("title") or t.get("name") or "Sem título",
            "subject": subject_names.get(str(t.get("subject_id", "")), "Sem disciplina"),
            "deadline": t.get("due_date") or t.get("deadline") or "Sem prazo",
            "status": _normalize_task_status(t.get("status")),
        })

    return {
        "user": {
            "name": user.get("name", "") if user else "",
            "email": user.get("email", "") if user else "",
            "id": user.get("id", "") if user else "",
        },
        "issued_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "subjects": report_subjects,
        "tasks": report_tasks,
        "indicators": {
            "subjects": dashboard["total_disciplines"],
            "total_tasks": dashboard["total_tasks"],
            "completed": dashboard["completed_tasks"],
            "overall_progress": dashboard["overall_completion"],
        },
    }


def render_dashboard_page():
    user = st.session_state.get("current_user") or {}
    user_name = user.get("name") or "Usuário"

    st.markdown(
        f"<h1 style='color:#0C1E33;font-size:1.75rem;font-weight:800;margin-bottom:0.1rem;'>"
        f"👋 Bem-Vindo, {user_name}!</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#5A7084;font-size:0.875rem;margin-bottom:1.5rem;'>"
        "Acompanhe suas disciplinas, tarefas e seu progresso acadêmico.</p>",
        unsafe_allow_html=True,
    )

    has_token = bool(get_auth_token())
    if has_token:
        subjects = fetch_subjects_from_xano()
        tasks = fetch_tasks_from_xano(user_subjects=subjects)
    else:
        subjects = get_all_subjects()
        tasks = []

    dashboard = summarize_dashboard(subjects, tasks)
    active_subjects_count = count_active_subjects() if not has_token else sum(
        1
        for subject in subjects
        if str(subject.get("status") or "active").lower() in {"active", "in_progress", "em andamento"}
    )

    # PDF download button – uses real data from the authenticated user
    token = st.session_state.get("auth_token")
    if token:
        user = st.session_state.get("current_user") or {}
        try:
            report_data = _build_report_data(user, subjects, tasks, dashboard)
            pdf_bytes = generate_report_pdf(report_data)
            st.download_button(
                label="📄 Baixar relatório acadêmico",
                data=pdf_bytes,
                file_name="relatorio_academico.pdf",
                mime="application/pdf",
            )
        except Exception as exc:
            st.error(f"Erro ao gerar relatório: {exc}")
    else:
        st.info("Faça login para gerar o relatório acadêmico.")

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("Disciplinas ativas", active_subjects_count)
    col2.metric("Disciplinas", dashboard["total_disciplines"])
    col3.metric("Tarefas", dashboard["total_tasks"])
    col4.metric("Concluídas", dashboard["completed_tasks"])
    col5.metric("Pendentes", dashboard["pending_tasks"])
    col6.metric("Em andamento", dashboard["in_progress_tasks"])
    col7.metric("Progresso geral", f"{dashboard['overall_completion']}%")

    st.markdown("---")

    st.markdown(
        "<h3 style='color:#0C1E33;font-weight:700;margin-bottom:1rem;'>"
        "📈 Desempenho</h3>",
        unsafe_allow_html=True,
    )

    if tasks:
        chart_data = pd.DataFrame(
            {
                "status": ["Concluídas", "Pendentes", "Em andamento"],
                "count": [
                    dashboard["completed_tasks"],
                    dashboard["pending_tasks"],
                    dashboard["in_progress_tasks"],
                ],
            }
        )
        chart_col, summary_col = st.columns([2, 1])
        with chart_col:
            st.bar_chart(chart_data.set_index("status")["count"])
        with summary_col:
            for label, value, bg, text_color in [
                ("Concluídas",   dashboard["completed_tasks"],   "#CCEFBF", "#2D6A1F"),
                ("Pendentes",    dashboard["pending_tasks"],     "#FDE1AC", "#7A5000"),
                ("Em andamento", dashboard["in_progress_tasks"], "#E1D2FF", "#4B2D9A"),
            ]:
                st.markdown(
                    f"<div style='"
                    f"background:{bg};"
                    f"border-radius:12px;"
                    f"padding:12px 16px;"
                    f"margin-bottom:10px;"
                    f"'>"
                    f"<p style='margin:0;font-size:0.75rem;font-weight:600;"
                    f"color:{text_color};text-transform:uppercase;letter-spacing:0.05em;'>{label}</p>"
                    f"<span style='font-size:1.6rem;font-weight:800;color:{text_color};'>{value}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.info("Você ainda não possui tarefas cadastradas.")

    st.markdown("---")

    st.markdown(
        "<h3 style='color:#0C1E33;font-weight:700;margin-bottom:1rem;'>"
        "📚 Minhas Disciplinas</h3>",
        unsafe_allow_html=True,
    )
    subject_summary = summarize_subject_progress(subjects, tasks)

    if not subject_summary:
        st.info("Você ainda não possui disciplinas cadastradas.")
    else:
        for subject in subject_summary:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{subject['subject_name']}**")
                    st.caption(f"Professor: {subject['teacher']}")
                    st.caption(f"Horas: {subject['hours']}")
                with c2:
                    st.markdown(f"**Total: {subject['total_tasks']}**")
                    st.markdown(f"Concluídas: {subject['completed_tasks']}")
                    st.markdown(f"Pendentes: {subject['pending_tasks']}")
                    st.markdown(f"Em andamento: {subject['in_progress_tasks']}")
                st.progress(min(max(subject["progress_percentage"] / 100, 0.0), 1.0))
                st.caption(f"Progresso: {subject['progress_percentage']}%")


render_dashboard_page()
