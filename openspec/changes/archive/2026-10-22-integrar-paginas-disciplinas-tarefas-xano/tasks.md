## 1. Camada de Serviços para Integração com Xano

- [ ] 1.1 Atualizar `services/subject_service.py` para integrar com os endpoints `GET /subjects` e `POST /subjects` da API Xano e verificar o retorno das funções
- [ ] 1.2 Criar `services/task_service.py` para consultar tarefas no endpoint `GET /academic_tasks` da API Xano e verificar a estrutura do serviço

## 2. Integração da Página de Disciplinas

- [ ] 2.1 Conectar a aba de listagem em `pages/1_📚_Disciplinas.py` ao endpoint `GET /subjects`, removendo a mensagem mockup e a tabela fixa e verificando a renderização dos dados
- [ ] 2.2 Conectar o formulário de cadastro em `pages/1_📚_Disciplinas.py` ao endpoint `POST /subjects`, enviando os campos reais e verificando as mensagens de validação e sucesso

## 3. Integração da Página de Tarefas

- [ ] 3.1 Conectar a listagem de tarefas em `pages/2_📝_Tarefas.py` ao endpoint `GET /academic_tasks`, removendo o expander de exemplo estático e verificando a renderização dinâmica
- [ ] 3.2 Implementar a consulta a `GET /subjects` em `pages/2_📝_Tarefas.py` para mapear `subject_id` ao nome da disciplina em cada tarefa e verificar a exibição da matéria relacionada
- [ ] 3.3 Integrar os filtros existentes de busca textual e status em `pages/2_📝_Tarefas.py` aos dados retornados do Xano e verificar o comportamento da filtragem

