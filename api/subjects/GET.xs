// Listar todas as disciplinas pertencentes ao usuário autenticado
query "subjects" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $user_subjects
  }

  response = $user_subjects
  tags = ["edutrack:academic"]
  guid = "HJ6zw42PGMWecWyl3SQIl-Xi1IU"
}

