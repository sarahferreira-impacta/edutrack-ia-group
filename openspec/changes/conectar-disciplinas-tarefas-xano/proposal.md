## Why

As páginas de Disciplinas (`pages/1_📚_Disciplinas.py`) e Tarefas (`pages/2_📝_Tarefas.py`) da aplicação EduTrack AI atualmente exibem tabelas e expanders com dados estáticos e simulados (mockups). Com a disponibilidade dos endpoints de consulta no Xano (`GET https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects` e `GET https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks`), esta change estabelece a conexão direta dessas duas páginas aos serviços de leitura da API, permitindo aos usuários visualizar as informações reais persistidas no banco de dados.

## What Changes

- **Consulta de Disciplinas no Frontend (`pages/1_📚_Disciplinas.py`)**:
  - Conexão da aba de listagem ao endpoint `GET https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects`.
  - Substituição da tabela fixa com dados simulados pela renderização dos dados reais retornados pelo Xano.
  - Exibição de mensagens apropriadas para carregamento, estado sem registros e tratamento de erros de rede/resposta inválida.
  - Preservação integral do layout atual da página.

- **Consulta de Tarefas no Frontend (`pages/2_📝_Tarefas.py`)**:
  - Conexão da listagem ao endpoint `GET https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks`.
  - Substituição do expander fixo de exemplo pela listagem dinâmica das tarefas reais retornadas pela API.
  - Aplicação dos filtros existentes de busca textual e status aos dados reais carregados.
  - Exibição de mensagens de erro claras e feedback visual em caso de falha de conexão ou resposta inválida.
  - Preservação do layout visual atual da página.

- **Camada de Integração (`services/`)**:
  - Adaptação das funções de leitura em `services/subject_service.py` e criação de leitor em `services/task_service.py` para consulta via `requests` nos endpoints GET especificados, respeitando cabeçalhos de autenticação caso configurados, sem criar sistemas provisórios de login.

## Capabilities

### New Capabilities
<!-- Nenhuma nova capability introduzida; integrações no frontend de capabilities já existentes -->

### Modified Capabilities
- `subjects`: Consulta e renderização de dados reais do endpoint `GET /subjects` do Xano na página de Disciplinas.
- `academic-tasks`: Consulta e renderização de dados reais do endpoint `GET /academic_tasks` do Xano na página de Tarefas com suporte a busca e filtros.

## Impact

- **Frontend (`pages/1_📚_Disciplinas.py`, `pages/2_📝_Tarefas.py`)**: Consumo de dados dinâmicos da API Xano em substituição aos dados mockados.
- **Serviços (`services/`)**: Atualização de métodos de consulta HTTP para os endpoints reais do Xano.
- **Backend / Xano**: Nenhum novo endpoint, mutação de dados (POST/PATCH/DELETE) ou alteração de schema.

