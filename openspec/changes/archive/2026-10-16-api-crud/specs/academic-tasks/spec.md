# academic-tasks Specification

## ADDED Requirements

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

