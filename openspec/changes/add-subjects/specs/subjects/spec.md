## Purpose

Provides academic subject (disciplina) management for students, enabling the registration, listing, updating, and tracking of enrolled courses in EduTrack AI.

## ADDED Requirements

### Requirement: Subject Creation
The system SHALL allow users to register a new academic subject with a required name and optional attributes including subject code, instructor name, semester/term, and color indicator.

#### Scenario: Successful subject creation
- **WHEN** the user submits the subject registration form with a valid subject name and optional metadata
- **THEN** the system MUST save the subject associated with the user and display a confirmation message

#### Scenario: Validation failure on missing name
- **WHEN** the user attempts to create a subject without providing a subject name
- **THEN** the system MUST reject the submission and inform the user that the name is required

### Requirement: Subject Listing
The system SHALL retrieve and display all academic subjects associated with the authenticated student in the "Disciplinas" view.

#### Scenario: Listing user subjects
- **WHEN** the user navigates to the "Disciplinas" section and has registered subjects
- **THEN** the system MUST display all subjects with their names, codes, instructors, semesters, and visual tags

#### Scenario: Empty subjects state
- **WHEN** the user navigates to the "Disciplinas" section and has no registered subjects
- **THEN** the system MUST display an informative empty state message with a prompt to add the first subject

### Requirement: Subject Modification
The system SHALL allow users to edit existing subject details such as the name, code, instructor, semester, and color indicator.

#### Scenario: Successfully updating a subject
- **WHEN** the user submits updated information for an existing subject
- **THEN** the system MUST persist the changes and reflect the updated information in the subjects view

### Requirement: Subject Deletion
The system SHALL allow users to remove an existing subject from their academic list.

#### Scenario: Successfully removing a subject
- **WHEN** the user confirms deletion of a specific subject
- **THEN** the system MUST delete the subject record and remove it from the displayed list

### Requirement: Active Subjects Dashboard Metric
The system SHALL display the accurate count of active registered subjects on the user dashboard.

#### Scenario: Dashboard metric updates
- **WHEN** the user views the "Dashboard"
- **THEN** the system MUST display a metric card for "Disciplinas Ativas" reflecting the total number of subjects registered by the user
