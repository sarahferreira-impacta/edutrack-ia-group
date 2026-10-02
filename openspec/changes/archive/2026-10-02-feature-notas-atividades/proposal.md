## Why

No EduTrack AI, professores precisam registrar e acompanhar as notas dos alunos em avaliações e tarefas específicas de suas disciplinas. Atualmente, a plataforma suporta autenticação e dados de disciplinas, mas não possui estrutura de backend para o lançamento de notas por atividade. Esta funcionalidade viabiliza o controle de notas, avaliação contínua do aprendizado e histórico de desempenho do estudante.

## What Changes

- **Esquema de Dados para Atividades**: Definição da tabela `activity` (`table/activity.xs`) contendo `id`, `created_at`, `subject_id` (FK para disciplina), `title`, `description` e `max_score` (valor máximo da atividade).
- **Esquema de Dados para Notas**: Definição da tabela `activity_grade` (`table/activity_grade.xs`) contendo `id`, `created_at`, `activity_id` (FK para atividade), `student_id` (FK para `user`), `score` (nota obtida), `feedback` (comentários do professor) e `graded_by` (FK para `user` do professor).
- **APIs de Lançamento e Consulta de Notas**: Criação de endpoints no Xano para:
  - `POST /grade`: Lançamento ou atualização de nota de um aluno em determinada atividade pelo professor autenticado.
  - `GET /grade/activity/{activity_id}`: Consulta de notas de todos os alunos em uma atividade específica.
  - `GET /grade/student/{student_id}`: Consulta das notas atribuídas a um aluno específico.

## Capabilities

### New Capabilities
- `grades`: Gerenciamento e lançamento de notas de atividades acadêmicas por professores para alunos.

### Modified Capabilities
<!-- Nenhuma capacidade existente teve seus requisitos alterados -->

## Impact

- **Banco de Dados (Xano .xs)**: Criação dos esquemas `table/activity.xs` e `table/activity_grade.xs`.
- **APIs (Xano .xs)**: Novos endpoints sob o grupo de API `api/grades/`.
- **Contratos e Permissões**: Apenas professores e administradores autorizados poderão lançar ou modificar notas.
