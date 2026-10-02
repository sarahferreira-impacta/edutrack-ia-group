// List all subjects for the authenticated user
query "subject" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subject {
      where = $db.subject.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  tags = ["edutrack:academic"]
}
