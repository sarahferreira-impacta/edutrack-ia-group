import unittest

from app import summarize_dashboard, summarize_subject_progress


class TestDashboardMetrics(unittest.TestCase):
    def test_summarize_dashboard_counts_statuses(self):
        tasks = [
            {"status": "completed"},
            {"status": "completed"},
            {"status": "pending"},
            {"status": "in_progress"},
            {"status": "pending"},
        ]

        summary = summarize_dashboard([], tasks)

        self.assertEqual(summary["total_tasks"], 5)
        self.assertEqual(summary["completed_tasks"], 2)
        self.assertEqual(summary["pending_tasks"], 2)
        self.assertEqual(summary["in_progress_tasks"], 1)
        self.assertEqual(summary["overall_completion"], 40.0)

    def test_summarize_subject_progress_isolated_by_subject(self):
        subjects = [
            {"id": 10, "name": "Matemática", "teacher": "Prof. Ana", "hours": 40},
            {"id": 20, "name": "História", "teacher": "Prof. Beto", "hours": 30},
        ]
        tasks = [
            {"subject_id": 10, "status": "completed"},
            {"subject_id": 10, "status": "pending"},
            {"subject_id": 20, "status": "completed"},
            {"subject_id": 20, "status": "completed"},
        ]

        summary = summarize_subject_progress(subjects, tasks)

        self.assertEqual(len(summary), 2)
        by_id = {item["subject_id"]: item for item in summary}
        self.assertEqual(by_id[10]["completed_tasks"], 1)
        self.assertEqual(by_id[10]["total_tasks"], 2)
        self.assertEqual(by_id[10]["progress_percentage"], 50.0)
        self.assertEqual(by_id[20]["completed_tasks"], 2)
        self.assertEqual(by_id[20]["total_tasks"], 2)
        self.assertEqual(by_id[20]["progress_percentage"], 100.0)


if __name__ == "__main__":
    unittest.main()
