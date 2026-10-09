## Why

No EduTrack AI, os alunos precisam registrar e gerenciar suas obrigações acadêmicas (lições de casa, provas, trabalhos e projetos) diretamente vinculadas a cada disciplina cursada. Atualmente, o sistema conta com a tabela de disciplinas (`subjects`), mas necessita da estrutura de dados para armazenar e organizar essas tarefas no backend.

## What Changes

- **Esquema de Tabela `academic_tasks`**: Definir a tabela no Xano (`table/academic_tasks.xs`) contendo os campos:
  - `id` (int, chave primária autoincremento);
  - `created_at` (timestamp, criação do registro);
  - `title` (text, título da tarefa);
  - `description` (text, descrição detalhada da obrigação acadêmica);
  - `due_date` (date/timestamp, data de entrega/realização);
  - `status` (text, estado da tarefa como "pending", "completed");
  - `subject_id` (int, chave estrangeira referenciando a tabela `subjects`);
  - `user_id` (int, vínculo com o usuário autenticado da tabela `user`).

## Capabilities

### New Capabilities
- `academic-tasks`: Definição e armazenamento das tarefas e obrigações acadêmicas vinculadas a disciplinas no EduTrack AI.

### Modified Capabilities
<!-- Nenhuma capacidade existente teve seus requisitos modificados -->

## Impact

- **Banco de Dados (Xano .xs)**: Criação do arquivo de esquema `table/academic_tasks.xs`.

