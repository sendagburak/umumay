# SPDX-License-Identifier: GPL-3.0-or-later
"""Only module preferences are persisted automatically. Export is explicit."""

import json
import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path

from . import __version__


@dataclass(frozen=True)
class Module:
    id: str
    title: str
    description: str


MODULES = (
    Module('system', 'Sistem', 'Anlık CPU, bellek ve disk doluluğu'),
    Module('packages', 'Paketler', 'Kurulu paketlerde salt okunur arama'),
    Module('awake', 'Uyanık tut', 'Boşta kalma/güç tasarrufunu süreli ertele'),
    Module('links', 'Bağlantı', 'Elle girilen URL’den takip parametrelerini temizle'),
)
MODULE_IDS = frozenset(m.id for m in MODULES)


class StorageError(RuntimeError):
    pass


def default_settings_path():
    base = os.environ.get('XDG_CONFIG_HOME', '')
    root = Path(base) if base and Path(base).is_absolute() else Path.home() / '.config'
    return root / 'umumay' / 'settings.json'


def _check_target(path):
    if path.is_symlink() or path.parent.is_symlink():
        raise StorageError('Sembolik bağlantıya yazma/okuma reddedildi.')
    if path.exists() and (not path.is_file() or path.stat().st_uid != os.getuid()):
        raise StorageError('Dosya türü veya sahipliği uygun değil.')


def _write_private(path, data):
    path = Path(path)
    temporary = None
    try:
        _check_target(path)
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        handle, temporary = tempfile.mkstemp(prefix='.umumay-', dir=str(path.parent))
        with os.fdopen(handle, 'w', encoding='utf-8') as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        _check_target(path)
        os.replace(temporary, path)
    except (OSError, ValueError, TypeError) as error:
        raise StorageError('Yerel dosya kaydedilemedi.') from error
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


class SettingsStore:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else default_settings_path()

    def load(self):
        try:
            _check_target(self.path)
            if not self.path.exists():
                return set()
            flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
            with os.fdopen(os.open(str(self.path), flags), 'r', encoding='utf-8') as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise StorageError('Ayar dosyası normal dosya değil.')
                raw = stream.read(65537)
            if len(raw) > 65536:
                raise StorageError('Ayar dosyası boyut sınırını aşıyor.')
            data = json.loads(raw)
            if not isinstance(data, dict) or data.get('schema') != 1:
                raise StorageError('Ayar şeması tanınmıyor.')
            disabled = data.get('disabled')
            if not isinstance(disabled, list) or not all(isinstance(x, str) for x in disabled):
                raise StorageError('Modül tercihleri geçersiz.')
            if not set(disabled) <= MODULE_IDS:
                raise StorageError('Bilinmeyen modül kimliği.')
            return set(disabled)
        except (OSError, ValueError, UnicodeError) as error:
            raise StorageError('Ayarlar okunamadı; varsayılanlar kullanılabilir.') from error

    def save(self, disabled):
        if not isinstance(disabled, (set, frozenset)) or not disabled <= MODULE_IDS:
            raise StorageError('Bilinmeyen modül kimliği.')
        _write_private(self.path, {'schema': 1, 'disabled': sorted(disabled)})


def report_data(snapshot):
    memory = snapshot.memory
    return {
        'schema': 1,
        'app_version': __version__,
        'platform': {'distribution': snapshot.release.distribution, 'pardus_family': snapshot.release.family},
        'session': {'desktop': snapshot.desktop, 'type': snapshot.session},
        'metrics': {
            'cpu_percent': snapshot.cpu_percent,
            'memory_total_bytes': memory.total if memory else None,
            'memory_used_bytes': memory.used if memory else None,
            'disk_total_bytes': snapshot.disk_total,
            'disk_used_bytes': snapshot.disk_used,
            'uptime_seconds': snapshot.uptime_seconds,
        },
    }


def write_report(path, snapshot):
    _write_private(path, report_data(snapshot))
