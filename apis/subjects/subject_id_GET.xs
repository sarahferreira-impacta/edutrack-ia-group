// Get a subject by ID
query "subject/{id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get subject {
      field_name = "id"
      field_value = $input.id
    } as $subject

    // Verify ownership
    precondition ($subject.user_id == $auth.id) {
      error_type = "forbidden"
      error_message = "Access denied"
    }
  }

  response = $subject
  tags = ["edutrack:academic"]
}
