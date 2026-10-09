# academic-tasks Specification

## Purpose

Define a estrutura de dados da tabela de tarefas acadêmicas (academic_tasks), permitindo que os estudantes gerenciem obrigações associadas a suas disciplinas no EduTrack AI.

## ADDED Requirements

### Requirement: Academic Tasks Table Schema
The system SHALL define the `academic_tasks` table schema with the following fields:
- `id`: integer primary key with auto-increment;
- `created_at`: timestamp of creation;
- `title`: text (trimmed);
- `description`: text (optional, trimmed);
- `due_date`: date or timestamp for completion deadline;
- `status`: text indicating task state;
- `subject_id`: integer foreign key referencing the `subjects` table;
- `user_id`: integer foreign key referencing the `user` table.

#### Scenario: Valid schema declaration
- **WHEN** the backend schema is parsed or deployed
- **THEN** the system MUST recognize `id`, `title`, `description`, `due_date`, `status`, `subject_id`, and `user_id` with their respective data types and constraints

### Requirement: Subject and User Association
The system SHALL enforce relational association between each academic task, its parent subject in `subjects`, and the owner in `user`.

#### Scenario: Linking task to subject and user
- **WHEN** an academic task is created with a valid `subject_id` and `user_id`
- **THEN** the system MUST persist the task linked to the corresponding subject and user

