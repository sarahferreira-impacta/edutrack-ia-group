"""
AppTest integration tests for EduTrack AI app.py
"""

import os
import unittest
from streamlit.testing.v1 import AppTest

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))


class TestStreamlitApp(unittest.TestCase):
    def test_dashboard_load(self):
        at = AppTest.from_file(APP_PATH, default_timeout=10)
        at.run()
        self.assertFalse(at.exception, f"Exceptions on Dashboard load: {at.exception}")

        # Check metrics exist
        metric_values = [m.value for m in at.metric]
        self.assertIn("2", metric_values)  # 2 active sample subjects

    def test_navigation_to_disciplinas(self):
        at = AppTest.from_file(APP_PATH, default_timeout=10)
        at.run()
        self.assertFalse(at.exception)

        # Change sidebar radio to "Disciplinas"
        at.sidebar.radio[0].set_value("Disciplinas").run()
        self.assertFalse(at.exception, f"Exceptions on Disciplinas view: {at.exception}")

        # Verify tabs exist
        self.assertTrue(len(at.tabs) >= 2)

    def test_navigation_to_tarefas(self):
        at = AppTest.from_file(APP_PATH, default_timeout=10)
        at.run()
        at.sidebar.radio[0].set_value("Tarefas").run()
        self.assertFalse(at.exception, f"Exceptions on Tarefas view: {at.exception}")


if __name__ == "__main__":
    unittest.main()
