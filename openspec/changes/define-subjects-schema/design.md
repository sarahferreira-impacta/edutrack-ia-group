## Context

See `proposal.md` for background and motivation. The project requires a dedicated Xano table schema `subjects` with the exact fields requested: `id` (auto), `name` (text), `teacher` (text), `hours` (int), and `user_id` (foreign key to Xano's authentication `user` table).

## Goals / Non-Goals

**Goals:**
- Define `tables/subjects.xs` conforming strictly to the requested fields and Xano schema conventions.
- Configure proper indexes for `id` (primary key), `user_id` (btree lookup for student queries), and `created_at`.
- Align backend API query inputs/outputs in `apis/subjects/` to handle `teacher` and `hours`.
- Update the Python service layer (`services/subject_service.py`) and Streamlit UI (`app.py`) to support `teacher` and `hours` (carga horária).

**Non-Goals:**
- Complex attendance logs or automated schedule conflict detection.
- Syllabus file uploads or PDF extraction (separate future change).

## Decisions

### Decision 1: Xano Table Definition Syntax
- **Approach**: Define the table as `table subjects` in `tables/subjects.xs`:
  ```xs
  table subjects {
    auth = false

    schema {
      int id
      timestamp created_at?=now

      int user_id? {
        table = "user"
      }

      text name filters=trim
      text? teacher filters=trim
      int? hours
    }

    index = [
      {type: "primary", field: [{name: "id"}]}
      {type: "btree", field: [{name: "created_at", op: "desc"}]}
      {type: "btree", field: [{name: "user_id", op: "asc"}]}
    ]

    tags = ["edutrack:academic"]
  }
  ```
- **Rationale**: Matches the structure of existing tables (`883218_user.xs`, `883219_event_log.xs`) while adhering exactly to the requested fields.

### Decision 2: Service and UI Field Adaptation
- **Approach**: Update `services/subject_service.py` to use `teacher` and `hours` as first-class fields (with fallback alias for `professor` if previously saved), and enhance `app.py` to include a numeric input for "Carga Horária (horas)".
- **Rationale**: Ensures seamless continuity while fulfilling the user's specific schema requirements.

## Risks / Trade-offs

- **[Risk]** Negative values entered for course hours.  
  → **Mitigation**: Constrain `hours >= 0` in `subject_service.py` and enforce `min_value=0` on Streamlit's `st.number_input`.
