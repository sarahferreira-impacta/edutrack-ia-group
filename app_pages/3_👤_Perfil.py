import html
import streamlit as st

from services.auth_service import get_current_user
from services.subject_service import get_auth_token
from styles.theme import inject_css

st.set_page_config(page_title="Perfil", page_icon="👤")
inject_css()

token = get_auth_token()
if not token:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login para continuar.")
    st.stop()


def clear_session() -> None:
    for key in ["auth_token", "current_user", "is_logged_in"]:
        st.session_state.pop(key, None)


# ── Busca dinâmica dos dados do usuário autenticado no Xano via JWT ──
try:
    user = get_current_user(token)
    if isinstance(user, dict) and user:
        st.session_state.current_user = user
    else:
        user = st.session_state.get("current_user") or {}
except Exception as exc:
    user = st.session_state.get("current_user") or {}
    if not user:
        st.error(f"Não foi possível carregar os dados do perfil do Xano: {exc}")

raw_name = user.get("name") or user.get("full_name") or user.get("nome") or "Não informado"
raw_email = user.get("email") or "Não informado"

user_name = html.escape(str(raw_name))
user_email = html.escape(str(raw_email))

# ── CSS com st.html (ou markdown limpo sem quebras que gerem codeblock) ──
st.html(
    """<style>
.profile-header-card {
    background-color: #EDF4FB;
    border-radius: 18px;
    padding: 1.5rem 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
    border: 1px solid #DCE7F2;
}
.profile-avatar-circle {
    width: 72px;
    height: 72px;
    min-width: 72px;
    background-color: #C7DCF3;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    color: #0C1E33;
}
.profile-header-text h1 {
    color: #0C1E33 !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.profile-header-text p {
    color: #5A7084 !important;
    font-size: 0.95rem !important;
    margin: 0.35rem 0 0 0 !important;
}
.profile-info-card {
    background-color: #FFFFFF;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(12, 30, 51, 0.06);
    border: 1px solid #E2EBF4;
    overflow: hidden;
}
.profile-info-header {
    background-color: #0C1E33;
    color: #FFFFFF;
    padding: 1rem 1.75rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.profile-info-body {
    padding: 2rem 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}
.profile-field-item {
    display: flex;
    align-items: center;
    gap: 1.25rem;
}
.profile-field-icon {
    width: 52px;
    height: 52px;
    min-width: 52px;
    background-color: #E2EBF4;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: #0C1E33;
}
.profile-field-content {
    display: flex;
    flex-direction: column;
}
.profile-field-label {
    color: #5A7084;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 0.2rem;
}
.profile-field-value {
    color: #0C1E33;
    font-size: 1.15rem;
    font-weight: 700;
    word-break: break-word;
}
</style>"""
)

# ── Renderização do HTML do Perfil via st.html ──
st.html(
    f"""<div class="profile-header-card">
    <div class="profile-avatar-circle">👤</div>
    <div class="profile-header-text">
        <h1>Meu Perfil</h1>
        <p>Aqui estão suas informações cadastradas no EduTrack AI</p>
    </div>
</div>
<div class="profile-info-card">
    <div class="profile-info-header">
        <span>👤</span>
        <span>Informações Pessoais</span>
    </div>
    <div class="profile-info-body">
        <div class="profile-field-item">
            <div class="profile-field-icon">👤</div>
            <div class="profile-field-content">
                <span class="profile-field-label">Nome Completo</span>
                <span class="profile-field-value">{user_name}</span>
            </div>
        </div>
        <div class="profile-field-item">
            <div class="profile-field-icon">✉️</div>
            <div class="profile-field-content">
                <span class="profile-field-label">E-mail</span>
                <span class="profile-field-value">{user_email}</span>
            </div>
        </div>
    </div>
</div>"""
)
