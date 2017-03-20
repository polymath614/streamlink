import unittest

from streamlink.plugins.myfreecams import MyFreeCams


class TestPluginMyFreeCams(unittest.TestCase):
    def test_can_handle_url(self):
        # should match
        self.assertTrue(MyFreeCams.can_handle_url("http://myfreecams.com/#USERNAME"))
        self.assertTrue(MyFreeCams.can_handle_url("http://www.myfreecams.com/#USERNAME"))
        self.assertTrue(MyFreeCams.can_handle_url("https://myfreecams.com/#USERNAME"))
        self.assertTrue(MyFreeCams.can_handle_url("https://www.myfreecams.com/#USERNAME"))

        # shouldn't match
        self.assertFalse(MyFreeCams.can_handle_url("http://www.myfreecams.com"))
        self.assertFalse(MyFreeCams.can_handle_url("https://www.myfreecams.com"))
