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
        with self.assertRaises(RuntimeError):
            require_x11_notch(':0', {'XDG_SESSION_TYPE': 'wayland'})
        with self.assertRaises(RuntimeError):
            require_x11_notch('', {'XDG_SESSION_TYPE': 'x11'})
        require_x11_notch(':99', {'XDG_SESSION_TYPE': 'x11'})
        require_x11_notch('unix/:0', {'XDG_SESSION_TYPE': 'x11'})
