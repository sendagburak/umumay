import unittest

from umumay.links import clean_url
from umumay.awake import AwakeController


class UrlTests(unittest.TestCase):
    def test_tracking_removed_other_query_bytes_and_fragment_preserved(self):
        raw = 'https://example.test/a?q=a%20b&q=x+y&utm_source=mail&gclid=123#here'
        self.assertEqual(clean_url(raw), 'https://example.test/a?q=a%20b&q=x+y#here')

    def test_encoded_and_uppercase_tracking_keys_removed(self):
        self.assertEqual(clean_url('https://example.test/?UTM_MEDIUM=x&%66bclid=y&a=1'),
                         'https://example.test/?a=1')

    def test_signed_link_is_unchanged(self):
        url = 'https://example.test/?X-Amz-Signature=abc&utm_source=signed'
        self.assertEqual(clean_url(url), url)

    def test_invalid_or_credential_urls_are_rejected(self):
        for url in ['', 'javascript:alert(1)', 'file:///etc/passwd', 'https://',
                    'https://user:secret@example.test', 'https://example.test:bad',
                    'https://example.test/\nsecret', 'https://example.test/' + 'x' * 8192]:
            with self.subTest(url=url[:50]), self.assertRaises(ValueError):
                clean_url(url)

    def test_unicode_link_is_local_and_preserved(self):
        self.assertEqual(clean_url('https://örnek.test/ç?utm_source=x'), 'https://örnek.test/ç')


class Backend:
    def __init__(self):
        self.acquired = 0
        self.released = []

    def acquire(self):
        self.acquired += 1
        return 0  # zero is a valid D-Bus cookie

    def release(self, cookie):
        self.released.append(cookie)


class AwakeTests(unittest.TestCase):
    def setUp(self):
        self.now = 100.0
        self.backend = Backend()
        self.controller = AwakeController(self.backend, clock=lambda: self.now)

    def test_zero_cookie_active_and_released_on_timeout(self):
        self.controller.start(15)
        self.assertTrue(self.controller.active)
        self.now += 901
        self.controller.tick()
        self.assertFalse(self.controller.active)
        self.assertEqual(self.backend.released, [0])

    def test_double_start_does_not_leak_inhibitor(self):
        self.controller.start(15)
        with self.assertRaises(RuntimeError):
            self.controller.start(30)
        self.assertEqual(self.backend.acquired, 1)

    def test_stop_is_idempotent(self):
        self.controller.start(15)
        self.controller.stop()
        self.controller.stop()
        self.assertEqual(self.backend.released, [0])

    def test_invalid_duration_never_calls_backend(self):
        for duration in [0, -1, 481, True, 1.5]:
            with self.assertRaises(ValueError):
                self.controller.start(duration)
        self.assertEqual(self.backend.acquired, 0)

    def test_unavailable_backend_never_shows_success(self):
        def fail():
            raise RuntimeError('unavailable')
        self.backend.acquire = fail
        with self.assertRaises(RuntimeError):
            self.controller.start(15)
        self.assertFalse(self.controller.active)

    def test_release_failure_remembers_cookie_for_retry(self):
        self.controller.start(15)
        original = self.backend.release
        self.backend.release = lambda cookie: (_ for _ in ()).throw(RuntimeError('failed'))
        with self.assertRaises(RuntimeError):
            self.controller.stop()
        self.assertTrue(self.controller.active)
        self.backend.release = original
        self.controller.stop()
        self.assertFalse(self.controller.active)
