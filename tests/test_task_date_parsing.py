import unittest
from datetime import date

from app_pages import __init__
from app_pages import task_helpers


class TestTaskDateParsing(unittest.TestCase):
    def test_parse_xano_date_handles_iso_and_timezone(self):
        self.assertEqual(task_helpers.parse_xano_date("2026-11-05T18:30:00Z"), date(2026, 11, 5))
        self.assertEqual(task_helpers.parse_xano_date("2026-11-05T18:30:00-03:00"), date(2026, 11, 5))
        self.assertEqual(task_helpers.parse_xano_date("2026-11-05"), date(2026, 11, 5))

    def test_parse_xano_date_handles_timestamps_and_invalid_values(self):
        self.assertEqual(task_helpers.parse_xano_date(1760000000000), date(2025, 10, 9))
        self.assertIsNone(task_helpers.parse_xano_date(None))
        self.assertIsNone(task_helpers.parse_xano_date("valor invalido"))


if __name__ == "__main__":
    unittest.main()
