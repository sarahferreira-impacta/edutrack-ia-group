## Why

Atualmente, as páginas de Disciplinas (`pages/1_📚_Disciplinas.py`) e Tarefas (`pages/2_📝_Tarefas.py`) do EduTrack AI utilizam dados simulados e mockups estáticos no frontend Streamlit, enquanto o backend Xano já possui tabelas e endpoints RESTful CRUD funcionais e protegidos por autenticação (`/subjects` e `/academic_tasks`). É necessário conectar essas páginas aos serviços e endpoints reais do backend para que os estudantes possam visualizar e cadastrar suas disciplinas e tarefas acadêmicas reais com persistência e isolamento por usuário.

## What Changes

- **Integração da Página de Disciplinas (`pages/1_📚_Disciplinas.py`)**:
  - Consulta e exibição de dados reais a partir do endpoint `GET /subjects`.
  - Envio de dados de novas disciplinas utilizando o endpoint `POST /subjects` com os campos `name` e `teacher`.
  - Tratamento de estados de carregamento, sucesso e erros de comunicação com o backend.
  - Remoção dos dados fixos de demonstração e mensagens de mockup.
  - Preservação integral do layout, abas e estilo visual existente.

- **Integração da Página de Tarefas (`pages/2_📝_Tarefas.py`)**:
  - Consulta e exibição de tarefas reais a partir do endpoint `GET /academic_tasks`.
  - Consulta auxiliar a `GET /subjects` para mapear `subject_id` ao nome da disciplina correspondente.
  - Aplicação dos filtros existentes de busca textual e status sobre os dados carregados do Xano.
  - Exibição de mensagens apropriadas para carregamento, estado vazio e falhas de requisição.
  - Remoção do mockup de tarefa fixa, mantendo a estrutura visual de expander e cards.

- **Camada de Serviços (`services/`)**:
  - Adaptação de `services/subject_service.py` para integração HTTP com a API Xano (`GET /subjects`, `POST /subjects`).
  - Criação de `services/task_service.py` para comunicação HTTP com a API Xano (`GET /academic_tasks`, `POST /academic_tasks`), respeitando os cabeçalhos de autenticação e a URL base configurada.

## Capabilities

### New Capabilities
<!-- Nenhuma nova capability introduzida; a mudança integra capabilities existentes ao frontend -->

### Modified Capabilities
- `subjects`: Adição de requisitos para integração da página Streamlit de disciplinas com os endpoints `GET /subjects` e `POST /subjects` do Xano.
- `academic-tasks`: Adição de requisitos para integração da página Streamlit de tarefas com os endpoints `GET /academic_tasks` e `GET /subjects` do Xano.

## Impact

- **Frontend (`pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`)**: Substituição de dados mockados por chamadas aos serviços de integração do backend.
- **Serviços (`services/`)**: Atualização de `subject_service.py` e criação de `task_service.py` com suporte a requisições HTTP seguras.
- **Backend / Xano**: Nenhum novo endpoint ou alteração de schema necessária; consumo estrito dos endpoints existentes.

