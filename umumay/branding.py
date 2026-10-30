# SPDX-License-Identifier: GPL-3.0-or-later
"""Bundled desktop identity; never fetched from a service."""

import os
from pathlib import Path

APP_ID = 'io.github.sendagburak.umumay'
ICON_FILE = Path(__file__).with_name('umumay.png')
DESKTOP_FILE = Path(__file__).with_name(APP_ID + '.desktop')


def create_shortcut(path):
    """Explicit user-selected destination; refuse existing files and symlinks."""
    content = DESKTOP_FILE.read_bytes()
    handle = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o700)
    with os.fdopen(handle, 'wb') as stream:
        os.fchmod(stream.fileno(), 0o700)
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
