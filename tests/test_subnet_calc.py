"""Hand-calculated boundary oracles and real CLI behavior."""

import contextlib
import importlib
import io
from pathlib import Path
import subprocess
import sys
import unittest

import subnet_calc


ROOT = Path(__file__).resolve().parents[1]


class CalculationTests(unittest.TestCase):
    def test_documentation_example(self):
        self.assertEqual(subnet_calc.calculate_subnet("192.0.2.0/24"), {
            "network": "192.0.2.0", "prefix_length": 24,
            "subnet_mask": "255.255.255.0", "wildcard_mask": "0.0.0.255",
            "broadcast": "192.0.2.255", "first_usable": "192.0.2.1",
            "last_usable": "192.0.2.254", "usable_count": 254, "normalized": False,
        })

    def test_small_subnet_endpoints(self):
        value = subnet_calc.calculate_subnet("198.51.100.4/30")
        self.assertEqual((value["first_usable"], value["last_usable"], value["usable_count"]),
                         ("198.51.100.5", "198.51.100.6", 2))
        self.assertEqual(value["broadcast"], "198.51.100.7")

    def test_point_to_point_uses_both_endpoints(self):
        value = subnet_calc.calculate_subnet("198.51.100.10/31")
        self.assertEqual((value["first_usable"], value["last_usable"], value["usable_count"]),
                         ("198.51.100.10", "198.51.100.11", 2))

    def test_single_host(self):
        value = subnet_calc.calculate_subnet("203.0.113.7/32")
        self.assertEqual((value["first_usable"], value["last_usable"], value["usable_count"]),
                         ("203.0.113.7", "203.0.113.7", 1))

    def test_entire_ipv4_space_is_arithmetic(self):
        value = subnet_calc.calculate_subnet("0.0.0.0/0")
        self.assertEqual((value["first_usable"], value["last_usable"], value["usable_count"]),
                         ("0.0.0.1", "255.255.255.254", 4294967294))

    def test_host_bits_are_reported(self):
        value = subnet_calc.calculate_subnet("192.0.2.73/24")
        self.assertEqual(value["network"], "192.0.2.0")
        self.assertTrue(value["normalized"])

    def test_invalid_inputs_are_rejected(self):
        for value in ("", "192.0.2.1", "192.0.2.0/33", "192.0.2.0/-1", "999.0.2.0/24",
                      "192.0.2.0/255.255.255.0", "192.0.2.0/024", "192.0.2.0/24/1",
                      "2001:db8::/64", "example.org/24", "192.0.2.0/\u0662\u0664", "x" * 1000,
                      "192.0.2.0/24\n", " 192.0.2.0/24", None, 24):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "decimal CIDR"):
                subnet_calc.calculate_subnet(value)

    def test_import_has_no_output(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            importlib.reload(subnet_calc)
        self.assertEqual(output.getvalue(), "")


class CommandTests(unittest.TestCase):
    def run_cli(self, value):
        # Fixed owned script and interpreter; input is an argv value, never a shell command.
        return subprocess.run([sys.executable, "-I", str(ROOT / "subnet_calc.py"), value],
                              capture_output=True, text=True, timeout=5, check=False)

    def test_real_example_output(self):
        result = self.run_cli("192.0.2.0/24")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Network:       192.0.2.0/24", result.stdout)
        self.assertIn("Usable count:  254", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_large_network_finishes_without_enumeration(self):
        result = self.run_cli("0.0.0.0/0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("4294967294", result.stdout)

    def test_bad_input_has_exit_two_without_echoing_controls(self):
        result = self.run_cli("\x1b[31mnot-an-address/24")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("decimal CIDR", result.stderr)
        self.assertNotIn("\x1b", result.stderr)

    def test_normalization_and_point_to_point_notes(self):
        result = self.run_cli("198.51.100.11/31")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("host bits were normalized", result.stdout)
        self.assertIn("point-to-point", result.stdout)
        self.assertIn("not a broadcast destination", result.stdout)


if __name__ == "__main__":
    unittest.main()
