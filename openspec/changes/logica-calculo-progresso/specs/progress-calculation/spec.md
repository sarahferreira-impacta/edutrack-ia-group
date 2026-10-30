# progress-calculation Specification

## Purpose

Define the specification for calculating the academic progress percentage of a subject based on its associated tasks and returning the result in JSON format.

## ADDED Requirements

### Requirement: Calculate subject progress percentage
The system SHALL calculate the academic progress percentage for a given subject by determining the ratio of completed tasks to total tasks associated with that subject.

#### Scenario: Subject with completed and pending tasks
- **WHEN** progress is calculated for a subject having completed and pending tasks
- **THEN** system SHALL calculate progress as `(completed_tasks / total_tasks) * 100` and return a JSON payload with `subject_id`, `subject_name`, `total_tasks`, `completed_tasks`, and `progress_percentage`

#### Scenario: Subject with no tasks
- **WHEN** progress is calculated for a subject with zero associated tasks
- **THEN** system SHALL return `0.0` as `progress_percentage` without division-by-zero errors

#### Scenario: Subject not found or invalid
- **WHEN** progress is calculated for a subject ID that does not exist or cannot be retrieved
- **THEN** system SHALL return an error structure formatted as JSON indicating the subject was not found

### Requirement: Consume CRUD endpoints for progress calculation
The progress calculation logic SHALL retrieve subject information and task records using the existing CRUD endpoints.

#### Scenario: Retrieve tasks and subject via endpoints
- **WHEN** the calculation script executes for a specific subject ID
- **THEN** system SHALL request the subject details and the corresponding tasks list via authenticated CRUD endpoints and use the returned dataset for computation

