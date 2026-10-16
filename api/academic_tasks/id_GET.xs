// Obter detalhes de uma tarefa acadêmica específica com validação de usuário
query "academic_tasks/{id}" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $task

    // Validação de propriedade: usuário só pode acessar sua própria tarefa
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: esta tarefa pertence a outro usuário."
    }
  }

  response = $task
  tags = ["edutrack:academic"]
  guid = "ZB_lVNs9OqO1tCML65YNugBSIeU"
}

