## 1. Esquema de Banco de Dados (Xano)

- [ ] 1.1 Criar o esquema da tabela de atividades em `table/activity.xs` com campos `id`, `created_at`, `subject_id`, `title`, `description` e `max_score` e verificar a sintaxe do arquivo
- [ ] 1.2 Criar o esquema da tabela de notas em `table/activity_grade.xs` com campos `id`, `created_at`, `activity_id`, `student_id`, `score`, `feedback` e `graded_by` e verificar a integridade dos relacionamentos

## 2. Endpoints de API (Xano)

- [ ] 2.1 Criar a definição do grupo de API em `api/grades/api_group.xs` e verificar a estrutura do grupo
- [ ] 2.2 Criar o endpoint de lançamento de nota `POST /grade` em `api/grades/grade_POST.xs` com validação de nota e upsert e verificar a estrutura do endpoint
- [ ] 2.3 Criar o endpoint de consulta por atividade `GET /grade/activity/{activity_id}` em `api/grades/grade_activity_id_GET.xs` e verificar os campos retornados
- [ ] 2.4 Criar o endpoint de consulta por aluno `GET /grade/student/{student_id}` em `api/grades/grade_student_id_GET.xs` e verificar a filtragem por aluno
