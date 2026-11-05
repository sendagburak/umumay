import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from umumay.autostart import AutostartError, is_autostart_enabled, set_autostart


class AutostartTests(unittest.TestCase):
    def test_explicit_opt_in_and_opt_out(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'autostart' / 'io.github.sendagburak.umumay.desktop'
            self.assertFalse(is_autostart_enabled(target))
            with patch('umumay.autostart.shutil.which', return_value='/usr/bin/umumay'):
                self.assertTrue(set_autostart(True, target))
                self.assertTrue(is_autostart_enabled(target))
                self.assertEqual(target.stat().st_mode & 0o777, 0o600)
                self.assertTrue(set_autostart(True, target))
            self.assertFalse(set_autostart(False, target))
            self.assertFalse(target.exists())

    def test_do_not_overwrite_or_delete_other_apps_settings(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'autostart' / 'io.github.sendagburak.umumay.desktop'
            target.parent.mkdir()
            target.write_text('[Desktop Entry]\nName=Some other file\n')
            with patch('umumay.autostart.shutil.which', return_value='/usr/bin/umumay'):
                with self.assertRaises(AutostartError):
                    set_autostart(True, target)
            with self.assertRaises(AutostartError):
                set_autostart(False, target)
            self.assertEqual(target.read_text(), '[Desktop Entry]\nName=Some other file\n')

    def test_existing_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'autostart' / 'io.github.sendagburak.umumay.desktop'
            target.parent.mkdir()
            victim = Path(folder) / 'existing'
            victim.write_text('keep')
            target.symlink_to(victim)
            with patch('umumay.autostart.shutil.which', return_value='/usr/bin/umumay'):
                with self.assertRaises(AutostartError):
                    set_autostart(True, target)
            with self.assertRaises(AutostartError):
                set_autostart(False, target)
            self.assertEqual(victim.read_text(), 'keep')

    def test_no_executable_no_autostart(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'autostart' / 'io.github.sendagburak.umumay.desktop'
            with patch('umumay.autostart.shutil.which', return_value=None):
                with self.assertRaises(AutostartError):
                    set_autostart(True, target)
            self.assertFalse(target.exists())
