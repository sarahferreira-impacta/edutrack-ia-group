# activity-grades Specification

## Purpose

Define as regras e requisitos para que professores possam lançar notas de alunos em atividades acadêmicas específicas no EduTrack AI.

## ADDED Requirements

### Requirement: Record Student Grade for Activity
The system SHALL allow an authenticated instructor to submit a grade for a student in a specific academic activity.

#### Scenario: Successful grade submission
- **WHEN** the instructor submits a valid score, student identifier, and activity identifier to the grade submission endpoint
- **THEN** the system MUST save the grade record in the database linked to the activity and student and return confirmation

#### Scenario: Missing required parameters
- **WHEN** the instructor attempts to submit a grade without providing the score or student identifier
- **THEN** the system MUST reject the request and return a validation error
