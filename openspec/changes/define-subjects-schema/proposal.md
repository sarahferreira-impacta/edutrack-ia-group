## Why

Standardize the database schema for the `subjects` table according to project requirements and backend conventions in Xano. The schema needs to explicitly define core academic attributes: `id` (auto), `name` (text), `teacher` (text), `hours` (int), and `user_id` (foreign key pointing to the Xano authentication `user` table).

## What Changes

- **Define `subjects` table schema**: Create `tables/subjects.xs` with explicit field definitions:
  - `id` (auto-incrementing int, primary key)
  - `created_at` (timestamp, default now)
  - `name` (text, trimmed)
  - `teacher` (text, trimmed)
  - `hours` (int, workload hours)
  - `user_id` (int, foreign key referencing the `user` table)
- **Database indexes**: Primary key on `id`, index on `user_id`, and index on `created_at`.
- **Backend and Service Alignment**: Ensure subject data models, API schemas, and service layer methods support `teacher` and `hours`.

## Capabilities

### New Capabilities
- `subjects-schema`: Definition of the Xano `subjects` table schema with `id`, `name`, `teacher`, `hours`, and `user_id`.

### Modified Capabilities
<!-- None -->

## Impact

- **Database / Schema**: New or updated schema definition in `tables/subjects.xs`.
- **Data Models / Services**: Adapt service fields in `services/subject_service.py` to seamlessly handle `teacher` and `hours`.
- **API Contracts**: CRUD endpoints in `apis/subjects/` receive `teacher` and `hours` inputs.
