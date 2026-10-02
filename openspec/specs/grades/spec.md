# grades Specification

## Purpose

Permite que professores lancem, atualizem e consultem notas e feedbacks de alunos em atividades acadêmicas específicas no EduTrack AI.

## Requirements

### Requirement: Grade Submission for Activity
The system SHALL allow an authenticated instructor to register or update a numeric grade score and optional qualitative feedback for an enrolled student in a specific activity.

#### Scenario: Successful grade assignment
- **WHEN** a teacher submits a valid numeric score between 0 and the activity's maximum score along with optional feedback for a student
- **THEN** the system MUST persist the grade record associated with the activity, student, and teacher, returning the created/updated grade details

#### Scenario: Score validation failure
- **WHEN** a teacher submits a score that is negative or exceeds the maximum score allowed for the activity
- **THEN** the system MUST reject the operation and return an appropriate validation error

### Requirement: Grade Retrieval by Activity
The system SHALL allow instructors to retrieve all student grades registered for a given activity.

#### Scenario: Fetching all grades of an activity
- **WHEN** an authorized instructor queries grades by activity ID
- **THEN** the system MUST return the list of student grades including student ID, score, feedback, and creation date

### Requirement: Student Grade Record Consultation
The system SHALL allow retrieval of all activity grades assigned to an individual student.

#### Scenario: Fetching student grades history
- **WHEN** a user queries grades for a specific student ID
- **THEN** the system MUST return all associated activity grades with activity title, score achieved, maximum score, and instructor comments
