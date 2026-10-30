# SPDX-License-Identifier: GPL-3.0-or-later
"""Local read-only metrics. No identities, process inspection or network I/O."""

import os
import re
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Release:
    distribution: str
    family: Optional[int]


@dataclass(frozen=True)
class Cpu:
    total: int
    idle: int


@dataclass(frozen=True)
class Memory:
    total: int
    available: int

    @property
    def used(self):
        return self.total - self.available


@dataclass(frozen=True)
class Package:
    name: str
    version: str


@dataclass(frozen=True)
class Snapshot:
    release: Release
    cpu: Optional[Cpu]
    cpu_percent: Optional[float]
    memory: Optional[Memory]
    disk_total: Optional[int]
    disk_used: Optional[int]
    uptime_seconds: Optional[int]
    desktop: str
    session: str


def parse_os_release(text):
    values = {}
    for line in text.splitlines():
        key, sep, value = line.partition('=')
        if sep and key in {'ID', 'VERSION_ID'}:
            try:
                words = shlex.split(value, comments=True)
                values[key] = words[0] if len(words) == 1 else ''
            except ValueError:
                pass
    distribution = values.get('ID', '')
    distribution = distribution if distribution in {'pardus', 'debian'} else 'other'
    match = re.fullmatch(r'(21|23|25)(?:\.\d+)*', values.get('VERSION_ID', ''))
    family = int(match.group(1)) if distribution == 'pardus' and match else None
    return Release(distribution, family)


def parse_cpu(text):
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[0] == 'cpu':
            try:
                ticks = [int(n) for n in parts[1:9]]
                if len(ticks) < 4 or any(n < 0 for n in ticks):
                    return None
                idle = ticks[3] + (ticks[4] if len(ticks) > 4 else 0)
                return Cpu(sum(ticks), idle)
            except ValueError:
                return None
    return None


def cpu_percent(before, after):
    if before is None or after is None:
        return None
    total, idle = after.total - before.total, after.idle - before.idle
    if total <= 0 or idle < 0 or idle > total:
        return None
    return round(100.0 * (total - idle) / total, 1)


def parse_memory(text):
    values = {}
    for line in text.splitlines():
        match = re.fullmatch(r'(\w+):\s+(\d+) kB\s*', line)
        if match:
            values[match.group(1)] = int(match.group(2)) * 1024
    total = values.get('MemTotal', 0)
    if total <= 0:
        return None
    available = values.get('MemAvailable')
    if available is None:
        available = sum(values.get(k, 0) for k in ('MemFree', 'Buffers', 'Cached', 'SReclaimable'))
        available -= values.get('Shmem', 0)
    return Memory(total, max(0, min(total, available)))


def parse_packages(text):
    packages = []
    for line in text.splitlines():
        parts = line.split('\t')
        if len(parts) != 3 or parts[2] != 'installed':
            continue
        name, version, _ = parts
        if re.fullmatch(r'[a-z0-9][a-z0-9+.\-]*(?::[a-z0-9]+)?', name) and \
                version and len(version) <= 256 and not any(ord(c) < 32 for c in version):
            packages.append(Package(name, version))
    return sorted(packages, key=lambda p: p.name)


def installed_packages():
    try:
        result = subprocess.run(
            ['/usr/bin/dpkg-query', '-W',
             '-f=${binary:Package}\t${Version}\t${db:Status-Status}\n'],
            check=True, capture_output=True, text=True, encoding='utf-8',
            errors='replace', timeout=10, env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'},
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise RuntimeError('Yerel paket listesi okunamadı (dpkg-query).') from error
    return parse_packages(result.stdout)


def _read(path):
    try:
        # Bound inputs, including malformed proc fixtures; do not enumerate users/processes.
        with Path(path).open(encoding='utf-8', errors='replace') as source:
            return source.read(65536)
    except OSError:
        return ''


def collect_snapshot(previous_cpu=None, proc_root=Path('/proc'), os_release=Path('/etc/os-release')):
    cpu = parse_cpu(_read(proc_root / 'stat'))
    memory = parse_memory(_read(proc_root / 'meminfo'))
    try:
        uptime = max(0, int(float(_read(proc_root / 'uptime').split()[0])))
    except (IndexError, ValueError, OverflowError):
        uptime = None
    try:
        disk = shutil.disk_usage('/')
        total, used = disk.total, disk.used
    except OSError:
        total, used = None, None
    desktops = os.environ.get('XDG_CURRENT_DESKTOP', '').lower().split(':')
    desktop = next((d for d in ('xfce', 'gnome') if d in desktops), 'other')
    session = os.environ.get('XDG_SESSION_TYPE', '')
    if session not in {'x11', 'wayland'}:
        session = 'unknown'
    return Snapshot(parse_os_release(_read(os_release)), cpu, cpu_percent(previous_cpu, cpu),
                    memory, total, used, uptime, desktop, session)
