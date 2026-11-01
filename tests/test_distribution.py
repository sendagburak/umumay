import subprocess
import sys
import unittest
from pathlib import Path


class DistributionTests(unittest.TestCase):
    def test_cli_version_does_not_require_gtk(self):
        result = subprocess.run([sys.executable, '-m', 'umumay', '--version'],
                                capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.strip(), '0.1.4')

    def test_both_notices_are_present_offline(self):
        root = Path(__file__).resolve().parents[1]
        tr = (root / 'umumay/privacy_tr.txt').read_text()
        en = (root / 'umumay/privacy_en.txt').read_text()
        self.assertIn('GİZLİLİK', tr)
        self.assertIn('PRIVACY', en)
        self.assertIn('settings.json', tr)
        self.assertIn('settings.json', en)
