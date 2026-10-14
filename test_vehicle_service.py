"""Small regression tests for the Lab 5 vehicle service application."""

import tempfile
import unittest
from pathlib import Path

import vehicle_service as app


class VehicleServiceTests(unittest.TestCase):
    def setUp(self):
        app.service_records.clear()

    def test_default_history_is_not_shared(self):
        first = app.add_service("KA01AB1234")
        second = app.add_service("KA02CD5678")
        self.assertIsNot(first, second)
        self.assertEqual(first, ["KA01AB1234"])
        self.assertEqual(second, ["KA02CD5678"])

    def test_add_service_cost_and_total(self):
        app.add_service("KA01AB1234", "Oil Change")
        app.add_service("KA01AB1234", "Wheel Alignment")
        self.assertEqual(app.get_total_cost("KA01AB1234"), 2300)

    def test_unknown_service_type_is_rejected(self):
        with self.assertRaises(ValueError):
            app.add_service("KA01AB1234", "Teleportation")

    def test_empty_vehicle_number_is_rejected(self):
        with self.assertRaises(ValueError):
            app.add_service("  ")

    def test_cancel_missing_record_returns_false(self):
        self.assertFalse(app.cancel_service("KA09ZZ0001", "General"))

    def test_cancel_existing_service(self):
        app.add_service("KA01AB1234", "Brake Check")
        self.assertTrue(app.cancel_service("KA01AB1234", "Brake Check"))
        self.assertEqual(app.get_total_cost("KA01AB1234"), 0)

    def test_job_card_id_is_stable_and_short(self):
        first = app.job_card_id("KA01AB1234")
        self.assertEqual(first, app.job_card_id("KA01AB1234"))
        self.assertEqual(len(first), 8)

    def test_save_and_load_records(self):
        app.add_service("KA01AB1234", "Oil Change")
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "services.json"
            app.save_records(str(file_path))
            loaded = app.load_records(str(file_path))
        self.assertEqual(loaded, app.service_records)


if __name__ == "__main__":
    unittest.main()
