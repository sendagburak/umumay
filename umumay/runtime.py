# SPDX-License-Identifier: GPL-3.0-or-later
"""Refuse remote GUI/session transports; all desktop IPC must be local."""

import os
import re


def validate_local_session(environ=None):
    env = os.environ if environ is None else environ
    display = env.get('DISPLAY', '')
    if display and not re.fullmatch(r'(?:unix/?)?:\d+(?:\.\d+)?', display):
        raise RuntimeError('Uzak/TCP ekran oturumu desteklenmiyor; yerel XFCE/GNOME kullanın.')
    for key in ['DBUS_SESSION_BUS_ADDRESS', 'DBUS_SYSTEM_BUS_ADDRESS', 'DBUS_STARTER_ADDRESS', 'AT_SPI_BUS_ADDRESS']:
        address = env.get(key, '')
        if address and not all(part.startswith('unix:') for part in address.split(';')):
            raise RuntimeError('Uzak D-Bus adresi reddedildi; yalnız yerel Unix oturumu kullanılabilir.')
