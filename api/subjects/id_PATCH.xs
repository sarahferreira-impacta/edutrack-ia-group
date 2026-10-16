// Atualizar dados de uma disciplina existente com validação de usuário
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
    text? name filters=trim
    text? teacher filters=trim
    int? hours filters=min:0
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $existing_subject

    precondition ($existing_subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: esta disciplina pertence a outro usuário."
    }

    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        name   : ($input.name ?? $existing_subject.name)
        teacher: ($input.teacher ?? $existing_subject.teacher)
        hours  : ($input.hours ?? $existing_subject.hours)
      }
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["edutrack:academic"]
  guid = "QolWOTJILDn7kQ6lB2ywfXpNZMg"
}

