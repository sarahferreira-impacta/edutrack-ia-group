import streamlit as st

from services.auth_service import change_password, get_current_user, update_current_user_profile
from services.subject_service import get_auth_token

st.set_page_config(page_title="Perfil", page_icon="👤")

if not get_auth_token():
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login para continuar.")
    st.stop()


def clear_session() -> None:
    for key in ["auth_token", "current_user", "is_logged_in"]:
        st.session_state.pop(key, None)


token = get_auth_token()
user = get_current_user(token)
st.session_state.current_user = user

st.title("👤 Meu Perfil")
st.caption("Confira seus dados pessoais e gerencie a segurança da sua conta.")

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Informações pessoais")
    st.write(f"**Nome completo:** {user.get('name') or 'Não informado'}")
    st.write(f"**E-mail:** {user.get('email') or 'Não informado'}")
with col2:
    st.subheader("Segurança da conta")
    st.write("**Senha:** ••••••••••")

    with st.form("profile_password_form"):
        current_password = st.text_input("Senha atual", type="password")
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirmar nova senha", type="password")
        password_submitted = st.form_submit_button("Alterar senha", type="primary")

        if password_submitted:
            try:
                change_password(current_password, new_password, confirm_password, token=token)
                st.success("Sua senha foi alterada com sucesso.")
            except Exception as exc:
                st.error(str(exc))

st.markdown("---")

with st.form("profile_update_form"):
    full_name = st.text_input("Nome completo", value=user.get("name") or "")
    email = st.text_input("E-mail", value=user.get("email") or "")
    profile_submitted = st.form_submit_button("Salvar alterações", type="primary")

    if profile_submitted:
        try:
            update_current_user_profile(name=full_name, email=email, token=token)
            st.session_state.current_user = get_current_user(token)
            st.success("Dados do perfil atualizados com sucesso.")
            st.rerun()
        except Exception as exc:
            st.error(str(exc))

st.markdown("---")
if st.button("Sair", type="secondary"):
    clear_session()
    st.rerun()

