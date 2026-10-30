import io
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BrandingTests(unittest.TestCase):
    def test_desktop_shortcut_is_executable_and_never_replaces_a_file_or_link(self):
        from umumay import branding
        create = getattr(branding, 'create_shortcut', None)
        self.assertTrue(callable(create), 'Explicit desktop shortcut creation is missing')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'Umumay.desktop'
            create(path)
            self.assertIn('Exec=umumay\n', path.read_text())
            self.assertIn('Icon=umumay\n', path.read_text())
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o700)
            path.write_text('keep this')
            with self.assertRaises(FileExistsError):
                create(path)
            self.assertEqual(path.read_text(), 'keep this')
            link = Path(folder) / 'linked.desktop'
            link.symlink_to(path)
            with self.assertRaises(FileExistsError):
                create(link)
            self.assertEqual(path.read_text(), 'keep this')

    def test_built_package_contains_the_logo_and_matching_desktop_identity(self):
        self.assertTrue((ROOT / 'umumay/umumay.png').is_file(), 'Bundled logo is missing')
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'source'
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('dist', '.git', '__pycache__'))
            subprocess.run([sys.executable, 'tools/build_preview.py'], cwd=source,
                           check=True, capture_output=True, timeout=30)
            raw = next((source / 'dist').glob('*.deb')).read_bytes()
            self.assertEqual(raw[:8], b'!<arch>\n')
            offset, payloads = 8, {}
            while offset < len(raw):
                name = raw[offset:offset + 16].decode().strip().rstrip('/')
                size = int(raw[offset + 48:offset + 58])
                payloads[name] = raw[offset + 60:offset + 60 + size]
                offset += 60 + size + size % 2
            with tarfile.open(fileobj=io.BytesIO(payloads['data.tar.gz'])) as archive:
                desktop = archive.extractfile('usr/share/applications/io.github.sendagburak.umumay.desktop').read().decode()
                self.assertIn('StartupWMClass=io.github.sendagburak.umumay', desktop)
                self.assertIn('Icon=umumay\n', desktop)
                logo = archive.extractfile('usr/lib/python3/dist-packages/umumay/umumay.png').read()
                self.assertEqual(logo, (ROOT / 'umumay/umumay.png').read_bytes())
                for size in (16, 22, 24, 32, 48, 64, 128, 256, 512):
                    data = archive.extractfile('usr/share/icons/hicolor/%dx%d/apps/umumay.png' % (size, size)).read()
                    self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
                    self.assertEqual(int.from_bytes(data[16:20], 'big'), size)
                    self.assertEqual(int.from_bytes(data[20:24], 'big'), size)
