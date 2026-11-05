import re

import streamlit as st

from services.auth_service import get_current_user, login_user, signup_user

st.set_page_config(
    page_title="EduTrack AI - Portal Acadêmico",
    page_icon="🎓",
    layout="wide",
)


def clear_session() -> None:
    for key in ["auth_token", "current_user", "is_logged_in"]:
        st.session_state.pop(key, None)


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", (email or "").strip()))


def summarize_dashboard(subjects, tasks):
    total_tasks = len(tasks or [])
    completed_tasks = sum(1 for task in tasks or [] if str(task.get("status") or "").lower() in {"completed", "done", "concluida", "concluída"})
    pending_tasks = sum(1 for task in tasks or [] if str(task.get("status") or "").lower() in {"pending", ""})
    in_progress_tasks = sum(1 for task in tasks or [] if str(task.get("status") or "").lower() == "in_progress")
    overall_completion = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0.0
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overall_completion": overall_completion,
    }


def summarize_subject_progress(subjects, tasks):
    subjects_list = subjects or []
    task_list = tasks or []
    summary = []
    for subject in subjects_list:
        subject_id = subject.get("id")
        if subject_id is None:
            continue
        related_tasks = [task for task in task_list if str(task.get("subject_id")) == str(subject_id)]
        total_tasks = len(related_tasks)
        completed_tasks = sum(1 for task in related_tasks if str(task.get("status") or "").lower() in {"completed", "done", "concluida", "concluída"})
        progress = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0.0
        summary.append({
            "subject_id": subject_id,
            "subject_name": subject.get("name") or f"Disciplina #{subject_id}",
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress_percentage": progress,
        })
    return summary


def render_auth_screen() -> None:
    st.title("🎓 EduTrack AI")
    st.caption("Gestão acadêmica com autenticação segura e navegação simplificada.")
    auth_mode = st.radio("Acesso", ["Entrar", "Criar conta"], horizontal=True, index=0)

    if auth_mode == "Entrar":
        email = st.text_input("E-mail", key="login_email")
        password = st.text_input("Senha", type="password", key="login_password")

        if st.button("Entrar", type="primary"):
            if not email or not password:
                st.error("Informe e-mail e senha para continuar.")
            else:
                try:
                    result = login_user(email, password)
                    token = result.get("authToken") or result.get("token")
                    if not token:
                        raise ValueError("Resposta do Xano não retornou token de autenticação.")
                    st.session_state.auth_token = token
                    st.session_state.current_user = get_current_user(token)
                    st.session_state.is_logged_in = True
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Não foi possível entrar: {exc}")

        st.markdown("---")
        st.write("Não possui uma conta?")
        if st.button("Cadastre-se", use_container_width=True):
            st.session_state["auth_mode"] = "signup"
            st.rerun()
    else:
        name = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirmar senha", type="password")

        if st.button("Criar conta", type="primary"):
            if not name.strip() or not email or not password or not confirm_password:
                st.error("Todos os campos são obrigatórios.")
            elif not is_valid_email(email):
                st.error("Informe um e-mail válido.")
            elif len(password) < 8:
                st.error("A senha deve conter pelo menos 8 caracteres.")
            elif password != confirm_password:
                st.error("As senhas informadas não coincidem.")
            else:
                try:
                    signup_user(name, email, password)
                    st.success("Conta criada com sucesso! Faça login para continuar.")
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
                except Exception as exc:
                    st.error(f"Não foi possível criar a conta: {exc}")


if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

if not st.session_state.auth_token:
    render_auth_screen()
else:
    pages = [
        st.Page("app_pages/dashboard.py", title="Dashboard", icon="📊"),
        st.Page("app_pages/1_📚_Disciplinas.py", title="Disciplinas", icon="📚"),
        st.Page("app_pages/2_📝_Tarefas.py", title="Tarefas", icon="📝"),
        st.Page("app_pages/3_👤_Perfil.py", title="Perfil", icon="👤"),
    ]
    selected_page = st.navigation(pages, position="sidebar")
    selected_page.run()
