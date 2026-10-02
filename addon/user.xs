addon user {
  input {
    int user_id? {
      table = "user"
    }
  }

  stack {
    db.query user {
      where = $db.user.id == $input.user_id
      return = {type: "single"}
    }
  }

  guid = "McOB0wyFnwEaDVQb4pI0uqX4tJE"
}