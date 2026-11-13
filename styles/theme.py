"""
EduTrack AI — Design System
Paleta de cores e CSS compartilhado entre todas as páginas.
NÃO contém lógica de negócio.
"""

EDUTRACK_CSS = """
<style>
/* =========================================================
   IMPORT FONT
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* =========================================================
   VARIÁVEIS DE DESIGN
   ========================================================= */
:root {
    --navy:        #0C1E33;
    --navy-hover:  #1B3A5B;
    --bg:          #FFFFFF;
    --input-bg:    #DFE7EE;
    --green:       #CCEFBF;
    --blue-pastel: #BAE5F5;
    --yellow:      #FDE1AC;
    --purple:      #E1D2FF;
    --text-main:   #0C1E33;
    --text-muted:  #5A7084;
    --border:      #D0DCE8;
    --shadow:      0 2px 8px rgba(12,30,51,0.08);
    --radius-sm:   8px;
    --radius-md:   12px;
    --radius-lg:   16px;
}

/* =========================================================
   RESET GLOBAL
   ========================================================= */
html, body, [class*="st-"] {
    font-family: 'Inter', 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text-main);
}

.main .block-container {
    background-color: var(--bg);
    padding: 2rem 2.5rem 2rem 2.5rem;
    border-radius: var(--radius-lg);
}

/* =========================================================
   SIDEBAR FIEL À IMAGEM DE REFERÊNCIA
   ========================================================= */
[data-testid="stSidebar"] {
    background-color: var(--navy) !important;
    width: 250px !important;
    min-width: 250px !important;
    max-width: 250px !important;
    height: 100vh !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Garante apenas UM cabeçalho da sidebar no topo */
[data-testid="stSidebarHeader"] {
    display: none !important;
}

/* Injeta o cabeçalho único 'EDUTRACK AI' exclusivamente antes da lista de navegação */
[data-testid="stSidebarNav"]::before {
    content: "📖  EDUTRACK AI" !important;
    display: flex !important;
    align-items: center !important;
    padding: 1.5rem 1.25rem 1.25rem 1.25rem !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.06em !important;
    color: #FFFFFF !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
    margin-bottom: 0.25rem !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebarNav"] ul {
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: column !important;
}

[data-testid="stSidebarNav"] li {
    padding: 0 !important;
    margin: 0 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stSidebarNav"] a {
    height: 50px !important;
    min-height: 50px !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 1.25rem !important;
    margin: 0 !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    border-radius: 0 !important;
    transition: background 0.15s ease, color 0.15s ease !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
    color: #FFFFFF !important;
}

/* Item selecionado na Sidebar: fundo branco, texto navy, cantos arredondados no lado direito */
[data-testid="stSidebarNav"] a[aria-current="page"],
[data-testid="stSidebarNav"] a.active {
    background-color: #FFFFFF !important;
    color: var(--navy) !important;
    font-weight: 800 !important;
    border-radius: 0 24px 24px 0 !important;
    margin-right: 0.75rem !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] *,
[data-testid="stSidebarNav"] a.active * {
    color: var(--navy) !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
    color: inherit !important;
}

/* Botão de Logout na Sidebar */
.sidebar-logout-container {
    padding: 0.75rem 1rem !important;
    border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    margin-top: 1rem !important;
}

.sidebar-logout-container button {
    background-color: transparent !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.25) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}

.sidebar-logout-container button:hover {
    background-color: rgba(225, 29, 72, 0.15) !important;
    border-color: #E11D48 !important;
    color: #FFFFFF !important;
}

/* =========================================================
   COMPONENTE PROGRESSO ACADÊMICO (EXPANDER)
   Remove totalmente a palavra 'arrow' e ajusta o título
   ========================================================= */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 1px 4px rgba(12,30,51,0.04) !important;
    overflow: hidden !important;
}

[data-testid="stExpander"] summary {
    background-color: #F0F4F8 !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1.25rem !important;
    border-bottom: 1px solid var(--border) !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
}

/* Título em AZUL-MARINHO ESCURO (#0C1E33), sem quebra ou sobreposição */
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p,
[data-testid="stExpander"] summary span:not([data-testid="stIconMaterial"]) {
    color: #0C1E33 !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    margin: 0 !important;
}

/* Remove completamente textos soltos como 'arrow', 'expand_more' dos expanders */
[data-testid="stExpander"] summary [data-testid="stIconMaterial"],
[data-testid="stExpander"] summary .material-symbols-rounded,
[data-testid="stExpander"] summary span.material-symbols-outlined {
    font-size: 0 !important;
    color: transparent !important;
    overflow: hidden !important;
    width: 20px !important;
    height: 20px !important;
    display: inline-block !important;
    vertical-align: middle !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="%230C1E33" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>') !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
}

[data-testid="stExpander"][open] summary [data-testid="stIconMaterial"],
[data-testid="stExpander"][open] summary .material-symbols-rounded,
[data-testid="stExpander"][open] summary span.material-symbols-outlined {
    transform: rotate(180deg) !important;
}

[data-testid="stExpander"] summary svg {
    fill: #0C1E33 !important;
}

/* =========================================================
   BOTÕES GERAIS E ESTADOS INTERATIVOS (HOVER / ACTIVE / FOCUS)
   ========================================================= */

/* Botões escuros (Primários) */
[data-testid="stButton"] > button[kind="primary"],
.stButton > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button:not([kind="secondary"]) {
    background-color: var(--navy) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--navy) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.35rem !important;
    cursor: pointer !important;
    transition: background-color 200ms ease, transform 150ms ease, box-shadow 200ms ease !important;
}

[data-testid="stButton"] > button[kind="primary"] *,
.stButton > button[kind="primary"] *,
[data-testid="stFormSubmitButton"] > button * {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

[data-testid="stButton"] > button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background-color: var(--navy-hover) !important;
    border-color: var(--navy-hover) !important;
    color: #FFFFFF !important;
    cursor: pointer !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(12, 30, 51, 0.18) !important;
}

[data-testid="stButton"] > button[kind="primary"]:active,
.stButton > button[kind="primary"]:active,
[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 1px 4px rgba(12, 30, 51, 0.12) !important;
}

/* Botões claros / secundários */
[data-testid="stButton"] > button[kind="secondary"],
.stButton > button[kind="secondary"],
[data-testid="stButton"] > button:not([kind="primary"]),
.stButton > button:not([kind="primary"]) {
    background-color: #FFFFFF !important;
    color: var(--navy) !important;
    border: 1.5px solid #D0DCE8 !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.35rem !important;
    cursor: pointer !important;
    transition: background-color 200ms ease, border-color 200ms ease, transform 150ms ease, box-shadow 200ms ease !important;
}

[data-testid="stButton"] > button:not([kind="primary"]) *,
.stButton > button:not([kind="primary"]) * {
    color: var(--navy) !important;
}

[data-testid="stButton"] > button:not([kind="primary"]):hover,
.stButton > button:not([kind="primary"]):hover {
    background-color: var(--input-bg) !important;
    border-color: var(--navy) !important;
    color: var(--navy) !important;
    cursor: pointer !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 8px rgba(12, 30, 51, 0.08) !important;
}

[data-testid="stButton"] > button:not([kind="primary"]):active,
.stButton > button:not([kind="primary"]):active {
    transform: translateY(1px) !important;
}

/* Botões desabilitados */
[data-testid="stButton"] > button:disabled,
.stButton > button:disabled,
[data-testid="stFormSubmitButton"] > button:disabled {
    background-color: #E2E8F0 !important;
    color: #94A3B8 !important;
    border-color: #CBD5E1 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Botão Download Relatório */
[data-testid="stDownloadButton"] > button {
    background-color: var(--navy) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 1.4rem !important;
    cursor: pointer !important;
    transition: background-color 200ms ease, transform 150ms ease, box-shadow 200ms ease !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

[data-testid="stDownloadButton"] > button * {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background-color: var(--navy-hover) !important;
    color: #FFFFFF !important;
    cursor: pointer !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(12, 30, 51, 0.18) !important;
}

[data-testid="stDownloadButton"] > button:active {
    transform: translateY(1px) !important;
}

/* =========================================================
   INPUTS / TEXTAREAS COM FOCO INTERATIVO
   ========================================================= */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
    background-color: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-main) !important;
    padding: 0.5rem 0.75rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 200ms ease, box-shadow 200ms ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: var(--navy) !important;
    box-shadow: 0 0 0 3px rgba(12, 30, 51, 0.18) !important;
    background-color: #FFFFFF !important;
}

/* =========================================================
   ABAS DA PÁGINA DISCIPLINAS
   ========================================================= */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background-color: transparent !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0.5rem !important;
    border-bottom: 2px solid #E8EFF5 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background-color: #FFFFFF !important;
    color: var(--navy) !important;
    border: 1px solid var(--border) !important;
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.25rem !important;
    cursor: pointer !important;
    transition: all 200ms ease !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background-color: #F8FAFC !important;
    color: var(--navy) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background-color: var(--navy) !important;
    color: #FFFFFF !important;
    border-color: var(--navy) !important;
    border-bottom: 3px solid #E11D48 !important;
}

[data-testid="stTabs"] [aria-selected="true"] * {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: #E11D48 !important;
    height: 3px !important;
}

/* =========================================================
   TÍTULOS E TEXTOS
   ========================================================= */
h1, .stTitle {
    color: var(--navy) !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
}
h2, h3 {
    color: var(--navy) !important;
    font-weight: 600 !important;
}
h4 { color: var(--navy) !important; font-weight: 600 !important; }
p, label, .stCaption, caption {
    color: var(--text-muted) !important;
    font-size: 0.875rem !important;
}
.stCaption p { color: var(--text-muted) !important; }

/* Labels dos formulários */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stSelectbox"] label {
    color: var(--navy) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    margin-bottom: 2px !important;
}

/* =========================================================
   MÉTRICAS
   ========================================================= */
[data-testid="stMetric"] {
    background-color: var(--input-bg);
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
    padding: 1rem 1.25rem !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMetricValue"] {
    color: var(--navy) !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
}

/* =========================================================
   ALERTAS
   ========================================================= */
[data-testid="stAlert"][data-baseweb="notification"] {
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
}

/* =========================================================
   PROGRESS BAR
   ========================================================= */
[data-testid="stProgressBar"] > div > div {
    background-color: var(--navy) !important;
    border-radius: 999px !important;
}
[data-testid="stProgressBar"] > div {
    background-color: var(--input-bg) !important;
    border-radius: 999px !important;
    height: 8px !important;
}

/* =========================================================
   CHECKBOX
   ========================================================= */
[data-testid="stCheckbox"] label {
    color: var(--navy) !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
}
[data-testid="stCheckbox"] span[data-baseweb="checkbox"] > div {
    border-color: var(--navy) !important;
}

/* =========================================================
   HEADER TOP-BAR
   ========================================================= */
[data-testid="stHeader"] {
    position: static !important;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    height: auto !important;
    background-color: var(--navy) !important;
    box-shadow: none !important;
    z-index: auto !important;
}
[data-testid="stToolbar"] {
    display: none !important;
}
#MainMenu { display: none !important; }
footer { display: none !important; }

/* =========================================================
   BADGES DE STATUS
   ========================================================= */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.badge-green  { background: #CCEFBF; color: #2D6A1F; }
.badge-yellow { background: #FDE1AC; color: #7A5000; }
.badge-purple { background: #E1D2FF; color: #4B2D9A; }
.badge-blue   { background: #BAE5F5; color: #0D5C82; }
</style>
"""


def inject_css() -> None:
    """Injeta o CSS do Design System EduTrack AI via st.markdown."""
    import streamlit as st
    st.markdown(EDUTRACK_CSS, unsafe_allow_html=True)


def status_badge_html(status: str) -> str:
    """Retorna HTML de badge colorido conforme o status."""
    mapping = {
        "completed":   ("badge-green",  "Concluída"),
        "done":        ("badge-green",  "Concluída"),
        "in_progress": ("badge-purple", "Em andamento"),
        "pending":     ("badge-yellow", "Pendente"),
    }
    cls, label = mapping.get(str(status).lower(), ("badge-blue", status.capitalize()))
    return f'<span class="badge {cls}">{label}</span>'
