## Why

EduTrack AI aims to assist students in tracking and organizing their academic journey. Currently, the application only provides placeholder UI elements for subjects ("Disciplinas") without data models, APIs, or interactive management features. Adding the subjects capability is essential to allow students to register, view, update, and manage their academic courses, establishing the core data foundation for upcoming features like task management, study scheduling, and AI-driven academic insights.

## What Changes

- **Subject Data Model**: Define the database structure/schema for subjects (`subject` / `disciplina`), including fields for title/name, code, instructor/professor, semester/term, color tag, and user reference.
- **Backend APIs & Service Endpoints**: Define API endpoints to perform CRUD operations on subjects (create, read/list, update, delete) scoped to authenticated users.
- **Frontend Subjects Management (Streamlit)**: Upgrade the "Disciplinas" section in `app.py` to allow users to view current subjects, create new subjects with relevant academic details, edit subject info, and view active subject counts on the Dashboard.

## Capabilities

### New Capabilities
- `subjects`: Management of academic subjects (disciplinas), covering data model definitions, backend CRUD operations, and user interface workflows for viewing and managing enrolled courses.

### Modified Capabilities
<!-- None: this is a new capability in the project -->

## Impact

- **Database / Schema**: New table schema definition for subjects (e.g., in Xano `.xs` format and/or backend data definitions).
- **APIs**: New API group/endpoints for subjects CRUD operations.
- **Frontend (`app.py`)**: Updates to Streamlit UI navigation, dashboard metrics, and interactive forms/lists for subjects.
- **Dependencies**: No new external dependencies required (uses existing Streamlit framework and REST API integrations).
