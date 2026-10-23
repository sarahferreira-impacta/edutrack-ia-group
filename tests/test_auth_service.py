import unittest
from unittest.mock import patch

from services.auth_service import build_xano_url, signup_user, login_user


class TestAuthService(unittest.TestCase):
    @patch("services.auth_service.os.environ", {"XANO_BASE_URL": "https://example.com"})
    def test_build_xano_url(self):
        self.assertEqual(build_xano_url("auth/login"), "https://example.com/auth/login")

    @patch("services.auth_service.requests.post")
    @patch("services.auth_service.get_xano_base_url", return_value="https://example.com")
    def test_signup_user_success(self, mock_base_url, mock_post):
        mock_response = mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"authToken": "token-123", "user_id": 10}

        result = signup_user("Ana", "ana@email.com", "123456")

        self.assertEqual(result["authToken"], "token-123")
        self.assertEqual(result["user_id"], 10)

    @patch("services.auth_service.requests.post")
    @patch("services.auth_service.get_xano_base_url", return_value="https://example.com")
    def test_login_user_success(self, mock_base_url, mock_post):
        mock_response = mock_post.return_value
        mock_response.ok = True
        mock_response.json.return_value = {"authToken": "token-456", "user_id": 11}

        result = login_user("ana@email.com", "123456")

        self.assertEqual(result["authToken"], "token-456")
        self.assertEqual(result["user_id"], 11)


if __name__ == "__main__":
    unittest.main()
