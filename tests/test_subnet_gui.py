"""Widget behavior tests; explicitly skipped when Tk has no display."""

import importlib
import os
import tkinter as tk
import unittest
from unittest.mock import patch

import subnet_gui


class ImportTests(unittest.TestCase):
    def test_import_does_not_create_window(self):
        with patch("tkinter.Tk", side_effect=AssertionError("unexpected window")):
            importlib.reload(subnet_gui)


class WindowTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            if os.environ.get("SUBNET_GUI_REQUIRE_DISPLAY") == "1":
                raise
            self.skipTest(f"Tk display unavailable: {exc}")
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        self.app = subnet_gui.SubnetCalculator(self.root)

    def enter(self, address, prefix):
        self.app.address.set(address)
        self.app.prefix.set(prefix)
        self.app.calculate_button.invoke()

    def test_button_calculates_example_and_normalization(self):
        self.app.calculate_button.invoke()
        self.assertEqual(self.app.results["network"].get(), "192.168.1.0/24")
        self.assertEqual(self.app.results["usable_count"].get(), "254")
        self.assertIn("normalized", self.app.note.get())

    def test_invalid_inputs_clear_previous_results(self):
        for address, prefix in (("999.1.2.3", "24"), ("192.0.2.1", "33"),
                                ("", "24"), ("192.0.2.1", "024"),
                                ("2001:db8::", "24"), ("192.0.2.1", "9" * 5000)):
            with self.subTest(address=address, prefix=prefix[:20]):
                self.app.calculate_button.invoke()
                self.enter(address, prefix)
                self.assertTrue(all(not value.get() for value in self.app.results.values()))
                self.assertIn("Invalid input", self.app.status.get())
                self.assertEqual(self.app.note.get(), "")

    def test_editing_clears_stale_result(self):
        self.app.calculate_button.invoke()
        self.app.prefix.set("26")
        self.assertEqual(self.app.results["network"].get(), "")

    def test_special_prefix_notes_and_large_range(self):
        for prefix, count, note in (("31", "2", "point-to-point"),
                                    ("32", "1", "one host"), ("0", "4294967294", "normalized")):
            with self.subTest(prefix=prefix):
                self.enter("192.0.2.7", prefix)
                self.assertEqual(self.app.results["usable_count"].get(), count)
                self.assertIn(note, self.app.note.get())


if __name__ == "__main__":
    unittest.main()
