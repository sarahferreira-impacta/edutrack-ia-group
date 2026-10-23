import unittest
from unittest.mock import patch

from services.subject_service import fetch_subjects_from_xano
from services.task_service import fetch_tasks_from_xano


class TestXanoIntegration(unittest.TestCase):
    @patch("services.subject_service.requests.get")
    @patch("services.subject_service.os.getenv")
    def test_fetch_subjects_from_xano_success(self, mock_getenv, mock_get):
        mock_getenv.side_effect = lambda key, default=None: {
            "XANO_BASE_URL": "https://example.com/api:w0xiZjdk",
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
        self.assertEqual(mock_get.call_args.args[0], "https://example.com/api:w0xiZjdk/subjects")

    @patch("services.task_service.requests.get")
    @patch("services.task_service.os.getenv")
    def test_fetch_tasks_from_xano_success(self, mock_getenv, mock_get):
        mock_getenv.side_effect = lambda key, default=None: {
            "XANO_BASE_URL": "https://example.com/api:w0xiZjdk",
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
        self.assertEqual(mock_get.call_args.args[0], "https://example.com/api:w0xiZjdk/academic_tasks")


if __name__ == "__main__":
    unittest.main()
