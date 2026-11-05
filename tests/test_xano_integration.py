import unittest
from unittest.mock import patch

from services.subject_service import fetch_subjects_from_xano
from services.task_service import create_task_in_xano, fetch_tasks_from_xano, update_task_status_in_xano


class TestXanoIntegration(unittest.TestCase):
    @patch("services.subject_service.requests.get")
    @patch("services.subject_service.os.getenv")
    def test_fetch_subjects_from_xano_success(self, mock_getenv, mock_get):
        mock_getenv.side_effect = lambda key, default=None: {
            "XANO_SUBJECTS_URL": "https://example.com/subjects",
        }.get(key, default)
        mock_response = mock_get.return_value
        mock_response.ok = True
        mock_response.json.return_value = [
            {"id": 10, "name": "Algoritmos", "teacher": "Prof. Ada", "status": "active"}
        ]

        subjects = fetch_subjects_from_xano()

        self.assertEqual(len(subjects), 1)
        self.assertEqual(subjects[0]["name"], "Algoritmos")
        self.assertEqual(subjects[0]["professor"], "Prof. Ada")
        self.assertEqual(mock_get.call_args.args[0], "https://example.com/subjects")

    @patch("services.task_service.requests.get")
    @patch("services.task_service.os.getenv")
    def test_fetch_tasks_from_xano_success(self, mock_getenv, mock_get):
        mock_getenv.side_effect = lambda key, default=None: {
            "XANO_TASKS_URL": "https://example.com/academic_tasks",
        }.get(key, default)
        mock_response = mock_get.return_value
        mock_response.ok = True
        mock_response.json.return_value = [
            {"id": 21, "title": "Trabalho final", "status": "pending", "subject_id": 10}
        ]

        tasks = fetch_tasks_from_xano()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Trabalho final")
        self.assertEqual(tasks[0]["status"], "pending")
        self.assertEqual(mock_get.call_args.args[0], "https://example.com/academic_tasks")

    @patch("services.task_service.requests.patch")
    @patch("services.task_service.requests.get")
    @patch("services.task_service.get_auth_token", return_value="token-123")
    def test_update_task_status_in_xano_success(self, mock_token, mock_get, mock_patch):
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "id": 21,
            "title": "Trabalho final",
            "description": "Descreva o conteúdo",
            "due_date": "2026-12-31",
            "subject_id": 7,
            "status": "pending",
        }

        mock_response = mock_patch.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"id": 21, "status": "completed"}

        result = update_task_status_in_xano(task_id=21, status="completed")

        self.assertEqual(result["status"], "completed")
        self.assertTrue(mock_patch.call_args.args[0].endswith("/21"))
        self.assertEqual(
            mock_patch.call_args.kwargs["json"],
            {
                "title": "Trabalho final",
                "description": "Descreva o conteúdo",
                "due_date": "2026-12-31",
                "subject_id": 7,
                "status": "completed",
            },
        )

    @patch("services.task_service.requests.patch")
    @patch("services.task_service.requests.get")
    @patch("services.task_service.requests.post")
    @patch("services.task_service.os.getenv")
    @patch("services.task_service.get_auth_token", return_value="token-123")
    def test_create_and_update_task_use_configured_xano_base_url(self, mock_token, mock_getenv, mock_post, mock_get, mock_patch):
        mock_getenv.side_effect = lambda key, default=None: {
            "XANO_TASKS_URL": "https://example.com/academic_tasks",
        }.get(key, default)

        mock_post_response = mock_post.return_value
        mock_post_response.ok = True
        mock_post_response.json.return_value = {"id": 99, "status": "pending"}

        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "id": 99,
            "title": "Nova tarefa",
            "description": "Detalhes",
            "due_date": "2026-12-31",
            "subject_id": 7,
            "status": "pending",
        }

        mock_patch_response = mock_patch.return_value
        mock_patch_response.ok = True
        mock_patch_response.json.return_value = {"id": 99, "status": "completed"}

        create_task_in_xano(title="Nova tarefa", subject_id=7, status="pending")
        update_task_status_in_xano(task_id=99, status="completed")

        self.assertEqual(mock_post.call_args.args[0], "https://example.com/academic_tasks")
        self.assertEqual(mock_patch.call_args.args[0], "https://example.com/academic_tasks/99")
        self.assertEqual(
            mock_patch.call_args.kwargs["json"],
            {
                "title": "Nova tarefa",
                "description": "Detalhes",
                "due_date": "2026-12-31",
                "subject_id": 7,
                "status": "completed",
            },
        )


if __name__ == "__main__":
    unittest.main()
