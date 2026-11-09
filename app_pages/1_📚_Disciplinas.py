import streamlit as st

from services.subject_service import (
    create_subject_in_xano,
    delete_subject_in_xano,
    fetch_subjects_from_xano,
    get_auth_token,
    update_subject_in_xano,
)
from services.task_service import fetch_tasks_from_xano
from styles.theme import inject_css

st.set_page_config(page_title="Disciplinas", page_icon="📚")
inject_css()

if not get_auth_token():
    st.warning("Você precisa estar logado para acessar esta página.")
    st.info("Faça login na página de perfil para continuar.")
    st.stop()


st.markdown(
    "<h1 style='color:#0C1E33;font-size:1.75rem;font-weight:800;margin-bottom:0.25rem;'>"
    "🎓 Disciplinas</h1>",
    unsafe_allow_html=True,
)

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
        COLS = 2
        rows = [subjects[i:i+COLS] for i in range(0, len(subjects), COLS)]
        for row in rows:
            cols_ui = st.columns(COLS)
            for idx, subject in enumerate(row):
                subject_id = subject.get("id")
                if subject_id is None:
                    continue
                related_tasks = [task for task in tasks if str(task.get("subject_id")) == str(subject_id)]
                teacher_name = subject.get("teacher") or subject.get("professor") or "Não informado"
                hours_value = subject.get("hours") if subject.get("hours") is not None else 0
                with cols_ui[idx]:
                    with st.container(border=True):
                        st.markdown(
                            f"<p style='color:#0C1E33;font-weight:700;font-size:1rem;margin:0 0 8px 0;'>"
                            f"{subject.get('name') or 'Sem nome'}</p>",
                            unsafe_allow_html=True,
                        )
                        st.caption(f"👤 {teacher_name}")
                        st.caption(f"⏱️ {hours_value} horas")
                        st.caption(f"📝 Tarefas vinculadas: {len(related_tasks)}")
                        col_edit, col_del = st.columns(2)
                        edit_sub_key = f"edit_sub_{subject_id}"
                        del_sub_key = f"del_sub_{subject_id}"
                        if edit_sub_key not in st.session_state:
                            st.session_state[edit_sub_key] = False
                        if del_sub_key not in st.session_state:
                            st.session_state[del_sub_key] = False

                        with col_edit:
                            if st.button("✏️ Editar", key=f"btn_edit_sub_{subject_id}", use_container_width=True):
                                st.session_state[edit_sub_key] = not st.session_state[edit_sub_key]
                                st.session_state[del_sub_key] = False
                                st.rerun()
                        with col_del:
                            if st.button("🗑️ Excluir", key=f"btn_del_sub_{subject_id}", use_container_width=True):
                                st.session_state[del_sub_key] = not st.session_state[del_sub_key]
                                st.session_state[edit_sub_key] = False
                                st.rerun()

                        if st.session_state.get(edit_sub_key):
                            with st.form(f"edit_subject_form_{subject_id}"):
                                edited_name = st.text_input("Nome", value=subject.get("name") or "", key=f"subject_name_{subject_id}")
                                edited_teacher = st.text_input("Professor", value=subject.get("teacher") or subject.get("professor") or "", key=f"subject_teacher_{subject_id}")
                                edited_hours = st.number_input("Horas", min_value=0, value=int(subject.get("hours") if subject.get("hours") is not None else 0), step=1, key=f"subject_hours_{subject_id}")
                                c_save, c_cancel = st.columns(2)
                                with c_save:
                                    sub_save = st.form_submit_button("Salvar alterações", type="primary", use_container_width=True)
                                with c_cancel:
                                    sub_cancel = st.form_submit_button("Cancelar", type="secondary", use_container_width=True)
                                if sub_cancel:
                                    st.session_state[edit_sub_key] = False
                                    st.rerun()
                                if sub_save:
                                    try:
                                        update_subject_in_xano(subject_id, name=edited_name, teacher=edited_teacher, hours=int(edited_hours))
                                        st.session_state[edit_sub_key] = False
                                        st.success("Disciplina atualizada com sucesso!")
                                        st.rerun()
                                    except Exception as exc:
                                        st.error(f"Não foi possível atualizar a disciplina: {exc}")

                        if st.session_state.get(del_sub_key):
                            st.warning(f"Deseja excluir a disciplina '{subject.get('name') or 'Sem nome'}'?")
                            if related_tasks:
                                st.warning("Esta disciplina possui tarefas associadas. Não será possível excluir automaticamente registros relacionados.")
                            cd1, cd2 = st.columns(2)
                            with cd1:
                                if st.button("Confirmar exclusão", key=f"delete_subject_confirm_{subject_id}", type="secondary", use_container_width=True):
                                    if related_tasks:
                                        st.error("A exclusão foi bloqueada porque existem tarefas vinculadas a esta disciplina.")
                                    else:
                                        try:
                                            delete_subject_in_xano(subject_id)
                                            st.session_state[del_sub_key] = False
                                            st.success("Disciplina excluída com sucesso!")
                                            st.rerun()
                                        except Exception as exc:
                                            st.error(f"Não foi possível excluir a disciplina: {exc}")
                            with cd2:
                                if st.button("Cancelar", key=f"cancel_del_sub_{subject_id}", use_container_width=True):
                                    st.session_state[del_sub_key] = False
                                    st.rerun()
