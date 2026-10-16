# academic-tasks Specification

## Purpose

Define a estrutura de dados da tabela de tarefas acadêmicas (academic_tasks), permitindo que os estudantes gerenciem obrigações associadas a suas disciplinas no EduTrack AI.

## Requirements

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

### Requirement: Academic Tasks CRUD APIs with User Isolation
The system SHALL provide RESTful endpoints (`POST /academic_tasks`, `GET /academic_tasks`, `GET /academic_tasks/{id}`, `PATCH /academic_tasks/{id}`, `DELETE /academic_tasks/{id}`) requiring user authentication and enforcing that users only access and modify their own task records.

#### Scenario: Listing only owned academic tasks
- **WHEN** an authenticated user sends a `GET /academic_tasks` request
- **THEN** the system MUST return only the academic tasks matching the authenticated user's `user_id`

#### Scenario: Creating a task with user ownership
- **WHEN** an authenticated user submits valid task data to `POST /academic_tasks`
- **THEN** the system MUST persist the task record with `user_id` bound to the authenticated user

#### Scenario: Unauthorized access to another user's task
- **WHEN** an authenticated user attempts to read, update, or delete an academic task belonging to another user
- **THEN** the system MUST deny access and return an authorization error
