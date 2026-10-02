## Context

Consulte `proposal.md` para motivação e objetivos. O EduTrack AI já possui tabelas de usuários e disciplinas estruturadas na pasta `table/` e grupos de API em `api/`. Para que o professor possa lançar notas por atividade, é necessário estruturar a entidade de atividades avaliativas e o lançamento de notas associado ao aluno e ao professor.

## Goals / Non-Goals

**Goals:**
- Definir o modelo de dados Xano para atividades (`table/activity.xs`) e notas (`table/activity_grade.xs`).
- Definir as rotas e regras de negócio de backend em Xano sob `api/grades/` para lançamento de notas com validação de valor máximo e consultas por atividade e por aluno.
- Assegurar rastreabilidade com o professor que realizou o lançamento (`graded_by`).

**Non-Goals:**
- Implementação de telas de interface gráfica / frontend (escopo restrito estritamente ao backend e schema solicitados, conforme `AGENTS.md`).
- Correção automatizada de redação ou de código via IA (escopo de fases futuras).
- Cálculo de ponderação complexa de média final do curso.

## Decisions

### Decisão 1: Modelo Relacional entre Atividade e Nota
- **Abordagem**: Separar a atividade avaliativa (`activity`) do lançamento da nota (`activity_grade`).
  - `table/activity.xs`: `id`, `created_at`, `subject_id` (FK para disciplina), `title`, `description`, `max_score` (numérico decimal/int).
  - `table/activity_grade.xs`: `id`, `created_at`, `activity_id` (FK `activity`), `student_id` (FK `user`), `score` (decimal), `feedback` (text), `graded_by` (FK `user`).
- **Racional**: Permite que uma mesma atividade tenha notas lançadas individualmente para múltiplos alunos, mantendo o histórico e os critérios da avaliação desacoplados da entrega de cada estudante.

### Decisão 2: Mecanismo de Upsert na API de Lançamento de Nota
- **Abordagem**: O endpoint `POST /grade` verifica se já existe uma nota registrada para o par `(activity_id, student_id)`. Se existir, atualiza o registro (`score`, `feedback`, `graded_by`); caso contrário, insere um novo registro.
- **Racional**: Evita duplicidade de notas para o mesmo aluno na mesma atividade e simplifica o fluxo para o professor ao corrigir ou revisar uma avaliação já submetida.

### Decisão 3: Validação de Faixa de Nota
- **Abordagem**: Pré-condição na rota Xano garantindo que `score >= 0` e `score <= activity.max_score`.
- **Racional**: Garante a integridade pedagógica dos dados lançados.

## Risks / Trade-offs

- **[Risk]** Lançamento de nota para aluno que não pertença à turma da disciplina.  
  → **Mitigation**: A validação na API pode checar o vínculo do aluno com a disciplina da atividade.

- **[Risk]** Usuário com perfil de aluno tentando lançar notas.  
  → **Mitigation**: Adicionar pré-condição de autorização no endpoint verificando a role do usuário ou chamada ao helper `enforce_role`.
