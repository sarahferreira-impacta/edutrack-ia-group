"""
Unit tests for subject_service.
"""

import unittest
import streamlit as st
from services.subject_service import (
    init_session_subjects,
    get_all_subjects,
    get_active_subjects,
    count_active_subjects,
    get_subject_by_id,
    create_subject,
    update_subject,
    delete_subject,
    DEFAULT_SAMPLE_SUBJECTS,
)


class TestSubjectService(unittest.TestCase):
    def setUp(self):
        # Reset session state for each test
        st.session_state.clear()

    def test_init_session_subjects(self):
        init_session_subjects()
        self.assertIn("subjects", st.session_state)
        self.assertEqual(len(st.session_state.subjects), len(DEFAULT_SAMPLE_SUBJECTS))

    def test_get_all_and_active_subjects(self):
        all_subs = get_all_subjects()
        self.assertEqual(len(all_subs), 3)

        active_subs = get_active_subjects()
        self.assertEqual(len(active_subs), 2)
        self.assertEqual(count_active_subjects(), 2)

    def test_create_subject_success(self):
        new_sub = create_subject(
            name="Cálculo Diferencial",
            code="MAT-101",
            professor="Prof. Newton",
            semester="2026.1",
            color="#2563EB",
            status="active"
        )
        self.assertEqual(new_sub["name"], "Cálculo Diferencial")
        self.assertEqual(new_sub["id"], 4)
        self.assertEqual(count_active_subjects(), 3)

    def test_create_subject_validation(self):
        with self.assertRaises(ValueError):
            create_subject(name="")
        with self.assertRaises(ValueError):
            create_subject(name="   ")

    def test_update_subject_success(self):
        updated = update_subject(1, name="IA Avançada", professor="Dr. Alan Turing")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["name"], "IA Avançada")
        self.assertEqual(updated["professor"], "Dr. Alan Turing")
        # unchanged fields should stay
        self.assertEqual(updated["code"], "IA-401")

    def test_update_subject_empty_name(self):
        with self.assertRaises(ValueError):
            update_subject(1, name="   ")

    def test_delete_subject(self):
        result = delete_subject(2)
        self.assertTrue(result)
        self.assertIsNone(get_subject_by_id(2))
        self.assertEqual(len(get_all_subjects()), 2)

        # Deleting non-existent subject
        result_fake = delete_subject(999)
        self.assertFalse(result_fake)


if __name__ == "__main__":
    unittest.main()
