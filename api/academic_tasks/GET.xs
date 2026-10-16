// Listar todas as tarefas acadêmicas pertencentes ao usuário autenticado
query "academic_tasks" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int? subject_id
  }

  stack {
    db.query academic_tasks {
      where = ($db.academic_tasks.user_id == $auth.id) && ($input.subject_id == null || $db.academic_tasks.subject_id == $input.subject_id)
      return = {type: "list"}
    } as $user_tasks
  }

  response = $user_tasks
  tags = ["edutrack:academic"]
  guid = "mSuiHMvtPN3lgbh4KwdWkD9FPCo"
}

