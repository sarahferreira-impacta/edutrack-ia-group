// Deletar uma tarefa acadêmica com validação de usuário
query "academic_tasks/{id}" verb=DELETE {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $existing_task

    // Validação de propriedade: apenas o dono da tarefa pode excluí-la
    precondition ($existing_task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: esta tarefa pertence a outro usuário."
    }

    db.del academic_tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success   : true
    deleted_id: $input.id
  }
  tags = ["edutrack:academic"]
  guid = "Z3kOe8W4jY98lQycLXZWG1dU9EM"
}

