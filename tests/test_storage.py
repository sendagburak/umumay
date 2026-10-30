import json
import os
import tempfile
import unittest
from pathlib import Path

from umumay.core import collect_snapshot
from umumay.storage import SettingsStore, StorageError, report_data, write_report


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'config' / 'settings.json'

    def test_settings_defaults_and_roundtrip_private_permissions(self):
        store = SettingsStore(self.path)
        self.assertEqual(store.load(), set())
        store.save({'links', 'awake'})
        self.assertEqual(store.load(), {'links', 'awake'})
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.path.parent.stat().st_mode & 0o777, 0o700)
        self.assertEqual(set(json.loads(self.path.read_text())), {'schema', 'disabled'})

    def test_corrupt_unknown_or_oversized_settings_are_reported(self):
        self.path.parent.mkdir()
        for raw in ['invalid', '[]', '{"schema":2,"disabled":[]}',
                    '{"schema":1,"disabled":["execute-code"]}',
                    '{"schema":1,"disabled":"links"}', 'x' * 65537]:
            self.path.write_text(raw)
            with self.subTest(raw=raw[:45]), self.assertRaises(StorageError):
                SettingsStore(self.path).load()

    def test_symlink_target_is_not_read_or_overwritten(self):
        self.path.parent.mkdir()
        victim = Path(self.temp.name) / 'victim'
        victim.write_text('unchanged')
        self.path.symlink_to(victim)
        for operation in [lambda: SettingsStore(self.path).load(),
                          lambda: SettingsStore(self.path).save(set())]:
            with self.assertRaises(StorageError):
                operation()
        self.assertEqual(victim.read_text(), 'unchanged')

    def test_unknown_module_cannot_be_persisted(self):
        with self.assertRaises(StorageError):
            SettingsStore(self.path).save({'arbitrary.plugin'})

    def test_report_allowlist_omits_environment_packages_urls_and_identity(self):
        with unittest.mock.patch.dict(os.environ, {'XDG_CURRENT_DESKTOP': 'GNOME;private@example.test',
                                                   'XDG_SESSION_TYPE': 'secret-token'}):
            data = report_data(collect_snapshot())
        self.assertEqual(set(data), {'schema', 'app_version', 'platform', 'session', 'metrics'})
        self.assertEqual(set(data['platform']), {'distribution', 'pardus_family'})
        text = json.dumps(data)
        for private in ['private@example.test', 'secret-token', str(Path.home()), 'hostname', 'packages']:
            self.assertNotIn(private, text)

    def test_report_is_local_private_and_refuses_symlink(self):
        write_report(self.path, collect_snapshot())
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(json.loads(self.path.read_text())['schema'], 1)
        self.path.unlink()
        self.path.symlink_to(Path(self.temp.name) / 'victim')
        with self.assertRaises(StorageError):
            write_report(self.path, collect_snapshot())
