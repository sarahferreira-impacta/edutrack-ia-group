## Why

EduTrack AI currently manages academic subjects and tasks but lacks an automated progress calculation service to evaluate student completion rate per subject. Calculating and exposing the progress percentage (completed tasks over total tasks) as a structured JSON response allows consumers to track academic advancement per discipline.

## What Changes

- Add a Python script and reusable calculation function in `scripts/calculate_progress.py`.
- Calculate the completion percentage of a subject based on its associated tasks (`completed / total * 100`).
- Connect to existing CRUD endpoints to retrieve subject and task records for the authenticated student.
- Format and return the calculated result as a structured JSON object.
- Handle edge cases gracefully, such as subjects with no tasks (avoiding division by zero) and invalid subject IDs.

## Capabilities

### New Capabilities
- `progress-calculation`: Service that calculates progress percentage (completed / total) for an academic subject based on its tasks and returns a JSON payload.

### Modified Capabilities
<!-- No requirement changes to existing capabilities -->

## Impact

- Adds `scripts/calculate_progress.py`.
- Consumes existing `subjects` and `academic_tasks` GET CRUD endpoints.
- No database schema alterations or backend deployment required.

