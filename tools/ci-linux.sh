#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
set -eu
EXPECTED_ID="$1" EXPECTED_FAMILY="$2" python3 - <<'PY'
import os, shlex
from pathlib import Path
data = {}
for line in Path('/etc/os-release').read_text().splitlines():
    key, sep, value = line.partition('=')
    if sep:
        words = shlex.split(value)
        data[key] = words[0] if words else ''
assert data['ID'] == os.environ['EXPECTED_ID'], data
assert data['VERSION_ID'].split('.')[0] == os.environ['EXPECTED_FAMILY'], data
print('Verified test image:', data['ID'], data['VERSION_ID'])
PY
desktop-file-validate umumay/io.github.sendagburak.umumay.desktop
python3 -m unittest discover -s tests -v
python3 tools/build_preview.py
dpkg-deb --info dist/umumay_0.1.3_all.deb
dpkg-buildpackage -us -uc -b
dpkg -i ../umumay_0.1.3_all.deb
cd /tmp
/usr/bin/umumay --version
/usr/bin/umumay --report /tmp/report.json
RUN_GTK_TESTS=1 dbus-run-session -- xvfb-run -a \
    strace -f -e trace=network -o /artifacts/gui-network.trace \
    python3 -m unittest discover -s /src/tests -p test_gui.py -v
if grep -E 'sa_family=AF_INET6?' /artifacts/gui-network.trace; then
    echo 'Unexpected IP network operation' >&2
    exit 1
fi
dpkg -r umumay
cp /umumay_0.1.3_all.deb /src/dist/umumay-0.1.3-source.tar.gz /artifacts/
cd /artifacts
sha256sum umumay_0.1.3_all.deb umumay-0.1.3-source.tar.gz > SHA256SUMS
