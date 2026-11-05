import unittest
from unittest.mock import patch

from services.auth_service import build_xano_url, get_current_user, signup_user, login_user, update_current_user_profile
from services.subject_service import create_subject_in_xano
from services.task_service import create_task_in_xano


class TestAuthService(unittest.TestCase):
    @patch("services.auth_service.os.environ", {"XANO_AUTH_BASE_URL": "https://example.com/api:w0xiZjdk"})
    def test_build_xano_url(self):
        self.assertEqual(build_xano_url("auth/login"), "https://example.com/api:w0xiZjdk/auth/login")

    @patch("services.auth_service.requests.post")
    @patch("services.auth_service.get_xano_base_url", return_value="https://example.com/api:w0xiZjdk")
    def test_signup_user_success(self, mock_base_url, mock_post):
        mock_response = mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"authToken": "token-123", "user_id": 10}

        result = signup_user("Ana", "ana@email.com", "123456")

        self.assertEqual(result["authToken"], "token-123")
        self.assertEqual(result["user_id"], 10)

    @patch("services.auth_service.requests.post")
    @patch("services.auth_service.get_xano_base_url", return_value="https://example.com/api:w0xiZjdk")
    def test_login_user_success(self, mock_base_url, mock_post):
        mock_response = mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"authToken": "token-456", "user_id": 11}

        result = login_user("ana@email.com", "123456")

        self.assertEqual(result["authToken"], "token-456")
        self.assertEqual(result["user_id"], 11)

    @patch("services.auth_service.requests.get")
    @patch("services.auth_service.get_xano_base_url", return_value="https://example.com/api:w0xiZjdk")
    def test_get_current_user_unpacks_xano_data(self, mock_base_url, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"data": {"id": 7, "name": "Ana", "email": "ana@email.com"}}

        result = get_current_user("token-abc")

        self.assertEqual(result["id"], 7)
        self.assertEqual(result["email"], "ana@email.com")

    @patch("services.auth_service.requests.patch")
    @patch("services.auth_service.get_xano_base_url", return_value="https://example.com/api:w0xiZjdk")
    @patch("services.auth_service.get_current_user", return_value={"id": 7, "name": "Ana", "email": "ana@email.com"})
    def test_update_current_user_profile_uses_xano_user_route(self, mock_current_user, mock_base_url, mock_patch):
        mock_response = mock_patch.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"id": 7, "name": "Ana Souza", "email": "ana.nova@email.com"}

        result = update_current_user_profile(name="Ana Souza", email="ana.nova@email.com", token="token-abc")

        self.assertEqual(result["email"], "ana.nova@email.com")
        self.assertEqual(mock_patch.call_args.args[0], "https://example.com/api:w0xiZjdk/user/7")
        self.assertEqual(mock_patch.call_args.kwargs["json"], {"name": "Ana Souza", "email": "ana.nova@email.com"})

    @patch("services.subject_service.requests.post")
    @patch("services.subject_service.get_auth_token", return_value="abc123")
    def test_create_subject_in_xano_success(self, mock_token, mock_post):
        mock_response = mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"id": 1, "name": "Algoritmos"}

        result = create_subject_in_xano("Algoritmos", teacher="Prof. Ada")

        self.assertEqual(result["name"], "Algoritmos")
        self.assertEqual(mock_post.call_args.args[0], "https://x8ki-letl-twmt.n7.xano.io/api:LG5UUEEH/subjects")

    @patch("services.task_service.requests.post")
    @patch("services.task_service.get_auth_token", return_value="abc123")
    def test_create_task_in_xano_success(self, mock_token, mock_post):
        mock_response = mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"id": 99, "title": "Trabalho final"}

        result = create_task_in_xano("Trabalho final", subject_id=7, status="pending")

        self.assertEqual(result["title"], "Trabalho final")
        self.assertEqual(mock_post.call_args.args[0], "https://x8ki-letl-twmt.n7.xano.io/api:6lZMI4mm/academic_tasks")


if __name__ == "__main__":
    unittest.main()
