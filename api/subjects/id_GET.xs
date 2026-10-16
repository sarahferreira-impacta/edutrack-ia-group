// Obter detalhes de uma disciplina específica com validação de usuário
query "subjects/{id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject

    // Validação de propriedade: usuário só pode ver sua própria disciplina
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Acesso negado: esta disciplina pertence a outro usuário."
    }
  }

  response = $subject
  tags = ["edutrack:academic"]
  guid = "BzxMfHq6L_MafdpHF0cwJyfbdoQ"
}

