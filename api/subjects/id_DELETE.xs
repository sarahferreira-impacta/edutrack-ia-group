// Deletar uma disciplina com validação de usuário
query "subjects/{id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
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

    db.del subjects {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success   : true
    deleted_id: $input.id
  }
  tags = ["edutrack:academic"]
  guid = "fDbGI9_zQNvF0xhSgOYOAKMZPBQ"
}

