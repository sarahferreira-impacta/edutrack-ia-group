## Context

Consulte `proposal.md` para motivação e objetivos. O projeto EduTrack AI já possui as tabelas `subjects` (`table/subjects.xs`) e `academic_tasks` (`table/academic_tasks.xs`). O objetivo desta mudança é definir os grupos de API e os endpoints RESTful CRUD completos para ambas as entidades, assegurando que todas as operações sejam protegidas por autenticação e isoladas por usuário (`auth = "user"`).

## Goals / Non-Goals

**Goals:**
- Criar a estrutura de API para `subjects` com endpoints CRUD:
  - `POST /subjects`: Criação de disciplina vinculada a `$auth.id`.
  - `GET /subjects`: Listagem filtrando exclusivamente por `where = $db.subjects.user_id == $auth.id`.
  - `GET /subjects/{id}`: Consulta individual com validação de propriedade (`$subject.user_id == $auth.id`).
  - `PATCH /subjects/{id}`: Atualização com validação de propriedade.
  - `DELETE /subjects/{id}`: Exclusão com validação de propriedade.
- Criar a estrutura de API para `academic_tasks` com endpoints CRUD:
  - `POST /academic_tasks`: Criação de tarefa vinculada a `$auth.id` e `subject_id`.
  - `GET /academic_tasks`: Listagem filtrando exclusivamente por `where = $db.academic_tasks.user_id == $auth.id`.
  - `GET /academic_tasks/{id}`: Consulta individual com validação de propriedade (`$task.user_id == $auth.id`).
  - `PATCH /academic_tasks/{id}`: Atualização com validação de propriedade.
  - `DELETE /academic_tasks/{id}`: Exclusão com validação de propriedade.
- Aplicar o padrão RESTful e convenções XanoScript em todos os arquivos.

**Non-Goals:**
- Não criar componentes de interface gráfica ou frontend no Streamlit (escopo estrito às APIs solicitadas).
- Não criar suítes de testes automatizados não solicitadas, em conformidade com a Regra nº 1 do `AGENTS.md`.

## Decisions

### Decisão 1: Estrutura de Diretórios de API
- **Abordagem**: Organizar as APIs em pastas dedicadas sob `api/`:
  - `api/subjects/`: arquivo do grupo `subjects.xs` e endpoints `POST.xs`, `GET.xs`, `id_GET.xs`, `id_PATCH.xs`, `id_DELETE.xs`.
  - `api/academic_tasks/`: arquivo do grupo `academic_tasks.xs` e endpoints `POST.xs`, `GET.xs`, `id_GET.xs`, `id_PATCH.xs`, `id_DELETE.xs`.
- **Racional**: Segue a convenção do projeto observada em `api/authentication/` e `api/event_logs/`.

### Decisão 2: Isolamento de Dados por Usuário Autenticado
- **Abordagem**:
  - Em todos os endpoints, definir `auth = "user"`.
  - Nas queries de listagem (`GET /subjects`, `GET /academic_tasks`), aplicar filtro obrigatório `where = $db.<table>.user_id == $auth.id`.
  - Nas rotas de criação (`POST`), o campo `user_id` é sempre atribuído diretamente de `$auth.id`.
  - Nas rotas parametrizadas por ID (`GET/{id}`, `PATCH/{id}`, `DELETE/{id}`), executar `db.get` seguido de:
    ```xs
    precondition ($record.user_id == $auth.id) {
      error_type = "forbidden"
      error_message = "Acesso negado: registro pertence a outro usuário."
    }
    ```
- **Racional**: Atende diretamente à diretriz de segurança do `AGENTS.md` ("Filtro Obrigatório: Toda query deve filtrar por user_id do usuário autenticado") e ao pedido do usuário.

## Risks / Trade-offs

- **[Risk]** Criação de tarefa apontando para `subject_id` pertencente a outro aluno.  
  → **Mitigation**: No endpoint `POST /academic_tasks`, verificar se a disciplina informada pertence ao `$auth.id` antes de persistir a tarefa.

