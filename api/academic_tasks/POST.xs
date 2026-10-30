// Criar uma nova tarefa acadêmica vinculada à disciplina e ao usuário autenticado
query "academic_tasks" verb=POST {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    text title filters=trim
    text? description filters=trim
    timestamp? due_date
    text? status filters=trim
    int subject_id
  }

  stack {
    // Validar se a disciplina informada pertence ao usuário autenticado via consulta por id e user_id
    db.query subjects {
      where = ($db.subjects.id == $input.subject_id) && ($db.subjects.user_id == $auth.id)
      return = {type: "single"}
    } as $subject

    precondition ($subject != null) {
      error_type = "accessdenied"
      error = "Acesso negado: a disciplina selecionada não pertence ao seu usuário."
    }

    db.add academic_tasks {
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : ($input.status ?? "pending")
        subject_id : $input.subject_id
        user_id    : $auth.id
      }
    } as $new_task
  }

  response = $new_task
  tags = ["edutrack:academic"]
  guid = "u4pCiAYB5aKwpZQNUmHJzvf7RJ8"
}
