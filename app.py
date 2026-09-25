import streamlit as st
from services.subject_service import (
    get_all_subjects,
    get_active_subjects,
    count_active_subjects,
    create_subject,
    update_subject,
    delete_subject,
)

# Configuração da Página
st.set_page_config(
    page_title="EduTrack AI - Portal Acadêmico",
    page_icon="🎓",
    layout="wide"
)

# Sidebar (Menu Lateral)
st.sidebar.title("🎓 EduTrack AI")
st.sidebar.caption("Seu assistente acadêmico inteligente")
menu_option = st.sidebar.radio(
    "Navegar",
    ["Dashboard", "Disciplinas", "Tarefas"],
    index=0
)

# Dicionários auxiliares para status
STATUS_LABELS = {
    "active": "🟢 Em Andamento",
    "completed": "🔵 Concluída",
    "archived": "⚪ Arquivada"
}

STATUS_OPTIONS = {
    "Ativa": "active",
    "Concluída": "completed",
    "Arquivada": "archived"
}
REVERSE_STATUS = {v: k for k, v in STATUS_OPTIONS.items()}

# ==========================================
# 1. DASHBOARD
# ==========================================
if menu_option == "Dashboard":
    st.title("📊 Painel de Controle")
    st.write("Bem-vindo ao seu assistente acadêmico! Acompanhe o progresso das suas disciplinas e metas.")

    active_count = count_active_subjects()
    all_subjects = get_all_subjects()

    # Métricas Principais
    col1, col2, col3 = st.columns(3)
    col1.metric("Disciplinas Ativas", str(active_count))
    col2.metric("Total de Disciplinas", str(len(all_subjects)))
    col3.metric("Tarefas Pendentes", "0")

    st.divider()

    # Resumo das Disciplinas Ativas
    st.subheader("📚 Disciplinas em Curso")
    active_subjects = get_active_subjects()

    if not active_subjects:
        st.info("Nenhuma disciplina ativa no momento. Acesse a aba 'Disciplinas' para cadastrar!")
    else:
        cols = st.columns(min(len(active_subjects), 3))
        for idx, sub in enumerate(active_subjects):
            col = cols[idx % 3]
            with col:
                with st.container(border=True):
                    color = sub.get("color", "#4F46E5")
                    st.markdown(
                        f"<div style='border-left: 5px solid {color}; padding-left: 10px; margin-bottom: 8px;'>"
                        f"<h4 style='margin:0; padding:0;'>{sub['name']}</h4>"
                        f"<span style='color: gray; font-size: 0.85rem;'>{sub.get('code', '')}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    if sub.get("professor"):
                        st.caption(f"👨‍🏫 **Professor(a):** {sub['professor']}")
                    if sub.get("semester"):
                        st.caption(f"🗓️ **Semestre:** {sub['semester']}")

# ==========================================
# 2. DISCIPLINAS
# ==========================================
elif menu_option == "Disciplinas":
    st.title("📖 Gerenciamento de Disciplinas")
    st.write("Organize todas as matérias do seu curso, professores e períodos letivos.")

    tab_list, tab_create = st.tabs(["📋 Minhas Disciplinas", "➕ Cadastrar Nova Disciplina"])

    # --- ABA 1: LISTAGEM E EDIÇÃO ---
    with tab_list:
        subjects = get_all_subjects()

        if not subjects:
            st.info("Nenhuma disciplina cadastrada ainda. Clique na aba **'Cadastrar Nova Disciplina'** para começar!")
        else:
            col_filter, col_total = st.columns([3, 1])
            with col_filter:
                filter_status = st.selectbox(
                    "Filtrar por Status",
                    ["Todas", "Ativas", "Concluídas", "Arquivadas"],
                    index=0
                )
            with col_total:
                st.write("")
                st.write(f"**Total listado:** {len(subjects)}")

            filtered = subjects
            if filter_status == "Ativas":
                filtered = [s for s in subjects if s.get("status") == "active"]
            elif filter_status == "Concluídas":
                filtered = [s for s in subjects if s.get("status") == "completed"]
            elif filter_status == "Arquivadas":
                filtered = [s for s in subjects if s.get("status") == "archived"]

            if not filtered:
                st.warning(f"Nenhuma disciplina com o status '{filter_status}' encontrada.")
            else:
                for sub in filtered:
                    sub_id = sub["id"]
                    color = sub.get("color", "#4F46E5")
                    status_text = STATUS_LABELS.get(sub.get("status", "active"), "🟢 Em Andamento")

                    with st.container(border=True):
                        col_card, col_actions = st.columns([4, 1.2])

                        with col_card:
                            st.markdown(
                                f"<div style='border-left: 6px solid {color}; padding-left: 12px; margin-bottom: 6px;'>"
                                f"<h3 style='margin: 0;'>{sub['name']} <span style='font-size: 0.9rem; font-weight: normal; color: gray;'>({sub.get('code', 'Sem código')})</span></h3>"
                                f"</div>",
                                unsafe_allow_html=True
                            )
                            c1, c2, c3 = st.columns(3)
                            c1.markdown(f"**Professor(a):** {sub.get('professor') or 'Não informado'}")
                            c2.markdown(f"**Semestre:** {sub.get('semester') or 'Não informado'}")
                            c3.markdown(f"**Status:** {status_text}")

                        with col_actions:
                            st.write("")
                            # Expander para edição
                            with st.popover("✏️ Editar", use_container_width=True):
                                st.markdown(f"**Editar: {sub['name']}**")
                                edit_name = st.text_input("Nome da Disciplina*", value=sub["name"], key=f"edit_name_{sub_id}")
                                edit_code = st.text_input("Código", value=sub.get("code", ""), key=f"edit_code_{sub_id}")
                                edit_prof = st.text_input("Professor(a)", value=sub.get("professor", ""), key=f"edit_prof_{sub_id}")
                                edit_sem = st.text_input("Semestre / Período", value=sub.get("semester", ""), key=f"edit_sem_{sub_id}")
                                edit_color = st.color_picker("Cor de Identificação", value=color, key=f"edit_color_{sub_id}")

                                current_status_pt = REVERSE_STATUS.get(sub.get("status", "active"), "Ativa")
                                edit_status_pt = st.selectbox(
                                    "Status",
                                    ["Ativa", "Concluída", "Arquivada"],
                                    index=["Ativa", "Concluída", "Arquivada"].index(current_status_pt),
                                    key=f"edit_status_{sub_id}"
                                )

                                if st.button("Salvar Alterações", key=f"btn_save_{sub_id}", type="primary"):
                                    if not edit_name.strip():
                                        st.error("O nome da matéria não pode ficar vazio.")
                                    else:
                                        update_subject(
                                            subject_id=sub_id,
                                            name=edit_name,
                                            code=edit_code,
                                            professor=edit_prof,
                                            semester=edit_sem,
                                            color=edit_color,
                                            status=STATUS_OPTIONS[edit_status_pt]
                                        )
                                        st.success("Disciplina atualizada com sucesso!")
                                        st.rerun()

                            # Botão de Exclusão
                            with st.popover("🗑️ Excluir", use_container_width=True):
                                st.write(f"Tem certeza que deseja excluir **{sub['name']}**?")
                                if st.button("Confirmar Exclusão", key=f"btn_del_{sub_id}", type="primary"):
                                    delete_subject(sub_id)
                                    st.success(f"Disciplina '{sub['name']}' removida com sucesso!")
                                    st.rerun()

    # --- ABA 2: CADASTRO DE NOVA DISCIPLINA ---
    with tab_create:
        st.subheader("Nova Disciplina")
        st.write("Preencha as informações para registrar uma matéria no EduTrack AI.")

        with st.form("form_create_subject", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                name_input = st.text_input("Nome da Disciplina *", placeholder="Ex: Algoritmos e Estruturas de Dados")
                professor_input = st.text_input("Professor(a)", placeholder="Ex: Dr. Alan Turing")
                color_input = st.color_picker("Cor da Etiqueta", value="#4F46E5")

            with col_b:
                code_input = st.text_input("Código da Matéria", placeholder="Ex: CC-201")
                semester_input = st.text_input("Semestre / Período", placeholder="Ex: 2026.1")
                status_choice = st.selectbox("Status Inicial", ["Ativa", "Concluída", "Arquivada"], index=0)

            submitted = st.form_submit_button("Cadastrar Disciplina", type="primary", use_container_width=True)

            if submitted:
                if not name_input.strip():
                    st.error("⚠️ O nome da disciplina é obrigatório. Por favor, preencha o campo para continuar.")
                else:
                    new_sub = create_subject(
                        name=name_input,
                        code=code_input,
                        professor=professor_input,
                        semester=semester_input,
                        color=color_input,
                        status=STATUS_OPTIONS[status_choice]
                    )
                    st.success(f"🎉 Disciplina **{new_sub['name']}** cadastrada com sucesso!")
                    st.rerun()

# ==========================================
# 3. TAREFAS
# ==========================================
elif menu_option == "Tarefas":
    st.title("📝 Gerenciamento de Tarefas")
    st.write("Acompanhe entregas, trabalhos e atividades acadêmicas.")
    st.info("Dica: Em breve você poderá associar suas tarefas diretamente às disciplinas cadastradas!")
    st.checkbox("Exemplo: Estudar conteúdo da semana de Inteligência Artificial")
    st.checkbox("Exemplo: Entregar relatório de Engenharia de Software")