# subjects Specification

## Purpose

Define os requisitos dos endpoints RESTful de CRUD para gerenciamento de disciplinas acadêmicas com isolamento de dados por usuário no EduTrack AI.

## ADDED Requirements

### Requirement: Subjects CRUD APIs with User Isolation
The system SHALL provide RESTful endpoints (`POST /subjects`, `GET /subjects`, `GET /subjects/{id}`, `PATCH /subjects/{id}`, `DELETE /subjects/{id}`) requiring user authentication and enforcing that users only access and modify their own subject records.

#### Scenario: Listing only owned subjects
- **WHEN** an authenticated user sends a `GET /subjects` request
- **THEN** the system MUST return only the subjects matching the authenticated user's `user_id`

#### Scenario: Creating a subject with user ownership
- **WHEN** an authenticated user submits valid subject data to `POST /subjects`
- **THEN** the system MUST persist the subject record with `user_id` bound to the authenticated user

#### Scenario: Unauthorized access to another user's subject
- **WHEN** an authenticated user attempts to read, update, or delete a subject record belonging to another user
- **THEN** the system MUST deny access and return an authorization error

