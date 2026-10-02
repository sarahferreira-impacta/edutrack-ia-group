## 1. Schema & Backend Definitions

- [ ] 1.1 Create `tables/subjects.xs` with table name `subjects` and fields `id` (auto/int), `created_at` (timestamp), `user_id` (FK to `user`), `name` (text), `teacher` (text), and `hours` (int), and verify schema syntax against existing table files
- [ ] 1.2 Update API endpoint definitions in `apis/subjects/` to incorporate `teacher` and `hours` in request inputs, db payloads, and responses, and verify file syntax

## 2. Service Layer & UI Integration

- [ ] 2.1 Update `services/subject_service.py` to support `teacher` and `hours` fields with non-negative validation (`hours >= 0`), and verify unit tests in `tests/test_subject_service.py`
- [ ] 2.2 Update `app.py` subject creation form and card views to include `teacher` and workload `hours` input fields, and verify Streamlit AppTest in `tests/test_streamlit_app.py`

## 3. End-to-End Validation

- [ ] 3.1 Run test suite across all services and Streamlit components and verify all tests pass without errors
