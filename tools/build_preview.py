#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Portable preview only. Release builds must use dpkg-buildpackage on Linux."""
import gzip
import hashlib
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1.4'
EPOCH = 1793394000
SOURCE_ROOTS = {'umumay', 'data', 'debian', 'docs', 'tests', 'tools', '.github',
                '.devcontainer', '.vscode', 'setup.py', 'LICENSE', 'README.md',
                'README.en.md', 'CONTRIBUTING.md', 'SECURITY.md', '.gitignore', '.dockerignore'}


def tar_bytes(files):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, content, mode in sorted(files):
            item = tarfile.TarInfo(name)
            item.size, item.mode, item.mtime = len(content), mode, EPOCH
            item.uid = item.gid = 0
            item.uname = item.gname = 'root'
            archive.addfile(item, io.BytesIO(content))
    return gzip.compress(buffer.getvalue(), mtime=0)


def build():
    destination = ROOT / 'dist'
    destination.mkdir(exist_ok=True)
    launcher = b'#!/usr/bin/python3\nfrom umumay.__main__ import main\nraise SystemExit(main())\n'
    files = [('usr/bin/umumay', launcher, 0o755)]
    for path in sorted((ROOT / 'umumay').iterdir()):
        if path.suffix == '.py' or path.name in {'privacy_tr.txt', 'privacy_en.txt',
                                               'umumay.png', 'io.github.sendagburak.umumay.desktop'}:
            files.append(('usr/lib/python3/dist-packages/umumay/' + path.name, path.read_bytes(), 0o644))
    for source, target in [
        ('umumay/io.github.sendagburak.umumay.desktop', 'usr/share/applications/io.github.sendagburak.umumay.desktop'),
        ('LICENSE', 'usr/share/doc/umumay/LICENSE'),
        ('README.md', 'usr/share/doc/umumay/README.md'),
        ('README.en.md', 'usr/share/doc/umumay/README.en.md'),
        ('SECURITY.md', 'usr/share/doc/umumay/SECURITY.md'),
        ('CONTRIBUTING.md', 'usr/share/doc/umumay/CONTRIBUTING.md'),
        ('debian/copyright', 'usr/share/doc/umumay/copyright'),
    ]:
        files.append((target, (ROOT / source).read_bytes(), 0o644))
    for path in sorted((ROOT / 'data/icons').rglob('*.png')):
        files.append(('usr/share/icons/hicolor/' + path.relative_to(ROOT / 'data/icons').as_posix(),
                      path.read_bytes(), 0o644))
    for path in sorted((ROOT / 'docs').rglob('*')):
        if path.is_file():
            files.append(('usr/share/doc/umumay/' + path.relative_to(ROOT).as_posix(), path.read_bytes(), 0o644))
    for path in sorted((ROOT / 'umumay').glob('privacy_*.txt')):
        files.append(('usr/share/doc/umumay/umumay/' + path.name, path.read_bytes(), 0o644))
    control = ('Package: umumay\nVersion: %s\nArchitecture: all\nSection: utils\n'
               'Priority: optional\nMaintainer: Umumay contributors <76114944+sendagburak@users.noreply.github.com>\n'
               'Depends: python3 (>= 3.9), python3-gi, gir1.2-gtk-3.0\n'
               'Recommends: at-spi2-core, gir1.2-ayatanaappindicator3-0.1\n'
               'Description: Umumay offline desktop utilities (preview)\n'
               ' Independent GTK3 utilities; no accounts, telemetry or network clients.\n' % VERSION).encode()
    archive_path = destination / ('umumay_%s_all.deb' % VERSION)
    with archive_path.open('wb') as out:
        out.write(b'!<arch>\n')
        for name, content in [('debian-binary', b'2.0\n'),
                              ('control.tar.gz', tar_bytes([('control', control, 0o644)])),
                              ('data.tar.gz', tar_bytes(files))]:
            header = '%-16s%-12s%-6s%-6s%-8s%-10s`\n' % (name, EPOCH, 0, 0, '100644', len(content))
            out.write(header.encode('ascii'))
            out.write(content)
            if len(content) % 2:
                out.write(b'\n')
    source_files = []
    for path in sorted(ROOT.rglob('*')):
        relative = path.relative_to(ROOT)
        if not path.is_file() or relative.parts[0] not in SOURCE_ROOTS:
            continue
        if any(p in {'dist', '__pycache__', '.git', '.pybuild', 'build', '.debhelper'}
               or p.endswith('.egg-info') for p in relative.parts):
            continue
        if (relative.parts[:2] == ('debian', 'umumay') or
                any(p.startswith('.env') for p in relative.parts) or
                path.name in {'SKILL.md', 'api_keys.txt', 'credentials.json', 'secrets.json'} or
                path.suffix in {'.pyc', '.deb', '.key', '.pem'}):
            continue
        source_files.append(('umumay-' + VERSION + '/' + relative.as_posix(), path.read_bytes(),
                             0o755 if relative.as_posix() in {'debian/rules', 'tools/build_preview.py'} else 0o644))
    source_path = destination / ('umumay-%s-source.tar.gz' % VERSION)
    source_path.write_bytes(tar_bytes(source_files))
    paths = [archive_path, source_path]
    (destination / 'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in paths))
    for path in paths:
        print(path.name)


if __name__ == '__main__':
    build()
