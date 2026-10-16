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
    // Validar se a disciplina informada pertence ao usuário autenticado
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject.user_id == $auth.id) {
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

