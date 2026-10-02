## Context

See `proposal.md` for background and motivation. The project currently has a Streamlit UI (`app.py`) with placeholder sections and Xano table/API schemas stored under `tables/` and `apis/`. There is currently no schema or UI implementation for managing academic subjects (disciplinas).

## Goals / Non-Goals

**Goals:**
- Define database table schema for `subject` in Xano format matching the existing schema conventions (`tables/`).
- Define the API endpoints for subject operations (`apis/subjects/`) for listing, creating, updating, and deleting subjects.
- Implement an interactive subjects management interface in `app.py` under the "Disciplinas" menu option.
- Provide a robust client/service layer in Python that supports `st.session_state` persistence for standalone local execution and adapts seamlessly to remote Xano API endpoints.
- Update the Dashboard view to reflect real-time active subject counts.

**Non-Goals:**
- Linking assignments, exams, or homework to subjects (out of scope for this change; handled in a future tasks change).
- Complex GPA or final grade calculations.
- Multi-institution sync or SIS (Student Information System) integrations.

## Decisions

### Decision 1: Service Adapter Layer for Subjects
- **Approach**: Create a service module (or helper functions) that manages subject state. If Xano API credentials/URL are configured in environment variables or Streamlit secrets, it calls the backend REST API; otherwise, it operates on `st.session_state` with seeded demo subjects.
- **Rationale**: Enables immediate local testing and interactive UX validation without requiring every contributor to have a live Xano instance connected right away.
- **Alternatives considered**:
  - Direct HTTP calls only: Fails during local development or offline reviews without live credentials.
  - Hardcoded dummy data only: Requires major refactoring when connecting the backend.

### Decision 2: Subject Table Schema Design
- **Approach**: Create a `tables/subject.xs` definition with:
  - `id` (int, primary key)
  - `created_at` (timestamp)
  - `user_id` (foreign key to `user`)
  - `name` (text, required)
  - `code` (text, optional, e.g. "CC101")
  - `professor` (text, optional)
  - `semester` (text, optional, e.g. "2026.1")
  - `color` (text, optional, hex or color tag for UI badges)
  - `status` (enum: "active", "completed", "archived")
- **Rationale**: Follows the existing `.xs` syntax seen in `tables/883218_user.xs` and `tables/883219_event_log.xs`.

### Decision 3: Streamlit UI Layout
- **Approach**: In `app.py`, organize "Disciplinas" into clear sections:
  - Subject creation form in an expander or tab with validation on `name`.
  - Subject cards / metrics showing course code, teacher, semester, and action buttons (edit / delete).
  - Dynamic summary cards in the Dashboard calculating the number of active subjects.
- **Rationale**: Conforms to the clean Figma dashboard reference and Streamlit best practices.

## Risks / Trade-offs

- **[Risk]** Session state resets on browser page refresh if no backend is configured.  
  → **Mitigation**: Initialize `st.session_state` with default sample subjects on first load if empty, and provide clear notification when running in local mock mode vs. live backend mode.

- **[Risk]** Data model drift between Xano `.xs` schema definitions and frontend field names.  
  → **Mitigation**: Standardize field names across `subject.xs` and the Streamlit model (`id`, `name`, `code`, `professor`, `semester`, `color`, `status`).
