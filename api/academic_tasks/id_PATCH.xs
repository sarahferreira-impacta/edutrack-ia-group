// Atualizar dados de uma tarefa acadêmica existente com validação de usuário
query "academic_tasks/{id}" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int id
    text? title filters=trim
    text? description filters=trim
    timestamp? due_date
    text? status filters=trim
    int? subject_id
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $existing_task

    // Validação de propriedade: apenas o dono da tarefa pode atualizá-la
    precondition ($existing_task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: esta tarefa pertence a outro usuário."
    }

    // Se a disciplina for alterada, validar que a nova disciplina pertence ao usuário
    conditional {
      if ($input.subject_id != null) {
        db.get subjects {
          field_name = "id"
          field_value = $input.subject_id
        } as $subject

        precondition ($subject.user_id == $auth.id) {
          error_type = "accessdenied"
          error = "Acesso negado: a disciplina selecionada não pertence ao seu usuário."
        }
      }
    }

    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        title      : ($input.title ?? $existing_task.title)
        description: ($input.description ?? $existing_task.description)
        due_date   : ($input.due_date ?? $existing_task.due_date)
        status     : ($input.status ?? $existing_task.status)
        subject_id : ($input.subject_id ?? $existing_task.subject_id)
      }
    } as $updated_task
  }

  response = $updated_task
  tags = ["edutrack:academic"]
  guid = "TV8gMl31kTsTaD8HRl_wZgua5HI"
}

