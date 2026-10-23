## 1. Serviços de Consulta aos Endpoints GET

- [x] 1.1 Implementar função de consulta ao endpoint `GET https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects` em `services/subject_service.py` com tratamento de erros de requisição e verificar a resposta
- [x] 1.2 Implementar função de consulta ao endpoint `GET https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks` em `services/task_service.py` com tratamento de erros de requisição e verificar a resposta

## 2. Conexão da Página de Disciplinas

- [x] 2.1 Conectar a aba de listagem em `pages/1_📚_Disciplinas.py` à consulta do endpoint `GET /subjects`, removendo a tabela fixa de simulação e verificando a exibição dos dados reais e mensagens de erro

## 3. Conexão da Página de Tarefas

- [x] 3.1 Conectar a listagem em `pages/2_📝_Tarefas.py` à consulta do endpoint `GET /academic_tasks`, removendo o expander de exemplo estático e verificando a renderização dos dados reais com mensagens de carregamento e erro
- [x] 3.2 Aplicar a busca textual e o filtro de status em `pages/2_📝_Tarefas.py` sobre os dados reais carregados e verificar o funcionamento da filtragem

