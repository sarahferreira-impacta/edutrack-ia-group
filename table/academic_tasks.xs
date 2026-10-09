// Tabela de tarefas e obrigações acadêmicas vinculadas a disciplinas
table academic_tasks {
  auth = false

  schema {
    // Identificador único da tarefa
    int id

    // Título da tarefa acadêmica (prova, trabalho, lição)
    text title filters=trim

    // Descrição detalhada da atividade
    text? description filters=trim

    // Prazo de entrega ou data da avaliação
    timestamp? due_date

    // Status atual da tarefa (ex: "pending", "in_progress", "completed")
    text status?="pending" filters=trim

    // Referência para a disciplina correspondente
    int subject_id {
      table = "subjects"
    }

    // Referência para o estudante proprietário da tarefa
    int user_id {
      table = "user"
    }

    // Data e hora de criação do registro
    timestamp created_at?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
  ]
  guid = "UsKo8RbFUZ2YUASF--DBEMOvQaU"
}

