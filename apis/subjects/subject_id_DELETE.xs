// Delete a subject by ID
query "subject/{id}" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
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

    db.delete subject {
      field_name = "id"
      field_value = $input.id
    } as $deleted_subject
  }

  response = {success: true}
  tags = ["edutrack:academic"]
}
