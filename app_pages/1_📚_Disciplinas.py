import streamlit as st

from services.subject_service import (
    create_subject_in_xano,
    delete_subject_in_xano,
    fetch_subjects_from_xano,
    get_auth_token,
    update_subject_in_xano,
)
from services.task_service import fetch_tasks_from_xano

st.set_page_config(page_title="Disciplinas", page_icon="📚")

if not get_auth_token():
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login na página de perfil para continuar.")
    st.stop()


st.title("📚 Gestão de Disciplinas")

subjects = fetch_subjects_from_xano() if get_auth_token() else []
tasks = fetch_tasks_from_xano(user_subjects=subjects) if subjects else []

list_tab, create_tab = st.tabs(["📋 Minhas Disciplinas", "➕ Nova Disciplina"])

with create_tab:
    with st.form("form_new_subject", clear_on_submit=True):
        name = st.text_input("Nome da disciplina")
        teacher = st.text_input("Professor")
        hours = st.number_input("Quantidade de horas", min_value=0, step=1, value=0)
        submitted = st.form_submit_button("Cadastrar disciplina", type="primary")

        if submitted:
            if not name.strip():
                st.error("O nome da disciplina é obrigatório.")
            else:
                try:
                    created = create_subject_in_xano(name=name, teacher=teacher, hours=int(hours))
                    st.success(f"Disciplina {created.get('name') or name} cadastrada com sucesso!")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

with list_tab:
    if not subjects:
        st.info("Nenhuma disciplina foi encontrada para este usuário.")
    else:
        for subject in subjects:
            subject_id = subject.get("id")
            if subject_id is None:
                continue
            related_tasks = [task for task in tasks if str(task.get("subject_id")) == str(subject_id)]
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    teacher_name = subject.get("teacher") or subject.get("professor") or "Não informado"
                    hours_value = subject.get("hours") if subject.get("hours") is not None else 0
                    st.markdown(f"**{subject.get('name') or 'Sem nome'}**")
                    st.caption(f"Professor: {teacher_name}")
                    st.caption(f"Horas: {hours_value}")
                    st.caption(f"Tarefas vinculadas: {len(related_tasks)}")
                with col2:
                    with st.popover("✏️ Editar", use_container_width=True):
                        with st.form(f"edit_subject_form_{subject_id}"):
                            edited_name = st.text_input("Nome", value=subject.get("name") or "", key=f"subject_name_{subject_id}")
                            edited_teacher = st.text_input("Professor", value=subject.get("teacher") or subject.get("professor") or "", key=f"subject_teacher_{subject_id}")
                            edited_hours = st.number_input("Horas", min_value=0, value=int(subject.get("hours") if subject.get("hours") is not None else 0), step=1, key=f"subject_hours_{subject_id}")
                            if st.form_submit_button("Salvar alterações", type="primary"):
                                try:
                                    update_subject_in_xano(subject_id, name=edited_name, teacher=edited_teacher, hours=int(edited_hours))
                                    st.success("Disciplina atualizada com sucesso!")
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Não foi possível atualizar a disciplina: {exc}")
                    with st.popover("🗑️ Excluir", use_container_width=True):
                        st.warning(f"Deseja excluir a disciplina '{subject.get('name') or 'Sem nome'}'?")
                        if related_tasks:
                            st.warning("Esta disciplina possui tarefas associadas. Não será possível excluir automaticamente registros relacionados.")
                        if st.button("Confirmar exclusão", key=f"delete_subject_confirm_{subject_id}", type="secondary"):
                            if related_tasks:
                                st.error("A exclusão foi bloqueada porque existem tarefas vinculadas a esta disciplina.")
                            else:
                                try:
                                    delete_subject_in_xano(subject_id)
                                    st.success("Disciplina excluída com sucesso!")
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Não foi possível excluir a disciplina: {exc}")
