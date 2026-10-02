## Purpose

Defines the Xano database schema for the subjects table, specifying the core fields including id, name, teacher, hours, and user_id foreign key relationship.

## ADDED Requirements

### Requirement: Subjects Table Schema Definition
The system SHALL define the `subjects` table schema containing the fields:
- `id`: integer, primary key, auto-incrementing.
- `created_at`: timestamp, default current time.
- `name`: text, trimmed, representing the subject or course title.
- `teacher`: text, trimmed, representing the instructor.
- `hours`: integer, representing the workload in hours.
- `user_id`: integer, foreign key referencing the authentication `user` table.

#### Scenario: Valid schema declaration
- **WHEN** the backend table schema is deployed or evaluated
- **THEN** the system MUST recognize `id`, `name`, `teacher`, `hours`, and `user_id` with their specified types and constraints

### Requirement: User Foreign Key Association
The system SHALL ensure that every subject record references a valid user in the Xano authentication table `user`.

#### Scenario: Linking subject to user
- **WHEN** a subject is stored in the database
- **THEN** the system MUST set `user_id` pointing to the authenticated student's record

### Requirement: Academic Workload Hours
The system SHALL support storing the total workload hours (`hours`) for each subject.

#### Scenario: Storing workload hours
- **WHEN** a user provides course workload hours as an integer
- **THEN** the system MUST persist and return the workload hours accurately
