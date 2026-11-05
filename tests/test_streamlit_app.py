"""
AppTest integration tests for EduTrack AI app.py
"""

import os
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))


class TestStreamlitApp(unittest.TestCase):
    def test_dashboard_load(self):
        at = AppTest.from_file(APP_PATH, default_timeout=10)
        at.run()
        self.assertFalse(at.exception, f"Exceptions on Dashboard load: {at.exception}")

    def test_single_navigation_source(self):
        source = Path(APP_PATH).read_text(encoding="utf-8")
        self.assertIn("st.navigation(", source)
        self.assertNotIn("st.sidebar.radio", source)
        self.assertNotIn("st.sidebar.title", source)

    def test_navigation_pages_are_defined(self):
        source = Path(APP_PATH).read_text(encoding="utf-8")
        for page_name in ["Dashboard", "Disciplinas", "Tarefas", "Perfil"]:
            self.assertIn(page_name, source)


if __name__ == "__main__":
    unittest.main()
