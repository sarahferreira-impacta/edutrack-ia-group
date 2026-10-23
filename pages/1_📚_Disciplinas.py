import streamlit as st

from services.subject_service import fetch_subjects_from_xano

st.set_page_config(page_title="Disciplinas", page_icon="📚")

st.title("Gestão de Disciplinas")

# Abas para separar Listagem de Cadastro
tab_lista, tab_novo = st.tabs(["📋 Listar", "➕ Nova Disciplina"])

with tab_novo:
    st.subheader("Cadastrar Nova Matéria")
    with st.form("form_disciplina"):
        nome = st.text_input("Nome da Disciplina")
        professor = st.text_input("Nome do Professor")
        dia_semana = st.selectbox("Dia da Aula", ["Seg", "Ter", "Qua", "Qui", "Sex"])

        submitted = st.form_submit_button("Salvar")
        if submitted:
            st.success(f"Disciplina {nome} cadastrada! (cadastro em desenvolvimento)")

with tab_lista:
    try:
        subjects = fetch_subjects_from_xano()
    except Exception:
        subjects = []
        st.error("Não foi possível carregar as disciplinas do Xano. Verifique a conexão ou o token de autenticação.")

    if not subjects:
        st.info("Nenhuma disciplina foi encontrada no Xano no momento.")
    else:
        table_rows = [
            {
                "Nome": subject.get("name") or "Sem nome",
                "Professor": subject.get("professor") or subject.get("teacher") or "Não informado",
                "Semestre": subject.get("semester") or "Não informado",
                "Status": subject.get("status") or "active",
            }
            for subject in subjects
        ]
        st.dataframe(table_rows, use_container_width=True)