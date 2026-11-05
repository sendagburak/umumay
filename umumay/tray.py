# SPDX-License-Identifier: GPL-3.0-or-later
"""Optional local tray host; close-to-tray is disabled without a visible host."""

import gi
from gi.repository import Gio, GLib, Gtk

from .branding import APP_ID, ICON_FILE


def _has_watcher():
    """Check a local StatusNotifierWatcher before trusting AppIndicator visibility."""
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        response = bus.call_sync(
            'org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus',
            'NameHasOwner', GLib.Variant('(s)', ('org.kde.StatusNotifierWatcher',)),
            GLib.VariantType.new('(b)'), Gio.DBusCallFlags.NONE, 800, None)
        return bool(response.unpack()[0])
    except GLib.Error:
        return False


class StatusArea:
    def __init__(self, window, on_show=None, on_quit=None):
        self.indicator, self.legacy = None, None
        show = on_show if on_show is not None else window.present
        quit_action = on_quit if on_quit is not None else window.destroy
        self.menu = Gtk.Menu()
        for title, action in [('Umumay çentiğini göster / Show Umumay', show),
                              ('Umumay’dan tamamen çık / Quit Umumay', quit_action)]:
            item = Gtk.MenuItem(label=title)
            item.connect('activate', lambda _, callback=action: callback())
            self.menu.append(item)
        self.menu.show_all()

        indicator_module = None
        try:
            gi.require_version('AyatanaAppIndicator3', '0.1')
            from gi.repository import AyatanaAppIndicator3
            indicator_module = AyatanaAppIndicator3
        except (ImportError, ValueError):
            pass

        if indicator_module is not None and _has_watcher():
            self.indicator = indicator_module.Indicator.new(
                APP_ID, str(ICON_FILE), indicator_module.IndicatorCategory.APPLICATION_STATUS)
            self.indicator.set_title('Umumay')
            self.indicator.set_menu(self.menu)
            self.indicator.set_status(indicator_module.IndicatorStatus.ACTIVE)
        else:
            self.legacy = Gtk.StatusIcon.new_from_file(str(ICON_FILE))
            self.legacy.set_title('Umumay')
            self.legacy.set_tooltip_text('Umumay · sağ tık: Çıkış')
            self.legacy.connect('activate', lambda *_: show())
            self.legacy.connect('popup-menu', self._popup)

    def can_background(self):
        if self.indicator is not None:
            return _has_watcher()
        return self.legacy is not None and bool(self.legacy.is_embedded())

    def _popup(self, icon, button, timestamp):
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, icon, button, timestamp)

    def close(self):
        if self.indicator is not None:
            from gi.repository import AyatanaAppIndicator3 as Indicator
            self.indicator.set_status(Indicator.IndicatorStatus.PASSIVE)
            self.indicator = None
        if self.legacy is not None:
            self.legacy.set_visible(False)
            self.legacy = None
        self.menu.destroy()
