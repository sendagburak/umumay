import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from umumay.core import (
    collect_snapshot, cpu_percent, parse_cpu, parse_memory,
    parse_os_release, parse_packages, installed_packages,
)


class CoreTests(unittest.TestCase):
    def test_three_families_are_recognized_not_lookalikes(self):
        for version, family in [('21.5', 21), ('23.5', 23), ('25.2', 25)]:
            info = parse_os_release('ID=pardus\nVERSION_ID="%s"' % version)
            self.assertEqual(info.family, family)
        for text in ['ID=pardus\nVERSION_ID=210', 'ID=debian\nVERSION_ID=25',
                     'ID=pardus\nVERSION_ID=27', '', 'VERSION_ID=23']:
            self.assertIsNone(parse_os_release(text).family)

    def test_os_release_is_data_not_executable(self):
        info = parse_os_release('ID=pardus\nPRETTY_NAME="$(touch bad)"\nVERSION_ID="23.5"')
        self.assertEqual(info.family, 23)

    def test_cpu_excludes_guest_double_counting(self):
        before = parse_cpu('cpu 10 0 10 80 0 0 0 0 8 0\ncpu0 1 2 3')
        after = parse_cpu('cpu 20 0 20 160 0 0 0 0 18 0')
        self.assertEqual(before.total, 100)
        self.assertAlmostEqual(cpu_percent(before, after), 20.0)

    def test_first_sample_reset_and_missing_cpu_are_unknown(self):
        first = parse_cpu('cpu 10 0 10 80 0 0 0 0')
        self.assertIsNone(cpu_percent(None, first))
        self.assertIsNone(cpu_percent(first, first))
        self.assertIsNone(cpu_percent(first, parse_cpu('cpu 1 0 1 8')))
        for text in ['', 'cpu invalid', 'cpu -1 0 0 2', 'cpu0 1 2 3 4']:
            self.assertIsNone(parse_cpu(text))

    def test_memory_available_and_old_kernel_fallback(self):
        memory = parse_memory('MemTotal: 1000 kB\nMemAvailable: 400 kB')
        self.assertEqual(memory.total, 1024000)
        self.assertEqual(memory.used, 614400)
        fallback = parse_memory('MemTotal: 1000 kB\nMemFree: 100 kB\nBuffers: 20 kB\nCached: 50 kB')
        self.assertEqual(fallback.available, 170 * 1024)
        self.assertIsNone(parse_memory('MemTotal: nope kB'))
        self.assertIsNone(parse_memory('MemTotal: 0 kB'))

    def test_package_inventory_excludes_not_installed_and_bad_rows(self):
        rows = parse_packages('zlib1g:amd64\t1.2.3\tinstalled\n'
                              'old-package\t1\tconfig-files\n'
                              'apt\t2.6\tinstalled\nbad row\n'
                              '<tag>\t1\tinstalled\n')
        self.assertEqual([p.name for p in rows], ['apt', 'zlib1g:amd64'])

    def test_package_query_is_fixed_and_bounded(self):
        with patch('umumay.core.subprocess.run') as run:
            run.return_value.stdout = 'apt\t2.6\tinstalled\n'
            self.assertEqual(installed_packages()[0].name, 'apt')
            args, kw = run.call_args
            self.assertEqual(args[0][0], '/usr/bin/dpkg-query')
            self.assertFalse(kw.get('shell', False))
            self.assertEqual(kw['timeout'], 10)
        with patch('umumay.core.subprocess.run', side_effect=FileNotFoundError):
            with self.assertRaises(RuntimeError):
                installed_packages()

    def test_missing_proc_files_do_not_crash(self):
        with tempfile.TemporaryDirectory() as root:
            snapshot = collect_snapshot(proc_root=Path(root), os_release=Path(root) / 'missing')
        self.assertIsNone(snapshot.cpu_percent)
        self.assertIsNone(snapshot.memory)
        self.assertIsNone(snapshot.uptime_seconds)


if __name__ == '__main__':
    unittest.main()
