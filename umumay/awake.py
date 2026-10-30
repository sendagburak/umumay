# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded idle-inhibitor lifecycle; no permanent OS preference changes."""

import time


class AwakeController:
    def __init__(self, backend, clock=time.monotonic):
        self.backend = backend
        self.clock = clock
        self._token = None
        self.deadline = None

    @property
    def active(self):
        return self._token is not None

    @property
    def remaining(self):
        return max(0, int(self.deadline - self.clock())) if self.active else 0

    def start(self, minutes):
        if type(minutes) is not int or not 1 <= minutes <= 480:
            raise ValueError('Süre 1–480 dakika arasında tam sayı olmalı.')
        if self.active:
            raise RuntimeError('Zaten etkin; önce durdurun.')
        token = self.backend.acquire()
        if token is None:
            raise RuntimeError('Oturum uyanık tutma isteğini kabul etmedi.')
        self._token = token
        self.deadline = self.clock() + minutes * 60

    def stop(self):
        if self.active:
            self.backend.release(self._token)
            self._token = None
            self.deadline = None

    def tick(self):
        if self.active and self.clock() >= self.deadline:
            self.stop()
