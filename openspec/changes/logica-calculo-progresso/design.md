## Context

EduTrack AI organizes academic entities across `subjects` (disciplinas) and `academic_tasks` (tarefas). See `proposal.md` for motivation. The application has existing CRUD services in `services/subject_service.py` and `services/task_service.py`, as well as REST API endpoints in Xano. A standalone script is required to compute progress per subject and output JSON.

## Goals / Non-Goals

**Goals:**
- Implement `scripts/calculate_progress.py` with function `calculate_subject_progress(subject_id: int, token: Optional[str] = None) -> str`.
- Compute the completion rate as `(completed_tasks / total_tasks) * 100` rounded to 2 decimal places.
- Consume existing CRUD endpoints (`GET /subjects/{id}` or `fetch_subjects_from_xano()` and `GET /academic_tasks?subject_id={id}` or `fetch_tasks_from_xano()`).
- Return a standard JSON payload with `subject_id`, `subject_name`, `total_tasks`, `completed_tasks`, and `progress_percentage`.
- Provide CLI support allowing execution directly via terminal (`python scripts/calculate_progress.py <subject_id>`).

**Non-Goals:**
- No creation of new Xano database tables or backend endpoints.
- No push, sync, or deploy to Xano.
- No modifications to Streamlit user interface pages.

## Decisions

### Decisão 1: Arquitetura do Módulo `scripts/calculate_progress.py`
- **Abordagem**: Implementar uma função reutilizável `calculate_subject_progress(subject_id, ...)` que retorna uma string JSON e também suporta execução direta via linha de comando (`if __name__ == "__main__":`).
- **Racional**: Permite que o cálculo seja utilizado tanto por outros scripts/serviços Python quanto diretamente via CLI para automações ou inspeção.

### Decisão 2: Consulta aos Endpoints CRUD e Respeito à Autenticação
- **Abordagem**: Utilizar os endpoints CRUD autenticados já existentes (`GET /subjects` e `GET /academic_tasks`), enviando o cabeçalho `Authorization: Bearer <token>` a partir de variáveis de ambiente (`.env`), parâmetros ou session state.
- **Racional**: Reutiliza a infraestrutura de segurança e dados do EduTrack AI sem duplicar chamadas de rede ou inventar credenciais.

### Decisão 3: Tratamento de Tarefas Concluídas e Divisão por Zero
- **Abordagem**: Considerar como concluídas tarefas cujo status seja `"completed"` ou `"done"`. Quando `total_tasks == 0`, o progresso retornado é `0.0`.
- **Racional**: Previne exceções de `ZeroDivisionError` e garante consistência semântica para disciplinas recém-criadas sem tarefas.

## Risks / Trade-offs

- **[Risk] Disciplina inexistente ou pertencente a outro usuário**  
  → **Mitigation**: Retornar JSON estruturado com chave `error` e status informativo, sem quebrar a execução do script.
- **[Risk] Falha de conexão de rede ou ausência de token**  
  → **Mitigation**: Capturar exceções de requisição HTTP e retornar payload JSON indicando a falha de autenticação ou conectividade.

