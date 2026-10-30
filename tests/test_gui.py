"""Real GTK smoke: run on Linux with RUN_GTK_TESTS=1 under Xvfb/D-Bus."""
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch


@unittest.skipUnless(os.environ.get('RUN_GTK_TESTS') == '1', 'Linux GTK/Xvfb required')
class GuiTests(unittest.TestCase):
    def test_first_run_privacy_local_tools_and_module_switch(self):
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import GLib, Gtk
        from umumay.ui import UtilityApp
        from umumay.storage import SettingsStore
        from umumay.branding import APP_ID
        self.assertTrue(Gtk.init_check()[0], 'GTK display required; do not silently skip CI')
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'XDG_CONFIG_HOME': folder}):
            app = UtilityApp()
            self.assertTrue(app.register(None))
            app.activate()
            self.addCleanup(app.window.destroy)
            self.assertEqual(app.get_application_id(), APP_ID)
            self.assertIsNotNone(app.window.get_icon())
            self.assertEqual(app.brand_image.get_pixbuf().get_width(), 48)
            self.assertEqual(len(app.tray.menu.get_children()), 2)
            self.assertTrue(app.tray.indicator is not None or app.tray.legacy is not None)
            def capture(name):
                loop = GLib.MainLoop()
                GLib.timeout_add(200, lambda: (loop.quit(), False)[1])
                loop.run()
                directory = os.environ.get('UMUMAY_SCREENSHOT_DIR')
                if directory:
                    destination = Path(directory)
                    destination.mkdir(parents=True, exist_ok=True)
                    # Old GTK/Cairo crashes in gdk_pixbuf_get_from_window; capture via X11.
                    x, y = app.window.get_position()
                    area = '%d,%d,%d,%d' % (x, y, app.window.get_allocated_width(), app.window.get_allocated_height())
                    subprocess.run(['/usr/bin/scrot', '-z', '-a', area,
                                    str(destination / (name + '.png'))], check=True, timeout=10)
            self.assertEqual(app.stack.get_visible_child_name(), 'privacy')
            self.assertIsNone(app.snapshot)
            capture('01-privacy')
            app._enter()
            self.assertIsNotNone(app.snapshot)
            time.sleep(0.05)
            app._tick()
            self.assertIsNotNone(app.snapshot.cpu_percent)
            capture('02-system')
            app.stack.set_visible_child_name('packages')
            deadline = time.monotonic() + 15
            while app.package_loading and time.monotonic() < deadline:
                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)
                time.sleep(0.01)
            self.assertFalse(app.package_loading, 'Package query did not finish')
            self.assertTrue(any(row[0] == 'python3' for row in app.package_list))
            self.assertGreater(len(app.package_list), 0)
            app.search.set_text('python3')
            app.search.emit('search-changed')
            capture('03-packages')
            app.stack.set_visible_child_name('links')
            app.url_input.set_text('https://example.test/?utm_source=test&a=1')
            app._clean_link()
            self.assertEqual(app.url_output.get_text(), 'https://example.test/?a=1')
            capture('04-link-cleaner')
            app.switches['links'].set_active(False)
            self.assertFalse(app.stack.get_child_by_name('links').get_visible())
            self.assertEqual(app.url_input.get_text(), '')
            self.assertEqual(SettingsStore().load(), {'links'})
            # A failed preference write must restore the switch, not crash GTK.
            original = app.store
            target = Path(folder) / 'invalid-settings'
            victim = Path(folder) / 'victim'
            victim.write_text('unchanged')
            target.symlink_to(victim)
            app.store = SettingsStore(target)
            app.switches['awake'].set_active(False)
            self.assertTrue(app.switches['awake'].get_active())
            self.assertEqual(victim.read_text(), 'unchanged')
            app.store = original
            app.stack.set_visible_child_name('awake')
            app._start_awake()
            self.assertFalse(app.awake.active, 'Isolated test bus should have no idle service')
            app.window.destroy()
            self.assertTrue(app.closed)
            self.assertIsNone(app.tray)
