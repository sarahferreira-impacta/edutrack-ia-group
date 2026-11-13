import re

import streamlit as st

from services.auth_service import get_current_user, login_user, signup_user
from styles.theme import inject_css

st.set_page_config(
    page_title="EduTrack AI - Portal Acadêmico",
    page_icon="🎓",
    layout="wide",
)

inject_css()


def clear_session() -> None:
    for key in ["auth_token", "current_user", "is_logged_in"]:
        st.session_state.pop(key, None)
    st.session_state["show_logout_modal"] = False


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


@st.dialog("Encerrar Sessão")
def confirm_logout_dialog():
    st.markdown(
        """
        <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🚪</div>
            <h3 style="color: #0C1E33; font-weight: 700; margin: 0 0 0.5rem 0;">Deseja mesmo sair da sua conta?</h3>
            <p style="color: #5A7084; font-size: 0.9rem; margin: 0;">Você precisará informar seu e-mail e senha novamente para entrar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c_cancel, c_confirm = st.columns(2)
    with c_cancel:
        if st.button("Cancelar", key="logout_cancel_btn", use_container_width=True):
            st.rerun()
    with c_confirm:
        if st.button("Sim, sair", type="primary", key="logout_confirm_btn", use_container_width=True):
            clear_session()
            st.rerun()


def render_auth_screen() -> None:
    st.html(
        """
        <style>
        /* Fundo geral da tela de login/cadastro limpo e público */
        html, body {
            margin: 0 !important;
            padding: 0 !important;
        }

        .stApp {
            background: linear-gradient(135deg, #F0F4F8 0%, #E2EBF4 50%, #F5F8FB 100%) !important;
            min-height: 100vh !important;
            overflow: hidden !important;
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        [data-testid="stMain"],
        section[data-testid="stMain"],
        .block-container {
            margin-top: 0 !important;
            padding-top: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: none !important;
            overflow: visible !important;
        }

        /* Oculta totalmente qualquer resquício de sidebar na tela pública */
        [data-testid="stSidebar"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
        }

        [data-testid="stHeader"] {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        .auth-topbar {
            background-color: #0C1E33;
            padding: 0.45rem 1.5rem 0.75rem;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.9rem;
            box-shadow: 0 4px 12px rgba(12, 30, 51, 0.15);
            position: relative !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            z-index: 1 !important;
            opacity: 1 !important;
            visibility: visible !important;
            overflow: visible !important;
            background-image: none !important;
            border-radius: 0;
            width: 100%;
            max-width: none;
            box-sizing: border-box;
            flex-wrap: nowrap;
        }

        .auth-topbar::before,
        .auth-topbar::after,
        .auth-topbar-title::before,
        .auth-topbar-title::after {
            content: none !important;
            display: none !important;
            background: transparent !important;
            position: static !important;
            width: 0 !important;
            height: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }

        .auth-topbar * {
            opacity: 1 !important;
            visibility: visible !important;
            background: transparent !important;
        }

        .auth-topbar-icon {
            font-size: 2.2rem;
            line-height: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-left: 0.2rem;
            transform: translateY(-1px);
        }

        .auth-topbar-copy {
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-width: 0;
            position: static !important;
            z-index: auto !important;
            margin-left: 0.15rem;
        }

        .auth-topbar-title {
            color: #FFFFFF !important;
            background: transparent !important;
            opacity: 1 !important;
            visibility: visible !important;
            display: block !important;
            font-size: clamp(1.8rem, 2.2vw, 2.6rem);
            font-weight: 800;
            letter-spacing: 0.04em;
            margin: 0;
            line-height: 1.1;
            text-shadow: none !important;
            box-shadow: none !important;
            position: static !important;
            top: auto !important;
            z-index: auto !important;
            flex: 0 0 auto;
            white-space: nowrap;
        }

        .auth-topbar-subtitle {
            color: rgba(255, 255, 255, 0.82) !important;
            opacity: 1 !important;
            visibility: visible !important;
            font-size: clamp(0.82rem, 1vw, 1rem);
            margin: 0.15rem 0 0 0;
            font-weight: 400;
            display: block;
            line-height: 1.4;
            white-space: normal;
        }

        .auth-topbar-icon {
            font-size: clamp(2rem, 2.4vw, 2.7rem);
            line-height: 1;
            display: inline-block;
            flex-shrink: 0;
            transform: translateY(-1px);
        }

        div[data-testid="stTextInput"] {
            position: relative !important;
        }

        div[data-testid="stTextInput"] input {
            padding-right: 3rem !important;
        }

        div[data-testid="stTextInput"] button[aria-label*="Show password"],
        div[data-testid="stTextInput"] button[aria-label*="Hide password"] {
            position: absolute !important;
            right: 0.5rem !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            width: 2.25rem !important;
            min-width: 2.25rem !important;
            height: 2.25rem !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            border-radius: 8px !important;
            background: transparent !important;
            box-shadow: none !important;
            color: transparent !important;
            font-size: 0 !important;
            line-height: 0 !important;
            overflow: hidden !important;
            z-index: 2 !important;
        }

        div[data-testid="stTextInput"] button[aria-label*="Show password"]::before,
        div[data-testid="stTextInput"] button[aria-label*="Hide password"]::before {
            content: "" !important;
            display: block !important;
            width: 18px !important;
            height: 18px !important;
            margin: 0 auto !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%230C1E33' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z'/%3E%3Ccircle cx='12' cy='12' r='3'/%3E%3C/svg%3E");
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-size: contain !important;
        }

        div[data-testid="stTextInput"] button[aria-label*="Show password"] span,
        div[data-testid="stTextInput"] button[aria-label*="Hide password"] span,
        div[data-testid="stTextInput"] button[aria-label*="Show password"] p,
        div[data-testid="stTextInput"] button[aria-label*="Hide password"] p,
        div[data-testid="stTextInput"] button[aria-label*="Show password"] svg,
        div[data-testid="stTextInput"] button[aria-label*="Hide password"] svg {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            font-size: 0 !important;
        }

        .auth-label {
            color: #0C1E33;
            font-weight: 800;
            font-size: 0.82rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
            display: block;
        }

        div[data-testid="stTextInput"] input {
            background-color: #DFE7EE !important;
            border: 1px solid #C8D6E2 !important;
            border-radius: 10px !important;
            height: 48px !important;
            padding: 0 1rem !important;
            font-size: 0.95rem !important;
            color: #0C1E33 !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #0C1E33 !important;
            box-shadow: 0 0 0 3px rgba(12, 30, 51, 0.18) !important;
            background-color: #FFFFFF !important;
        }

        .auth-submit-btn button {
            background-color: #0C1E33 !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            height: 48px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            letter-spacing: 0.02em !important;
            border: none !important;
            margin-top: 1rem !important;
        }

        .auth-submit-btn button * {
            color: #FFFFFF !important;
        }

        .auth-submit-btn button:hover {
            background-color: #1B3A5B !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(12, 30, 51, 0.2) !important;
        }

        .auth-tab-btn-active button {
            background-color: #0C1E33 !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            border: none !important;
            border-bottom: 3px solid #E11D48 !important;
            font-weight: 700 !important;
            height: 46px !important;
        }

        .auth-tab-btn-active button * {
            color: #FFFFFF !important;
        }

        .auth-tab-btn-inactive button {
            background-color: transparent !important;
            color: #0C1E33 !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            height: 46px !important;
        }

        .auth-tab-btn-inactive button * {
            color: #0C1E33 !important;
        }

        .auth-tab-btn-inactive button:hover {
            background-color: rgba(12, 30, 51, 0.05) !important;
        }
        </style>
    
        <div class="auth-topbar">
            <div class="auth-topbar-icon">📖</div>
            <div class="auth-topbar-copy">
                <h1 class="auth-topbar-title">EDUTRACK AI</h1>
                <p class="auth-topbar-subtitle">Gestão Acadêmica Com Autenticação Segura E Navegação Simplificada</p>
            </div>
        </div>
        """
    )

    _, center_col, _ = st.columns([1, 4.5, 1])

    with center_col:
        # Exibe mensagens globais de feedback (ex: após cadastro com sucesso)
        if "signup_success_msg" in st.session_state:
            st.success(st.session_state.pop("signup_success_msg"))
        if "auth_error_msg" in st.session_state:
            st.error(st.session_state.pop("auth_error_msg"))

        with st.container(border=True):
            # Abas superiores: [ ➔ Entrar ]  [ 👤+ Criar Conta ]
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                is_active = (st.session_state["auth_mode"] == "login")
                btn_class = "auth-tab-btn-active" if is_active else "auth-tab-btn-inactive"
                st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
                if st.button("➔  Entrar", key="tab_login", use_container_width=True):
                    st.session_state["auth_mode"] = "login"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with t_col2:
                is_active = (st.session_state["auth_mode"] == "signup")
                btn_class = "auth-tab-btn-active" if is_active else "auth-tab-btn-inactive"
                st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
                if st.button("👤+  Criar Conta", key="tab_signup", use_container_width=True):
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

            # ── Formulário: ENTRAR (LOGIN) ──
            if st.session_state["auth_mode"] == "login":
                # Preenche automaticamente com o e-mail cadastrado se existir
                default_email = st.session_state.pop("prefill_login_email", "")

                st.markdown('<label class="auth-label">EMAIL</label>', unsafe_allow_html=True)
                email = st.text_input("EMAIL", value=default_email, key="login_email", label_visibility="collapsed")

                st.markdown('<label class="auth-label">SENHA</label>', unsafe_allow_html=True)
                password = st.text_input("SENHA", type="password", key="login_password", label_visibility="collapsed")

                st.markdown('<div class="auth-submit-btn">', unsafe_allow_html=True)
                if st.button("Entrar", type="primary", key="btn_submit_login", use_container_width=True):
                    if not email or not password:
                        st.error("Informe e-mail e senha para continuar.")
                    else:
                        with st.spinner("Entrando no EduTrack AI..."):
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
                                # Mensagem amigável sem tracebacks
                                err_text = str(exc)
                                if "400" in err_text or "401" in err_text or "403" in err_text:
                                    st.error("E-mail ou senha incorretos. Verifique suas credenciais e tente novamente.")
                                else:
                                    st.error("Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.")
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Formulário: CRIAR CONTA (CADASTRO) ──
            else:
                st.markdown('<label class="auth-label">NOME COMPLETO</label>', unsafe_allow_html=True)
                name = st.text_input("NOME COMPLETO", key="signup_name", label_visibility="collapsed")

                st.markdown('<label class="auth-label">EMAIL</label>', unsafe_allow_html=True)
                email = st.text_input("EMAIL", key="signup_email", label_visibility="collapsed")

                st.markdown('<label class="auth-label">SENHA</label>', unsafe_allow_html=True)
                password = st.text_input("SENHA", type="password", key="signup_password", label_visibility="collapsed")

                st.markdown('<label class="auth-label">CONFIRMAR SENHA</label>', unsafe_allow_html=True)
                confirm_password = st.text_input("CONFIRMAR SENHA", type="password", key="signup_confirm_password", label_visibility="collapsed")

                st.markdown('<div class="auth-submit-btn">', unsafe_allow_html=True)
                if st.button("Criar Conta", type="primary", key="btn_submit_signup", use_container_width=True):
                    if not name.strip() or not email or not password or not confirm_password:
                        st.error("Todos os campos são obrigatórios.")
                    elif not is_valid_email(email):
                        st.error("Informe um e-mail válido.")
                    elif len(password) < 8:
                        st.error("A senha deve conter pelo menos 8 caracteres.")
                    elif password != confirm_password:
                        st.error("As senhas informadas não coincidem.")
                    else:
                        with st.spinner("Criando sua conta..."):
                            try:
                                signup_user(name, email, password)
                                # Sucesso: redireciona para aba Entrar com mensagem e e-mail pré-preenchido
                                st.session_state["signup_success_msg"] = "Conta criada com sucesso! Agora você já pode entrar no EduTrack AI."
                                st.session_state["prefill_login_email"] = email.strip().lower()
                                st.session_state["auth_mode"] = "login"
                                st.rerun()
                            except Exception as exc:
                                err_text = str(exc)
                                if "already exists" in err_text.lower() or "duplicat" in err_text.lower() or "400" in err_text:
                                    st.error("Este e-mail já está cadastrado no sistema. Utilize outro e-mail ou faça login.")
                                else:
                                    st.error("Não foi possível criar a conta. Verifique os dados e tente novamente.")
                st.markdown('</div>', unsafe_allow_html=True)


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
        st.Page("app_pages/2_📝_Tarefas.py", title="Tarefas", icon="📋"),
        st.Page("app_pages/3_👤_Perfil.py", title="Perfil", icon="👤"),
    ]
    selected_page = st.navigation(pages, position="sidebar")

    # Botão de Logout como ação na sidebar (não como página interna)
    with st.sidebar:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="sidebar_logout_action_btn", use_container_width=True):
            confirm_logout_dialog()

    selected_page.run()
