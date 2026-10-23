# academic-tasks Specification

## Purpose

Define os requisitos de integração entre o frontend Streamlit da página de Tarefas e os endpoints RESTful de `academic_tasks` e `subjects` do backend Xano no EduTrack AI.

## ADDED Requirements

### Requirement: Tarefas Page Listing and Subject Mapping Integration
The system SHALL retrieve academic tasks from `GET /academic_tasks` and resolve each task's `subject_id` to its corresponding subject name loaded from `GET /subjects`, displaying the actual records in the "Tarefas" page.

#### Scenario: Displaying tasks with resolved subject names
- **WHEN** an authenticated user opens the "Tarefas" page
- **THEN** the system MUST retrieve tasks from `GET /academic_tasks`, load available subjects from `GET /subjects` to resolve each task's `subject_id`, and render the tasks preserving the existing expander visual structure

#### Scenario: Empty tasks state
- **WHEN** no tasks are returned from the backend for the authenticated user
- **THEN** the system MUST display an informative notice indicating that no tasks were found

#### Scenario: Error handling during tasks loading
- **WHEN** the backend request to `GET /academic_tasks` or `GET /subjects` fails
- **THEN** the system MUST display an error message and maintain the page layout without raising unhandled exceptions

### Requirement: Tarefas Page Filtering and Search Integration
The system SHALL apply textual search and status filtering directly to the tasks retrieved from the backend.

#### Scenario: Filtering tasks by status
- **WHEN** the user selects a status filter option such as "Pendente" or "Concluída"
- **THEN** the system MUST filter the displayed task list matching the corresponding status value

#### Scenario: Searching tasks by title
- **WHEN** the user inputs search text into the task search field
- **THEN** the system MUST filter the displayed tasks showing only records where the title matches the query text (case-insensitive)

