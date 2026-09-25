## 1. Backend & Data Schema

- [x] 1.1 Create Xano table schema `tables/subject.xs` with fields (`id`, `created_at`, `user_id`, `name`, `code`, `professor`, `semester`, `color`, `status`) and verify syntax conforms to existing table definitions
- [x] 1.2 Create API group and endpoint definitions in `apis/subjects/` for CRUD operations (`GET /subject`, `POST /subject`, `GET /subject/{id}`, `PATCH /subject/{id}`, `DELETE /subject/{id}`) and verify file layout

## 2. Data Access & Service Layer

- [x] 2.1 Implement subject data service in `services/subject_service.py` with CRUD methods supporting `st.session_state` storage and optional backend API adapter, and verify operations with unit/smoke tests
- [x] 2.2 Add sample demo subjects initialization for offline/standalone local development and verify subjects load cleanly on fresh session start

## 3. Streamlit Interface ("Disciplinas" & "Dashboard")

- [x] 3.1 Implement subject creation form in `app.py` under "Disciplinas" with required validation on name, and verify successful creation persists to state and shows confirmation
- [x] 3.2 Implement subjects list view in `app.py` with card layout displaying course name, code, professor, semester, and color badge, including empty state handling, and verify visual presentation
- [x] 3.3 Implement edit and delete capabilities for subjects in `app.py`, and verify state updates and list refresh upon action
- [x] 3.4 Update "Dashboard" in `app.py` to dynamically display the active subjects count in the metric card, and verify it matches the current active subjects list

## 4. End-to-End Validation

- [x] 4.1 Run Streamlit application locally and verify navigation, subject creation, edition, deletion, and dashboard metric updates without runtime errors
