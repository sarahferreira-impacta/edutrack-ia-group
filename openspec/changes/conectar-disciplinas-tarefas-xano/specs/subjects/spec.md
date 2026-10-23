# subjects Specification

## Purpose

Define os requisitos de consulta e exibição de dados reais de disciplinas na página de Disciplinas do EduTrack AI a partir do endpoint GET do Xano.

## ADDED Requirements

### Requirement: Real Subjects Listing in Disciplinas Page
The system SHALL query the Xano endpoint `GET https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects` and render the retrieved subjects in the "Disciplinas" page listing tab without static mockup data.

#### Scenario: Displaying real subjects
- **WHEN** the user opens the "Disciplinas" page ("Listar" tab)
- **THEN** the system MUST retrieve subjects from the GET endpoint and display their real attributes in the view

#### Scenario: Empty state handling
- **WHEN** the Xano GET endpoint returns an empty collection of subjects
- **THEN** the system MUST display an informative notice indicating that no subjects are registered

#### Scenario: Network or invalid response error handling
- **WHEN** the request to the Xano GET endpoint fails or returns an error status code
- **THEN** the system MUST display a clear error message to the user without breaking the page layout

