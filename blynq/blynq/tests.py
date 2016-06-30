from django.test import TestCase

from blynq.settings import DEBUG, MEDIA_HOST, ALLOWED_HOSTS


class SettingsTest(TestCase):
    def test_hosts(self):
        if DEBUG:
            self.assertEqual(MEDIA_HOST, 'http://127.0.0.1:8000')
            self.assertEqual(ALLOWED_HOSTS, [])
        else:
            self.assertEqual(MEDIA_HOST, 'http://www.blynq.in')
            self.assertEqual(ALLOWED_HOSTS, ['http://www.blynq.in', 'www.blynq.in', 'blynq.in'])