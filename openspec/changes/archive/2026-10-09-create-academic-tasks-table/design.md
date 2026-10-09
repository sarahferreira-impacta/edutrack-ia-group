## Context

Consulte `proposal.md` para a motivação. O EduTrack AI já possui as tabelas `subjects` (`table/subjects.xs`) e `user` (`table/user.xs`). Esta alteração define a estrutura da tabela `academic_tasks` para armazenar as atividades acadêmicas dos estudantes vinculadas às disciplinas.

## Goals / Non-Goals

**Goals:**
- Definir o esquema da tabela `academic_tasks` em `table/academic_tasks.xs` em conformidade com o padrão XanoScript do projeto.
- Configurar os campos solicitados: `title` (text), `description` (text), `due_date` (date/timestamp), `status` (text), `subject_id` (FK para `subjects`), além dos campos estruturais `id`, `created_at` e `user_id` (FK para `user`).
- Estabelecer índices para chave primária (`id`) e buscas relacionais (`subject_id`, `user_id`).

**Non-Goals:**
- Não criar APIs CRUD neste momento (em cumprimento estrito à **Regra nº 1 do `AGENTS.md`**: "Se o usuário pedir 'criar tabela X', NÃO adicione automaticamente: API CRUD, testes, ou frontend").
- Não implementar interface ou componentes de frontend.
- Não incluir suítes de testes automatizados não solicitadas.

## Decisions

### Decisão 1: Estrutura da Tabela em `table/academic_tasks.xs`
- **Abordagem**: Criar o arquivo no diretório padrão `table/` com a seguinte modelagem:
  ```xs
  // Tabela de tarefas e obrigações acadêmicas vinculadas a disciplinas
  table academic_tasks {
    auth = false

    schema {
      int id
      text title filters=trim
      text? description filters=trim
      timestamp? due_date
      text status?="pending" filters=trim
      int subject_id {
        table = "subjects"
      }
      int user_id {
        table = "user"
      }
      timestamp created_at?=now
    }

    index = [
      {type: "primary", field: [{name: "id"}]}
      {type: "btree", field: [{name: "subject_id", op: "asc"}]}
      {type: "btree", field: [{name: "user_id", op: "asc"}]}
    ]
  }
  ```
- **Racional**: Segue exatamente o padrão estabelecido em `table/subjects.xs` e cumpre os requisitos do projeto e as convenções do XanoScript.

### Decisão 2: Vínculo com Usuário e Disciplina
- **Abordagem**: Utilizar `subject_id` apontando para a tabela `subjects` e `user_id` apontando para a tabela `user`.
- **Racional**: Garante a integridade referencial com as disciplinas existentes e permite filtrar tarefas do aluno autenticado.

## Risks / Trade-offs

- **[Risk]** Remoção de disciplina em cascata deixando tarefas órfãs.  
  → **Mitigation**: A integridade referencial declarada no Xano assegura a consistência das relações.

