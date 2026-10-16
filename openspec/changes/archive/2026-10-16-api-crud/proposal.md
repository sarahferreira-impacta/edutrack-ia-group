## Why

Atualmente, o EduTrack AI possui as tabelas `subjects` e `academic_tasks` definidas no backend Xano, porém faltam os endpoints da API REST para permitir que os clientes realizem operações de criação, listagem, atualização e exclusão (CRUD) desses dados de forma segura. É fundamental que todos os acessos sejam restritos ao usuário autenticado (`auth = "user"`), garantindo que cada aluno manipule estritamente suas próprias disciplinas e tarefas.

## What Changes

- **Grupo de API e Endpoints CRUD para `subjects`**:
  - `POST /subjects`: Criação de disciplina vinculada ao `user_id` do usuário autenticado.
  - `GET /subjects`: Listagem de disciplinas com filtro obrigatório por `user_id`.
  - `GET /subjects/{id}`: Consulta de detalhes da disciplina com validação de propriedade (`user_id == $auth.id`).
  - `PATCH /subjects/{id}`: Atualização de disciplina com validação de propriedade.
  - `DELETE /subjects/{id}`: Exclusão de disciplina com validação de propriedade.
- **Grupo de API e Endpoints CRUD para `academic_tasks`**:
  - `POST /academic_tasks`: Criação de tarefa vinculada à disciplina e ao `user_id` do usuário autenticado.
  - `GET /academic_tasks`: Listagem de tarefas com filtro obrigatório por `user_id`.
  - `GET /academic_tasks/{id}`: Consulta de detalhes da tarefa com validação de propriedade (`user_id == $auth.id`).
  - `PATCH /academic_tasks/{id}`: Atualização de tarefa com validação de propriedade.
  - `DELETE /academic_tasks/{id}`: Exclusão de tarefa com validação de propriedade.

## Capabilities

### New Capabilities
- `subjects`: Endpoints RESTful CRUD para manipulação de disciplinas acadêmicas com isolamento de dados por usuário.

### Modified Capabilities
- `academic-tasks`: Inclusão de endpoints RESTful CRUD para manipulação de tarefas acadêmicas com isolamento de dados por usuário.

## Impact

- **APIs (Xano .xs)**: Criação das pastas e arquivos de endpoint sob `api/subjects/` e `api/academic_tasks/`.
- **Segurança**: Aplicação de autenticação obrigatória (`auth = "user"`) e filtros relacionais por `$auth.id` em todas as consultas e mutações.

