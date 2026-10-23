## Context

Consulte `proposal.md` para motivação e justificativa. As páginas `pages/1_📚_Disciplinas.py` e `pages/2_📝_Tarefas.py` utilizam atualmente mockups locais e dados estáticos. O backend Xano possui os endpoints RESTful `GET /subjects`, `POST /subjects` e `GET /academic_tasks` sob autenticação de usuário (`auth = "user"`). O objetivo desta arquitetura é conectar as páginas a esses endpoints através de serviços Python em `services/`, mantendo a segurança, tratamento de erros e integridade do layout Streamlit.

## Goals / Non-Goals

**Goals:**
- Configurar cliente/serviço HTTP modular para consumir os endpoints do Xano usando `requests`.
- Atualizar `services/subject_service.py` para consultar `GET /subjects` e cadastrar via `POST /subjects`.
- Criar `services/task_service.py` para consultar tarefas via `GET /academic_tasks` e suportar parâmetros como `subject_id`.
- Integrar `pages/1_📚_Disciplinas.py` consumindo os dados reais e enviando novos registros ao backend.
- Integrar `pages/2_📝_Tarefas.py` consumindo tarefas reais e mapeando `subject_id` ao nome da disciplina correspondente carregada de `GET /subjects`.
- Manter busca por texto e filtro por status na listagem de tarefas.
- Prover feedback visual amigável (loading spinners, alertas de erro e sucesso).

**Non-Goals:**
- Não criar botões, rotas ou ações de edição (`PATCH`) ou exclusão (`DELETE`) na interface das páginas, pois não foram solicitadas.
- Não alterar schemas de banco de dados (`.xs`) ou criar novos endpoints no backend.
- Não executar comandos de push, sync ou deploy para o Xano (Regra nº 2 do `AGENTS.md`).
- Não alterar a estrutura visual ou o layout preexistente das páginas Streamlit.

## Decisions

### Decisão 1: Camada de Serviços Centralizada em `services/`
- **Abordagem**: Toda a comunicação HTTP com os endpoints Xano é encapsulada em módulos dentro de `services/`:
  - `services/subject_service.py`: funções para `get_all_subjects()` e `create_subject()`.
  - `services/task_service.py`: funções para `get_academic_tasks()`.
- **Racional**: Separa a lógica de apresentação das páginas Streamlit das chamadas de rede e do tratamento de requisições HTTP, facilitando testes e manutenção.
- **Alternativas consideradas**: Fazer chamadas `requests` diretamente nas páginas Streamlit (rejeitado por acoplamento excessivo e código duplicado).

### Decisão 2: Gestão de URL Base e Autenticação
- **Abordagem**: Obter `XANO_API_URL` e o token de autenticação via `st.secrets`, variáveis de ambiente (`os.getenv`) ou `st.session_state` (ex: `st.session_state.get("auth_token")`).
- **Racional**: Não expõe credenciais ou tokens em código versionado e respeita a diretriz de segurança de associar as operações ao usuário autenticado (`Authorization: Bearer <token>`).

### Decisão 3: Mapeamento Relacional de Disciplinas na Página de Tarefas
- **Abordagem**: A página `pages/2_📝_Tarefas.py` executa a consulta a `GET /academic_tasks` e também utiliza `get_all_subjects()` para montar um dicionário de correspondência `{subject['id']: subject['name']}`.
- **Racional**: O schema de `academic_tasks` armazena `subject_id`. Esse mapeamento em memória no frontend permite exibir o nome legível da disciplina para cada tarefa no expander sem exigir endpoints adicionais no backend.

### Decisão 4: Mapeamento de Campos de Formulário sem Invenção de Atributos
- **Abordagem**: O formulário existente em `pages/1_📚_Disciplinas.py` possui campos para nome, professor e dia da aula. O endpoint `POST /subjects` aceita estritamente `name`, `teacher` (opcional) e `hours` (opcional). O serviço mapeará `name` e `teacher`. Campos que não existem no schema do Xano (como dia da semana) não serão enviados no payload para não gerar erros de validação no Xano.
- **Racional**: Respeita a regra de ouro de conformidade estrita com o schema das tabelas e endpoints existentes.

## Risks / Trade-offs

- **[Risk]** Backend Xano indisponível ou falha temporária de rede.  
  → **Mitigation**: Tratar requisições com blocos `try/except requests.RequestException` nos serviços, retornando mensagens claras via `st.error` sem travar a interface do Streamlit.
- **[Risk]** Ausência de token autenticado durante o uso da aplicação.  
  → **Mitigation**: Exibir aviso amigável com `st.warning` orientando o usuário a efetuar login se o token não for encontrado no contexto da sessão.

