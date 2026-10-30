import sys
import time
from gi.repository import GLib
from umumay.awake import AwakeController
from umumay.desktop import IdleBackend

kind = sys.argv[1]
backend = IdleBackend()
now = [0]
controller = AwakeController(backend, clock=lambda: now[0])
deadline = time.monotonic() + 12
try:
    while True:
        try:
            controller.start(1)
            break
        except (RuntimeError, GLib.Error):
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.2)
    token = controller._token
    expected = {'org.gnome.SessionManager'} if kind == 'gnome' else {'org.xfce.ScreenSaver', 'org.freedesktop.ScreenSaver', 'org.freedesktop.PowerManagement.Inhibit'}
    assert token[2] in expected, token
    assert controller.active
    if kind == 'gnome':
        assert backend._call(token[0], token[1], token[2], 'IsInhibited', GLib.Variant('(u)', (8,))).unpack()[0]
    elif token[2] == 'org.freedesktop.PowerManagement.Inhibit':
        assert backend._call(token[0], token[1], token[2], 'HasInhibit', None).unpack()[0]
    now[0] = 61
    controller.tick()
    assert not controller.active
    if kind == 'gnome':
        assert not backend._call(token[0], token[1], token[2], 'IsInhibited', GLib.Variant('(u)', (8,))).unpack()[0]
    elif token[2] == 'org.freedesktop.PowerManagement.Inhibit':
        assert not backend._call(token[0], token[1], token[2], 'HasInhibit', None).unpack()[0]
    print(kind + ': real D-Bus acquisition, timed release and cleanup passed')
finally:
    controller.stop()
    backend.close()
