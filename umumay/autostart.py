# SPDX-License-Identifier: GPL-3.0-or-later
"""Opt-in XDG autostart, with strict ownership and no edits to other desktop entries."""

import os
import shutil
from pathlib import Path

from .branding import APP_ID

ENTRY = ("""[Desktop Entry]
Type=Application
Name=Umumay
Comment=Start Umumay notch on login
Comment[tr]=Oturum açıldığında Umumay çentiğini başlat
Exec=umumay
TryExec=umumay
Icon=umumay
Terminal=false
X-GNOME-Autostart-enabled=true
StartupNotify=false
""").encode('utf-8')


class AutostartError(RuntimeError):
    pass


def autostart_path(config_home=None):
    base = config_home if config_home is not None else os.environ.get('XDG_CONFIG_HOME', '')
    root = Path(base) if base and Path(base).is_absolute() else Path.home() / '.config'
    return root / 'autostart' / (APP_ID + '.desktop')


def _validate_parent(path):
    if path.is_symlink() or path.parent.is_symlink():
        raise AutostartError('Sembolik bağlantı üzerinden otomatik başlatma ayarı değiştirilmez.')
    if path.parent.exists() and (not path.parent.is_dir() or path.parent.stat().st_uid != os.getuid()):
        raise AutostartError('Otomatik başlatma klasörünün sahipliği geçersiz.')


def _ours(path):
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_uid != os.getuid():
            return False
        with path.open('rb') as stream:
            return stream.read(len(ENTRY) + 1) == ENTRY
    except OSError:
        return False


def is_autostart_enabled(path=None):
    target = Path(path) if path is not None else autostart_path()
    return _ours(target)


def set_autostart(enabled, path=None):
    """Only create or remove our exact private desktop file."""
    target = Path(path) if path is not None else autostart_path()
    try:
        _validate_parent(target)
        if enabled:
            if shutil.which('umumay') is None:
                raise AutostartError('Otomatik başlatma için önce Umumay .deb paketini kurun.')
            if target.exists() or target.is_symlink():
                if _ours(target):
                    return True
                raise AutostartError('Mevcut otomatik başlatma girdisi güvenle değiştirilemiyor.')
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
            handle = os.open(target, flags, 0o600)
            with os.fdopen(handle, 'wb') as stream:
                os.fchmod(stream.fileno(), 0o600)
                stream.write(ENTRY)
                stream.flush()
                os.fsync(stream.fileno())
            return True
        if target.exists() or target.is_symlink():
            if not _ours(target):
                raise AutostartError('Başka bir otomatik başlatma girdisi silinmedi.')
            target.unlink()
        return False
    except OSError as error:
        raise AutostartError('Otomatik başlatma ayarı güncellenemedi.') from error
