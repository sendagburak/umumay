import unittest

from umumay.notch import NotchState, require_x11_notch


class NotchStateTests(unittest.TestCase):
    def test_hover_mouse_out_and_pin(self):
        notch = NotchState()
        self.assertFalse(notch.expanded)
        notch.hover()
        self.assertTrue(notch.expanded)
        self.assertFalse(notch.try_collapse(pointer_inside=True))
        self.assertTrue(notch.expanded)
        self.assertTrue(notch.try_collapse(pointer_inside=False))
        self.assertFalse(notch.expanded)
        self.assertTrue(notch.toggle_pin())
        self.assertFalse(notch.try_collapse(pointer_inside=False))
        self.assertTrue(notch.expanded)
        notch.escape()
        self.assertFalse(notch.pinned)
        self.assertFalse(notch.expanded)

    def test_unsupported_wayland_never_falls_back_to_fake_notch(self):
        # Native wayland GDK backend is rejected
        with self.assertRaises(RuntimeError):
            require_x11_notch(':0', {'GDK_BACKEND': 'wayland'})
        # Missing display is rejected
        with self.assertRaises(RuntimeError):
            require_x11_notch('', {'XDG_SESSION_TYPE': 'x11'})
        # Valid X11 and XWayland with display is accepted
        require_x11_notch(':0', {'XDG_SESSION_TYPE': 'wayland'})
        require_x11_notch(':99', {'XDG_SESSION_TYPE': 'x11'})
        require_x11_notch('unix/:0', {'XDG_SESSION_TYPE': 'x11'})

    def test_gnome_top_offset(self):
        import os
        from unittest.mock import patch
        from umumay.notch import NotchShell, GNOME_TOP_BAR_HEIGHT

        with patch.dict(os.environ, {'XDG_CURRENT_DESKTOP': 'GNOME'}):
            self.assertEqual(NotchShell._top_offset(None), GNOME_TOP_BAR_HEIGHT)
        with patch.dict(os.environ, {'XDG_CURRENT_DESKTOP': 'XFCE'}):
            self.assertEqual(NotchShell._top_offset(None), 0)
