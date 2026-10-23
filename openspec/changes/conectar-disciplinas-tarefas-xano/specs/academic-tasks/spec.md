# academic-tasks Specification

## Purpose

Define os requisitos de consulta e exibição de dados reais de tarefas na página de Tarefas do EduTrack AI a partir do endpoint GET do Xano.

## ADDED Requirements

### Requirement: Real Academic Tasks Listing in Tarefas Page
The system SHALL query the Xano endpoint `GET https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks` and render the retrieved tasks in the "Tarefas" page without static mockup data.

#### Scenario: Displaying real tasks
- **WHEN** the user opens the "Tarefas" page
- **THEN** the system MUST retrieve tasks from the GET endpoint and display each record using the existing expander card layout

#### Scenario: Empty state handling
- **WHEN** the Xano GET endpoint returns an empty collection of tasks
- **THEN** the system MUST display an informative notice indicating that no tasks are registered

#### Scenario: Network or invalid response error handling
- **WHEN** the request to the Xano GET endpoint fails or returns an error status code
- **THEN** the system MUST display a clear error message to the user without breaking the page layout

### Requirement: Task Search and Status Filter on Real Data
The system SHALL apply textual search and status filtering directly to the task data loaded from the Xano GET endpoint.

#### Scenario: Filtering tasks by status
- **WHEN** the user selects a status option from the filter dropdown
- **THEN** the system MUST filter the rendered tasks matching the selected status

#### Scenario: Searching tasks by title
- **WHEN** the user inputs a search string into the search field
- **THEN** the system MUST filter the rendered tasks showing only records where the title matches the search query (case-insensitive)

