# SPDX-License-Identifier: GPL-3.0-or-later
"""X11 top-centre hover notch. Never silently substitute a regular window on Wayland."""

import os
import re

COLLAPSED_WIDTH = 156
COLLAPSED_HEIGHT = 30
PANEL_WIDTH = 640
PANEL_HEIGHT = 480
HOVER_DELAY_MS = 95
CLOSE_GRACE_MS = 430
GNOME_TOP_BAR_HEIGHT = 32


def require_x11_notch(display_name, environ=None):
    """Require an actual local X11 or XWayland session; native Wayland placement is unsupported."""
    env = os.environ if environ is None else environ
    # Native Wayland backend is not supported for absolute top-centre notch positioning,
    # but Wayland sessions running XWayland (GDK_BACKEND=x11) are supported.
    if env.get('GDK_BACKEND', '').lower() == 'wayland':
        raise RuntimeError('Umumay çentik modu yerel Wayland protokolü yerine XWayland gerektirir. '
                           'GDK_BACKEND=x11 kullanarak başlatın.')
    if not display_name or not re.fullmatch(r'(?:(?:unix/?)?:)?\d+(?:\.\d+)?', display_name):
        raise RuntimeError('Umumay çentik modu yerel X11/XWayland ekranı gerektiriyor (örn. :0).')


class NotchState:
    """Tiny, deterministic interaction policy, independent of GTK and testable offline."""

    def __init__(self):
        self.expanded = False
        self.pinned = False

    def hover(self):
        self.expanded = True
        return self.expanded

    def toggle_pin(self):
        self.pinned = not self.pinned
        self.expanded = True
        return self.pinned

    def try_collapse(self, pointer_inside=False):
        if self.pinned or pointer_inside:
            return False
        self.expanded = False
        return True

    def escape(self):
        self.pinned = False
        self.expanded = False


