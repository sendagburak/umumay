# SPDX-License-Identifier: GPL-3.0-or-later
"""Local session-bus idle inhibition, with a private connection for cleanup."""

import os

import gi
gi.require_version('Gio', '2.0')
from gi.repository import Gio, GLib

from .runtime import validate_local_session
from .branding import APP_ID


class IdleBackend:
    def __init__(self):
        self.connection = None

    def _call(self, name, path, interface, method, parameters, reply=None):
        return self.connection.call_sync(name, path, interface, method, parameters, reply,
                                         Gio.DBusCallFlags.NO_AUTO_START, 1500, None)

    def acquire(self):
        validate_local_session()
        address = os.environ.get('DBUS_SESSION_BUS_ADDRESS', '')
        if not address:
            raise RuntimeError('Yerel oturum D-Bus adresi bulunamadı.')
        if self.connection is None or self.connection.is_closed():
            self.connection = Gio.DBusConnection.new_for_address_sync(
                address, Gio.DBusConnectionFlags.AUTHENTICATION_CLIENT |
                Gio.DBusConnectionFlags.MESSAGE_BUS_CONNECTION, None, None)
        backends = [
            ('org.freedesktop.ScreenSaver', '/org/freedesktop/ScreenSaver',
             'org.freedesktop.ScreenSaver', 'UnInhibit', '(ss)', (APP_ID, 'Süreli ekran etkinliği')),
            ('org.xfce.ScreenSaver', '/org/xfce/ScreenSaver',
             'org.xfce.ScreenSaver', 'UnInhibit', '(ss)', (APP_ID, 'Süreli ekran etkinliği')),
            ('org.freedesktop.PowerManagement', '/org/freedesktop/PowerManagement/Inhibit',
             'org.freedesktop.PowerManagement.Inhibit', 'UnInhibit', '(ss)', (APP_ID, 'Süreli boşta kalma engeli')),
            ('org.gnome.SessionManager', '/org/gnome/SessionManager',
             'org.gnome.SessionManager', 'Uninhibit', '(susu)', (APP_ID, 0, 'Süreli ekran etkinliği', 8)),
        ]
        for name, path, interface, stop, signature, values in backends:
            try:
                owner = self._call('org.freedesktop.DBus', '/org/freedesktop/DBus',
                                   'org.freedesktop.DBus', 'GetNameOwner', GLib.Variant('(s)', (name,))).unpack()[0]
                cookie = self._call(owner, path, interface, 'Inhibit',
                                    GLib.Variant(signature, values), GLib.VariantType.new('(u)')).unpack()[0]
                return owner, path, interface, stop, cookie
            except GLib.Error:
                continue
        raise RuntimeError('Bu oturumda desteklenen ekran uyanık tutma hizmeti bulunamadı.')

    def release(self, token):
        owner, path, interface, stop, cookie = token
        try:
            self._call(owner, path, interface, stop, GLib.Variant('(u)', (cookie,)))
        except GLib.Error:
            # Closing our own bus connection also releases its inhibitors.
            self.close()

    def close(self):
        if self.connection is not None:
            try:
                self.connection.close_sync(None)
            except GLib.Error:
                pass
            self.connection = None
