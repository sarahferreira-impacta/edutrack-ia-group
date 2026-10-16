// Criar uma nova disciplina para o usuário autenticado
query "subjects" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text? teacher filters=trim
    int? hours filters=min:0
  }

  stack {
    db.add subjects {
      data = {
        name     : $input.name
        teacher  : $input.teacher
        hours    : $input.hours
        user_id  : $auth.id
      }
    } as $new_subject
  }

  response = $new_subject
  tags = ["edutrack:academic"]
  guid = "6aGYA073u7eKh9_zkXtGrD8-bL8"
}