class NotchShell:
    """GTK3/X11 controller: no decorations, compact always-on-top handle, hover expansion."""

    def __init__(self, window, content, icon_file):
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gdk, GdkPixbuf, GLib, Gtk

        self.Gdk, self.GLib, self.Gtk = Gdk, GLib, Gtk
        self.window = window
        self.state = NotchState()
        self._open_source = None
        self._close_source = None
        self._position_source = None
        self._screen_handler = None
        self._destroyed = False

        window.set_decorated(False)
        window.set_resizable(False)
        window.set_keep_above(True)
        window.set_skip_taskbar_hint(True)
        window.set_skip_pager_hint(True)
        window.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        window.set_accept_focus(True)
        window.set_default_size(COLLAPSED_WIDTH, COLLAPSED_HEIGHT)
        window.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK |
                          Gdk.EventMask.LEAVE_NOTIFY_MASK |
                          Gdk.EventMask.KEY_PRESS_MASK)
        window.connect('enter-notify-event', self._enter)
        window.connect('leave-notify-event', self._leave)
        window.connect('key-press-event', self._key)

        css = Gtk.CssProvider()
        css.load_from_data(b"""
            .umumay-notch-shell {
                background-color: #141b27;
                color: #f1f5fa;
                border: 1px solid #35445b;
                border-radius: 0 0 18px 18px;
            }
            .umumay-notch-handle {
                background-color: #101620;
                color: #f7f9fc;
                border-radius: 0 0 16px 16px;
            }
            .umumay-notch-handle label { color: #f7f9fc; }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            window.get_screen(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.shell = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.shell.get_style_context().add_class('umumay-notch-shell')
        self.handle = Gtk.EventBox()
        self.handle.get_style_context().add_class('umumay-notch-handle')
        self.handle.set_size_request(COLLAPSED_WIDTH, COLLAPSED_HEIGHT)
        self.handle.set_visible_window(True)
        self.handle.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                               Gdk.EventMask.ENTER_NOTIFY_MASK |
                               Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self.handle.connect('button-press-event', self._click)
        self.handle.connect('enter-notify-event', self._enter)
        self.handle.connect('leave-notify-event', self._leave)
        line = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        line.set_halign(Gtk.Align.CENTER)
        line.set_valign(Gtk.Align.CENTER)
        self.logo = Gtk.Image.new_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_scale(str(icon_file), 18, 18, True))
        line.pack_start(self.logo, False, False, 0)
        self.handle_label = Gtk.Label(label='Umumay  ▾')
        line.pack_start(self.handle_label, False, False, 0)
        self.handle.add(line)
        self.shell.pack_start(self.handle, False, False, 0)

        self.panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.panel.pack_start(content, True, True, 0)
        self.shell.pack_start(self.panel, True, True, 0)
        window.add(self.shell)

        # Show descendants while their parent is hidden; don't reshow disabled modules.
        self.panel.show_all()
        self.panel.hide()
        self.panel.set_no_show_all(True)

        self.screen = window.get_screen()
        self._screen_handler = self.screen.connect('monitors-changed', self._monitors_changed)

    def after_show(self):
        self.window.resize(COLLAPSED_WIDTH, COLLAPSED_HEIGHT)
        self._schedule_position()

    def _monitor_geometry(self):
        display = self.Gdk.Display.get_default()
        monitor = display.get_primary_monitor() or display.get_monitor(0)
        return monitor.get_geometry()

    def _top_offset(self):
        desktops = os.environ.get('XDG_CURRENT_DESKTOP', '').lower().split(':')
        if any(d in desktops for d in ('gnome', 'ubuntu:gnome')):
            return GNOME_TOP_BAR_HEIGHT
        return 0

    def _target_geometry(self):
        monitor = self._monitor_geometry()
        y_offset = self._top_offset()
        if self.state.expanded:
            width = min(PANEL_WIDTH, max(COLLAPSED_WIDTH, monitor.width - 24))
            height = min(PANEL_HEIGHT, max(170, monitor.height - y_offset - 48))
        else:
            width, height = COLLAPSED_WIDTH, COLLAPSED_HEIGHT
        x = monitor.x + (monitor.width - width) // 2
        y = monitor.y + y_offset
        return x, y, width, height

    def _schedule_position(self):
        if self._position_source is not None:
            self.GLib.source_remove(self._position_source)
        self._position_source = self.GLib.idle_add(self._position)

    def _position(self):
        self._position_source = None
        if self._destroyed:
            return False
        x, y, width, height = self._target_geometry()
        if self.state.expanded:
            self.panel.set_size_request(width, height - COLLAPSED_HEIGHT)
        self.window.resize(width, height)
        self.window.move(x, y)
        return False

    def _monitors_changed(self, *_):
        self._schedule_position()

    def _cancel(self, name):
        source = getattr(self, name)
        if source is not None:
            self.GLib.source_remove(source)
            setattr(self, name, None)

    def _is_inside(self):
        try:
            pointer = self.Gdk.Display.get_default().get_default_seat().get_pointer()
            _, x, y = pointer.get_position()
            wx, wy = self.window.get_position()
            width, height = self.window.get_size()
            return wx <= x < wx + width and wy <= y < wy + height
        except (AttributeError, TypeError):
            return False

    def _enter(self, _widget, _event):
        self._cancel('_close_source')
        if not self.state.expanded and self._open_source is None:
            self._open_source = self.GLib.timeout_add(HOVER_DELAY_MS, self._delayed_open)
        return False

    def _delayed_open(self):
        self._open_source = None
        if not self._destroyed and self._is_inside():
            self.expand()
        return False

    def _leave(self, _widget, _event):
        self._cancel('_open_source')
        if not self.state.pinned and self._close_source is None:
            self._close_source = self.GLib.timeout_add(CLOSE_GRACE_MS, self._delayed_close)
        return False

    def _delayed_close(self):
        self._close_source = None
        if not self._destroyed and self.state.try_collapse(self._is_inside()):
            self._apply_view()
        return False

    def _click(self, _widget, event):
        if event.button != 1:
            return False
        self._cancel('_open_source')
        self._cancel('_close_source')
        self.state.toggle_pin()
        self._apply_view()
        return True

    def _key(self, _widget, event):
        if event.keyval == self.Gdk.KEY_Escape:
            self._cancel('_open_source')
            self._cancel('_close_source')
            self.state.escape()
            self._apply_view()
            return True
        return False

    def expand(self, pin=False):
        if pin and not self.state.pinned:
            self.state.toggle_pin()
        else:
            self.state.hover()
        self._cancel('_close_source')
        self._apply_view()

    def _apply_view(self):
        if self.state.expanded:
            self.panel.set_no_show_all(False)
            self.panel.show()
        else:
            self.panel.hide()
            self.panel.set_size_request(-1, -1)
            self.panel.set_no_show_all(True)
        self.handle_label.set_text('Umumay  ' + ('●' if self.state.pinned else '▴' if self.state.expanded else '▾'))
        self._schedule_position()

    def close(self):
        self._destroyed = True
        for name in ('_open_source', '_close_source', '_position_source'):
            self._cancel(name)
        if self._screen_handler is not None:
            self.screen.disconnect(self._screen_handler)
            self._screen_handler = None
