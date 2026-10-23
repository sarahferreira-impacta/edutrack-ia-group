import streamlit as st

from services.auth_service import get_current_user, login_user, signup_user

st.set_page_config(page_title="Perfil", page_icon="👤")


def clear_session():
    for key in ["auth_token", "user", "is_logged_in"]:
        st.session_state.pop(key, None)


if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False


st.title("👤 Perfil e Acesso")

if st.session_state.auth_token:
    try:
        user = get_current_user(st.session_state.auth_token)
        st.session_state.user = user
        st.session_state.is_logged_in = True
        st.success("Você está autenticado com sucesso.")

        st.subheader("Meu perfil")
        st.write(f"**Nome:** {user.get('name') or 'Não informado'}")
        st.write(f"**E-mail:** {user.get('email') or 'Não informado'}")
        st.write(f"**Role:** {user.get('role') or 'member'}")

        if st.button("Sair", type="primary"):
            clear_session()
            st.rerun()
    except Exception as exc:
        st.warning(f"Sessão inválida ou expirada: {exc}")
        clear_session()
        st.rerun()
else:
    tab_login, tab_signup = st.tabs(["Entrar", "Criar conta"])

    with tab_login:
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("E-mail", key="login_email")
            password = st.text_input("Senha", type="password", key="login_password")
            submitted = st.form_submit_button("Entrar")

            if submitted:
                try:
                    result = login_user(email, password)
                    st.session_state.auth_token = result.get("authToken")
                    st.session_state.is_logged_in = True
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Não foi possível entrar: {exc}")

    with tab_signup:
        st.subheader("Cadastro")
        with st.form("signup_form"):
            name = st.text_input("Nome completo")
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Cadastrar")

            if submitted:
                try:
                    result = signup_user(name, email, password)
                    st.session_state.auth_token = result.get("authToken")
                    st.session_state.is_logged_in = True
                    st.success("Cadastro realizado com sucesso!")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Não foi possível cadastrar: {exc}")
