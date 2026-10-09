## Why

No EduTrack AI, os professores necessitam de uma funcionalidade dedicada para registrar notas dos alunos em atividades acadêmicas específicas. Atualmente, a plataforma suporta autenticação e gestão de disciplinas, mas não possui estrutura no backend para que o professor lance notas vinculadas a uma atividade e a um estudante.

## What Changes

- **Esquema de Dados para `activity_grades`**: Criar a definição de tabela no Xano (`table/activity_grades.xs`) para registrar as notas atribuídas aos estudantes em atividades específicas.
- **API POST para Lançar Nota**: Criar o endpoint `POST /activity_grades` no Xano (`api/activity_grades/`) para permitir que o professor autenticado lance a nota de um aluno em determinada atividade.

## Capabilities

### New Capabilities
- `activity-grades`: Permite que o professor lance notas para alunos em atividades específicas.

### Modified Capabilities
<!-- Nenhuma capacidade existente teve seus requisitos alterados -->

## Impact

- **Banco de Dados (Xano .xs)**: Criação da tabela `activity_grades`.
- **APIs (Xano .xs)**: Criação do endpoint `POST /activity_grades`.
