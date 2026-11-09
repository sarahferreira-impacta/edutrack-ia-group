import unittest
from unittest.mock import patch, MagicMock
from app_pages.task_helpers import normalize_status, status_label, parse_xano_date, format_due_date
from scripts.calculate_progress import calculate_progress_data


class TestTaskEditingAndStatusValidation(unittest.TestCase):
    """Testes obrigatórios de validação de status, checkbox, datas e recálculo de progresso."""

    def test_status_rules_for_checkbox(self):
        """Cenários obrigatórios:
        - Status Pendente -> Checkbox desmarcada
        - Status Em andamento -> Checkbox desmarcada
        - Status Concluída -> Checkbox marcada
        """
        # Pendente
        status_pending = normalize_status("pending")
        self.assertFalse(status_pending == "completed")

        # Em andamento
        status_in_progress = normalize_status("in_progress")
        self.assertFalse(status_in_progress == "completed")

        # Concluída
        status_completed = normalize_status("completed")
        self.assertTrue(status_completed == "completed")

    def test_status_normalization_aliases(self):
        """Garante consistência de sinônimos de status."""
        self.assertEqual(normalize_status("done"), "completed")
        self.assertEqual(normalize_status("concluida"), "completed")
        self.assertEqual(normalize_status("concluída"), "completed")
        self.assertEqual(normalize_status("in_progress"), "in_progress")
        self.assertEqual(normalize_status("in-progress"), "in_progress")
        self.assertEqual(normalize_status("em andamento"), "in_progress")
        self.assertEqual(normalize_status("pending"), "pending")
        self.assertEqual(normalize_status(""), "pending")

    def test_progress_recalculation_transitions(self):
        """Cenários:
        - Alterar Pendente para Concluída -> Progresso aumenta
        - Alterar Concluída para Pendente -> Progresso recalculado/diminui
        """
        tasks = [
            {"id": 1, "subject_id": 10, "status": "pending"},
            {"id": 2, "subject_id": 10, "status": "in_progress"},
            {"id": 3, "subject_id": 10, "status": "pending"},
        ]
        # Inicial: 0 de 3 concluídas (0%)
        initial_prog = calculate_progress_data(10, "Matemática", tasks)
        self.assertEqual(initial_prog["completed_tasks"], 0)
        self.assertEqual(initial_prog["progress_percentage"], 0.0)

        # Transição 1: Alterar Pendente para Concluída (tarefa 1)
        tasks[0]["status"] = "completed"
        step1_prog = calculate_progress_data(10, "Matemática", tasks)
        self.assertEqual(step1_prog["completed_tasks"], 1)
        self.assertEqual(step1_prog["progress_percentage"], 33.33)

        # Transição 2: Alterar Em andamento para Concluída (tarefa 2)
        tasks[1]["status"] = "completed"
        step2_prog = calculate_progress_data(10, "Matemática", tasks)
        self.assertEqual(step2_prog["completed_tasks"], 2)
        self.assertEqual(step2_prog["progress_percentage"], 66.67)

        # Transição 3: Alterar Concluída para Pendente (tarefa 1 reaberta)
        tasks[0]["status"] = "pending"
        step3_prog = calculate_progress_data(10, "Matemática", tasks)
        self.assertEqual(step3_prog["completed_tasks"], 1)
        self.assertEqual(step3_prog["progress_percentage"], 33.33)

        # Transição 4: Alterar Concluída para Em andamento (tarefa 2)
        tasks[1]["status"] = "in_progress"
        step4_prog = calculate_progress_data(10, "Matemática", tasks)
        self.assertEqual(step4_prog["completed_tasks"], 0)
        self.assertEqual(step4_prog["progress_percentage"], 0.0)

    def test_date_parsing_and_formatting(self):
        """Cenários de data:
        - Parse ISO 8601 (YYYY-MM-DD e com timezone/timestamp)
        - Formatação consistente DD/MM/YYYY
        - Manutenção de integridade
        """
        # ISO simples
        parsed = parse_xano_date("2026-11-20")
        self.assertEqual(str(parsed), "2026-11-20")
        self.assertEqual(format_due_date("2026-11-20"), "20/11/2026")

        # ISO com timestamp e timezone
        parsed_tz = parse_xano_date("2026-11-25T14:30:00Z")
        self.assertEqual(str(parsed_tz), "2026-11-25")
        self.assertEqual(format_due_date("2026-11-25T14:30:00Z"), "25/11/2026")

        # Vazio / None
        self.assertIsNone(parse_xano_date(None))
        self.assertIsNone(parse_xano_date(""))
        self.assertEqual(format_due_date(None), "Sem prazo")

    @patch("services.task_service._fetch_task_by_id")
    @patch("services.task_service.requests.patch")
    @patch("services.task_service.get_auth_token", return_value="fake-token")
    def test_update_task_in_xano_payload_integrity(self, mock_auth, mock_patch, mock_fetch):
        """Verifica se update_task_in_xano envia payload correto com due_date e status preservados/atualizados."""
        from services.task_service import update_task_in_xano

        mock_fetch.return_value = {
            "id": 42,
            "title": "Trabalho Final",
            "description": "Texto descritivo",
            "due_date": "2026-11-10",
            "status": "pending",
            "subject_id": 5,
        }

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "id": 42,
            "title": "Trabalho Final Modificado",
            "description": "Texto descritivo",
            "due_date": "2026-11-15",
            "status": "in_progress",
            "subject_id": 5,
        }
        mock_patch.return_value = mock_response

        result = update_task_in_xano(
            task_id=42,
            title="Trabalho Final Modificado",
            due_date="2026-11-15",
            status="in_progress",
        )

        mock_patch.assert_called_once()
        called_args, called_kwargs = mock_patch.call_args
        sent_payload = called_kwargs["json"]
        self.assertEqual(sent_payload["title"], "Trabalho Final Modificado")
        self.assertEqual(sent_payload["due_date"], "2026-11-15")
        self.assertEqual(sent_payload["status"], "in_progress")
        self.assertEqual(called_kwargs["headers"]["Authorization"], "Bearer fake-token")


if __name__ == "__main__":
    unittest.main()
