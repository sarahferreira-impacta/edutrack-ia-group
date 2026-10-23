## Context

Consulte `proposal.md` para motivação e escopo. As páginas `pages/1_📚_Disciplinas.py` e `pages/2_📝_Tarefas.py` utilizam mockups locais. O usuário forneceu as URLs reais publicadas no Xano para leitura:
- Disciplinas GET: `https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects`
- Tarefas GET: `https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks`

Esta arquitetura estabelece a integração somente-leitura (GET) entre o Streamlit e o backend Xano, garantindo robustez e manutenção do layout existente.

## Goals / Non-Goals

**Goals:**
- Conectar a página de Disciplinas ao endpoint GET real de `subjects` para exibir os registros persistidos.
- Conectar a página de Tarefas ao endpoint GET real de `academic_tasks` para exibir os registros persistidos.
- Tratar requisições com tratamento de exceções e respostas inválidas, exibindo mensagens claras via `st.error` / `st.info`.
- Manter busca por texto e filtro de status na página de Tarefas, aplicando-os à lista de tarefas retornada da API.
- Respeitar a autenticação existente (caso configurada em variáveis de ambiente, secrets ou session state) sem criar sistemas de login provisórios.
- Preservar o layout visual e estrutura de componentes das páginas.

**Non-Goals:**
- Não implementar POST, cadastro de disciplinas ou tarefas.
- Não implementar login provisório, tela de autenticação ou cadastro de usuários.
- Não implementar edição (PATCH) ou exclusão (DELETE) na interface.
- Não alterar schemas de banco ou arquivos XanoScript.
- Não executar push, deploy ou sincronização com o Xano.

## Decisions

### Decisão 1: URLs Fixadas nos Serviços com Suporte a Configuração
- **Abordagem**: Utilizar como padrão as URLs completas fornecidas:
  - `https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects`
  - `https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks`
  Permitindo sobreposição via variável de ambiente ou `st.secrets` caso configurado.
- **Racional**: Garante conexão imediata com os grupos reais publicados no Xano sem suposições sobre slugs ou identificadores de API.

### Decisão 2: Funções de Consulta Dedicadas na Camada `services/`
- **Abordagem**: Encapsular as chamadas GET em funções limpas em `services/subject_service.py` (`fetch_subjects_from_xano()`) e `services/task_service.py` (`fetch_tasks_from_xano()`).
- **Racional**: Mantém a separação entre apresentação e rede, facilitando testes e reutilização.

### Decisão 3: Tratamento de Autenticação Sem Login Provisório
- **Abordagem**: As funções de consulta verificam se há token disponível em `st.session_state.get("auth_token")` ou variável de ambiente/secrets `XANO_AUTH_TOKEN`. Se presente, anexam o cabeçalho `Authorization: Bearer <token>`. Se ausente, executam a requisição direta. Caso o backend responda com status `401 Unauthorized` ou erro de permissão, a interface exibe mensagem orientativa clara (`st.warning` / `st.error`) explicando a necessidade de credencial, sem inventar fluxos ou telas fictícias de login.
- **Racional**: Atende estritamente à diretriz de respeitar as configurações existentes sem introduzir autenticações provisórias fora do escopo.

### Decisão 4: Preservação de Layout e Filtragem em Memória
- **Abordagem**: Na página de Tarefas, os filtros existentes (input de busca e selectbox de status) continuam operando na camada de apresentação sobre a lista de tarefas recebida do Xano. Em Disciplinas, a tabela `st.dataframe` renderiza as colunas reais vindas do backend.
- **Racional**: Mantém 100% da identidade visual e usabilidade atual das páginas.

## Risks / Trade-offs

- **[Risk]** Falha de conectividade ou resposta com status de erro (ex: 401, 404, 500).  
  → **Mitigation**: Uso de `try/except requests.RequestException` e checagem de `response.ok` nos serviços, retornando mensagem descritiva para exibição no frontend.
- **[Risk]** Resposta com formato inesperado (não-JSON ou lista vazia).  
  → **Mitigation**: Validação do tipo do retorno com fallback para lista vazia e exibição de aviso amigável de estado vazio.

