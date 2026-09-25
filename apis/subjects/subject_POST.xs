// Create a new academic subject
query "subject" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text? code filters=trim
    text? professor filters=trim
    text? semester filters=trim
    text? color filters=trim
    enum status? {
      values = ["active", "completed", "archived"]
    }
  }

  stack {
    db.add subject {
      data = {
        user_id  : $auth.id
        name     : $input.name
        code     : $input.code
        professor: $input.professor
        semester : $input.semester
        color    : $input.color
        status   : ($input.status ?? "active")
      }
    } as $new_subject
  }

  response = $new_subject
  tags = ["edutrack:academic"]
}
