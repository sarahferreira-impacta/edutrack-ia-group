import unittest
from unittest.mock import patch

from services.subject_service import _resolve_xano_url as resolve_subject_url
from services.task_service import _get_tasks_api_url


class TestXanoRouteConfig(unittest.TestCase):
    @patch("services.subject_service.os.getenv", side_effect=lambda key, default=None: default)
    def test_subject_default_url_uses_subject_api_group(self, _mock_getenv):
        self.assertEqual(
            resolve_subject_url("subjects"),
            "https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects",
        )

    @patch("services.task_service.os.getenv", side_effect=lambda key, default=None: default)
    def test_task_default_url_uses_task_api_group(self, _mock_getenv):
        self.assertEqual(
            _get_tasks_api_url(),
            "https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks",
        )

    @patch("services.task_service.requests.post")
    @patch("services.task_service.get_auth_token", return_value="token-123")
    @patch("services.task_service.os.getenv", side_effect=lambda key, default=None: default)
    def test_create_task_uses_correct_xano_route(self, _mock_getenv, _mock_token, mock_post):
        mock_response = mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"id": 88, "title": "Nova tarefa", "subject_id": 7, "status": "pending"}

        from services.task_service import create_task_in_xano

        create_task_in_xano(title="Nova tarefa", subject_id=7, status="pending")

        self.assertEqual(
            mock_post.call_args.args[0],
            "https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks",
        )


if __name__ == "__main__":
    unittest.main()
