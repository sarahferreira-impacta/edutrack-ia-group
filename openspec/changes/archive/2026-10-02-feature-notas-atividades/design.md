## Context

Consulte `proposal.md` para motivação e objetivos. O EduTrack AI já possui tabelas de usuários e disciplinas no Xano. O objetivo desta mudança é viabilizar exclusivamente que o professor lance notas para alunos em atividades específicas.

## Goals / Non-Goals

**Goals:**
- Definir o esquema da tabela `activity_grades` em `table/activity_grades.xs` no formato XanoScript.
- Definir o endpoint `POST /activity_grades` em `api/activity_grades/` para inserção de notas por atividade e aluno.
- Garantir rastreabilidade associando o usuário do professor autenticado (`user_id`).

**Non-Goals:**
- Não criar APIs de consulta (GET), listagens ou relatórios analíticos, respeitando estritamente o escopo solicitado no `AGENTS.md`.
- Não implementar interfaces de frontend ou testes automatizados, conforme a Regra nº 1 do `AGENTS.md`.

## Decisions

### Decisão 1: Estrutura da Tabela `activity_grades`
- **Abordagem**: Criar `table/activity_grades.xs` com os campos:
  - `id` (int, autoincrement, primary key)
  - `created_at` (timestamp, default now)
  - `activity_id` (int, identificador da atividade)
  - `student_id` (int, FK para a tabela `user`)
  - `grade` (decimal/numeric, valor da nota)
  - `feedback` (text, opcional, comentários do professor)
  - `user_id` (int, FK para a tabela `user`, identificando o professor que lançou)
- **Racional**: Garante consistência relacional e rastreabilidade da avaliação.

### Decisão 2: Estrutura do Endpoint `POST /activity_grades`
- **Abordagem**: Criar o endpoint `POST` autenticado (`auth = "user"`) para persistir o registro da nota no banco de dados.
- **Racional**: Atende diretamente à ação de lançamento de nota solicitada pelo usuário.

## Risks / Trade-offs

- **[Risk]** Lançamento de nota duplicada para a mesma atividade e aluno.  
  → **Mitigation**: Configurar índice ou validação prévia na query Xano antes da inserção.

