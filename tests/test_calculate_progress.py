import json
import unittest
from unittest.mock import patch

from scripts.calculate_progress import (
    calculate_all_subjects_progress,
    calculate_progress_data,
    calculate_subject_progress,
    fetch_subject_details,
    fetch_subject_tasks,
)


class TestCalculateProgress(unittest.TestCase):
    def test_calculate_progress_with_mixed_tasks(self):
        tasks = [
            {"id": 1, "subject_id": 10, "status": "completed"},
            {"id": 2, "subject_id": 10, "status": "pending"},
            {"id": 3, "subject_id": 10, "status": "done"},
            {"id": 4, "subject_id": 10, "status": "in_progress"},
        ]
        data = calculate_progress_data(subject_id=10, subject_name="Banco de Dados", tasks=tasks)

        self.assertEqual(data["subject_id"], 10)
        self.assertEqual(data["subject_name"], "Banco de Dados")
        self.assertEqual(data["total_tasks"], 4)
        self.assertEqual(data["completed_tasks"], 2)
        self.assertEqual(data["progress_percentage"], 50.0)

    def test_calculate_progress_zero_tasks(self):
        data = calculate_progress_data(subject_id=11, subject_name="Inovação", tasks=[])

        self.assertEqual(data["subject_id"], 11)
        self.assertEqual(data["total_tasks"], 0)
        self.assertEqual(data["completed_tasks"], 0)
        self.assertEqual(data["progress_percentage"], 0.0)

    def test_calculate_progress_all_completed(self):
        tasks = [
            {"id": 1, "subject_id": 12, "status": "completed"},
            {"id": 2, "subject_id": 12, "status": "done"},
        ]
        data = calculate_progress_data(subject_id=12, tasks=tasks)

        self.assertEqual(data["total_tasks"], 2)
        self.assertEqual(data["completed_tasks"], 2)
        self.assertEqual(data["progress_percentage"], 100.0)

    def test_calculate_subject_progress_returns_valid_json(self):
        tasks = [
            {"id": 1, "subject_id": 5, "status": "completed"},
            {"id": 2, "subject_id": 5, "status": "pending"},
            {"id": 3, "subject_id": 5, "status": "pending"},
        ]
        json_str = calculate_subject_progress(subject_id=5, subject_name="Redes", tasks=tasks)
        parsed = json.loads(json_str)

        self.assertEqual(parsed["subject_id"], 5)
        self.assertEqual(parsed["subject_name"], "Redes")
        self.assertEqual(parsed["total_tasks"], 3)
        self.assertEqual(parsed["completed_tasks"], 1)
        self.assertEqual(parsed["progress_percentage"], 33.33)

    @patch("scripts.calculate_progress.fetch_subject_tasks")
    @patch("scripts.calculate_progress.requests.get")
    def test_calculate_all_subjects_progress(self, mock_get, mock_fetch_tasks):
        mock_response = mock_get.return_value
        mock_response.ok = True
        mock_response.json.return_value = [
            {"id": 1, "name": "IA"},
            {"id": 2, "name": "DevOps"},
        ]
        mock_fetch_tasks.side_effect = lambda sid, **kwargs: (
            [{"status": "completed"}, {"status": "pending"}] if sid == 1 else []
        )

        json_str = calculate_all_subjects_progress()
        parsed = json.loads(json_str)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["subject_id"], 1)
        self.assertEqual(parsed[0]["progress_percentage"], 50.0)
        self.assertEqual(parsed[1]["subject_id"], 2)
        self.assertEqual(parsed[1]["progress_percentage"], 0.0)

    @patch("scripts.calculate_progress.requests.get")
    def test_fetch_subject_details_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"id": 7, "name": "Matemática Aplicada"}

        subject = fetch_subject_details(7, token="token-test")
        self.assertIsNotNone(subject)
        self.assertEqual(subject["name"], "Matemática Aplicada")

    @patch("scripts.calculate_progress.requests.get")
    def test_fetch_subject_tasks_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.ok = True
        mock_response.json.return_value = [
            {"id": 1, "subject_id": 8, "title": "Lista 1", "status": "completed"},
            {"id": 2, "subject_id": 9, "title": "Lista 2", "status": "pending"},
        ]

        tasks = fetch_subject_tasks(8, token="token-test")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Lista 1")


if __name__ == "__main__":
    unittest.main()
