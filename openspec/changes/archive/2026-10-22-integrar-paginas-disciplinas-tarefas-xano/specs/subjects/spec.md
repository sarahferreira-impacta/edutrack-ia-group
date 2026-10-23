# subjects Specification

## Purpose

Define os requisitos de integração entre o frontend Streamlit da página de Disciplinas e os endpoints RESTful de `subjects` do backend Xano no EduTrack AI.

## ADDED Requirements

### Requirement: Disciplinas Page Listing Integration
The system SHALL retrieve academic subjects from the Xano backend via `GET /subjects` and render them in the "Disciplinas" page listing tab without static mockup data.

#### Scenario: Successful retrieval and display of subjects
- **WHEN** an authenticated user accesses the "Disciplinas" page ("Listar" tab)
- **THEN** the system MUST query `GET /subjects` and display the subjects returned by the backend preserving the existing card layout

#### Scenario: Empty subjects state
- **WHEN** the backend returns an empty list of subjects for the user
- **THEN** the system MUST display an informative message indicating that no subjects are currently registered

#### Scenario: Error handling during subjects loading
- **WHEN** the API request to `GET /subjects` fails or returns a network error
- **THEN** the system MUST display an error alert to the user and keep the page structure intact

### Requirement: Disciplinas Page Creation Integration
The system SHALL submit new subject records to the Xano backend via `POST /subjects` with form data entered in the "Nova Disciplina" tab.

#### Scenario: Successful creation of a new subject
- **WHEN** the user submits the subject creation form with a valid name
- **THEN** the system MUST send a `POST /subjects` request with `name` and optional `teacher`, display a success message upon completion, and update the listed subjects

#### Scenario: Validation on missing subject name
- **WHEN** the user attempts to submit the form without filling the required subject name
- **THEN** the system MUST block submission and display a validation warning without invoking the backend

