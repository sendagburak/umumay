import ast
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from umumay.runtime import validate_local_session


class OfflineTests(unittest.TestCase):
    def test_remote_display_and_remote_dbus_are_rejected_before_gui(self):
        for env in [{'DISPLAY': 'remote.test:0'}, {'DISPLAY': 'localhost:10.0'},
                    {'DBUS_SESSION_BUS_ADDRESS': 'tcp:host=remote.test,port=1234'},
                    {'AT_SPI_BUS_ADDRESS': 'tcp:host=remote.test,port=1234'},
                    {'DBUS_STARTER_ADDRESS': 'tcp:host=remote.test,port=1234'},
                    {'DBUS_SESSION_BUS_ADDRESS': 'unix:path=/tmp/bus;tcp:host=x,port=1'}]:
            with self.subTest(env=env), self.assertRaises(RuntimeError):
                validate_local_session(env)
        validate_local_session({'DISPLAY': ':0', 'DBUS_SESSION_BUS_ADDRESS': 'unix:path=/tmp/bus'})
        validate_local_session({'WAYLAND_DISPLAY': 'wayland-0'})

    def test_runtime_has_no_network_client_imports_or_shell_execution(self):
        forbidden = {'requests', 'httpx', 'aiohttp', 'socket', 'smtplib', 'ftplib',
                     'webbrowser', 'telemetry', 'sentry_sdk'}
        package = Path(__file__).resolve().parents[1] / 'umumay'
        for path in package.glob('*.py'):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                modules = [n.name for n in node.names] if isinstance(node, ast.Import) else \
                          [node.module or ''] if isinstance(node, ast.ImportFrom) else []
                for module in modules:
                    self.assertNotIn(module.split('.')[0], forbidden, str(path))
                    self.assertFalse(module.startswith(('urllib.request', 'http.client')), str(path))
                if isinstance(node, ast.Call):
                    for kw in node.keywords:
                        self.assertFalse(kw.arg == 'shell' and isinstance(kw.value, ast.Constant)
                                         and kw.value.value is True, str(path))

    def test_core_workflows_run_with_python_network_functions_disabled(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network socket')), \
             patch.object(socket, 'getaddrinfo', side_effect=AssertionError('DNS')):
            from umumay.core import collect_snapshot
            from umumay.links import clean_url
            from umumay.storage import SettingsStore, write_report
            with tempfile.TemporaryDirectory() as folder:
                store = SettingsStore(Path(folder) / 'settings.json')
                store.save({'links'})
                self.assertEqual(store.load(), {'links'})
                self.assertEqual(clean_url('https://example.test/?utm_source=x'), 'https://example.test/')
                write_report(Path(folder) / 'report.json', collect_snapshot())
