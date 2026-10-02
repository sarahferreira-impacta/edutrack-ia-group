// Update a subject by ID
query "subject/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
    text? name filters=trim
    text? code filters=trim
    text? professor filters=trim
    text? semester filters=trim
    text? color filters=trim
    enum status? {
      values = ["active", "completed", "archived"]
    }
  }

  stack {
    db.get subject {
      field_name = "id"
      field_value = $input.id
    } as $existing_subject

    precondition ($existing_subject.user_id == $auth.id) {
      error_type = "forbidden"
      error_message = "Access denied"
    }

    db.edit subject {
      field_name = "id"
      field_value = $input.id
      data = {
        name     : ($input.name ?? $existing_subject.name)
        code     : ($input.code ?? $existing_subject.code)
        professor: ($input.professor ?? $existing_subject.professor)
        semester : ($input.semester ?? $existing_subject.semester)
        color    : ($input.color ?? $existing_subject.color)
        status   : ($input.status ?? $existing_subject.status)
      }
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["edutrack:academic"]
}
