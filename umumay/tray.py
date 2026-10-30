# SPDX-License-Identifier: GPL-3.0-or-later
"""Optional local notification-area integration; no background process."""

import gi
from gi.repository import Gtk

from .branding import APP_ID, ICON_FILE


class StatusArea:
    def __init__(self, window):
        self.indicator, self.legacy = None, None
        self.menu = Gtk.Menu()
        for title, action in [('Umumay’ı göster / Show Umumay', window.present),
                              ('Çıkış / Quit', window.destroy)]:
            item = Gtk.MenuItem(label=title)
            item.connect('activate', lambda _, callback=action: callback())
            self.menu.append(item)
        self.menu.show_all()
        try:
            gi.require_version('AyatanaAppIndicator3', '0.1')
            from gi.repository import AyatanaAppIndicator3 as Indicator
        except (ImportError, ValueError):
            # ponytail: legacy fallback needs an X11 tray; GNOME needs a host extension.
            self.legacy = Gtk.StatusIcon.new_from_file(str(ICON_FILE))
            self.legacy.set_title('Umumay')
            self.legacy.set_tooltip_text('Umumay')
            self.legacy.connect('activate', lambda *_: window.present())
            self.legacy.connect('popup-menu', self._popup)
        else:
            self.indicator = Indicator.Indicator.new(APP_ID, str(ICON_FILE),
                                                    Indicator.IndicatorCategory.APPLICATION_STATUS)
            self.indicator.set_title('Umumay')
            self.indicator.set_menu(self.menu)
            self.indicator.set_status(Indicator.IndicatorStatus.ACTIVE)

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
