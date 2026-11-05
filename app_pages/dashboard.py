import pandas as pd
import streamlit as st

from services.subject_service import count_active_subjects, fetch_subjects_from_xano, get_all_subjects, get_auth_token
from services.task_service import fetch_tasks_from_xano


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


def render_dashboard_page():
    st.title("📊 Painel de Controle")
    st.caption("Bem-vindo ao seu assistente acadêmico! Acompanhe suas disciplinas, tarefas e seu progresso acadêmico.")

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

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.metric("Disciplinas ativas", active_subjects_count)
    col2.metric("Disciplinas", dashboard["total_disciplines"])
    col3.metric("Tarefas", dashboard["total_tasks"])
    col4.metric("Concluídas", dashboard["completed_tasks"])
    col5.metric("Pendentes", dashboard["pending_tasks"])
    col6.metric("Em andamento", dashboard["in_progress_tasks"])
    col7.metric("Progresso geral", f"{dashboard['overall_completion']}%")

    st.markdown("---")
    st.subheader("Relatório de Tarefas")

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
            for label, value in [
                ("Concluídas", dashboard["completed_tasks"]),
                ("Pendentes", dashboard["pending_tasks"]),
                ("Em andamento", dashboard["in_progress_tasks"]),
            ]:
                color = "#16a34a" if label == "Concluídas" else "#f59e0b" if label == "Pendentes" else "#2563eb"
                st.markdown(
                    f"<div style='border-left: 5px solid {color}; padding: 10px 12px; margin-bottom: 8px; border-radius: 8px; background: rgba(255,255,255,0.02);'>"
                    f"<strong>{label}</strong><br><span style='font-size: 1.4rem;'>{value}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.info("Você ainda não possui tarefas cadastradas.")

    st.markdown("---")
    st.subheader("Minhas Disciplinas")
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
