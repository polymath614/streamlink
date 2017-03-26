import unittest

from streamlink.plugins.myfreecams import MyFreeCams


class TestPluginMyFreeCams(unittest.TestCase):
    def test_can_handle_url(self):
        # should match - username url
        self.assertTrue(MyFreeCams.can_handle_url("http://myfreecams.com/#USERNAME"))
        self.assertTrue(MyFreeCams.can_handle_url("http://www.myfreecams.com/#USERNAME"))
        self.assertTrue(MyFreeCams.can_handle_url("https://myfreecams.com/#USERNAME"))
        self.assertTrue(MyFreeCams.can_handle_url("https://www.myfreecams.com/#USERNAME"))

        # should match - custom userid url
        self.assertTrue(MyFreeCams.can_handle_url("http://myfreecams.com/id=61234567"))
        self.assertTrue(MyFreeCams.can_handle_url("http://www.myfreecams.com/id=71234567"))
        self.assertTrue(MyFreeCams.can_handle_url("https://myfreecams.com/id=81234567"))
        self.assertTrue(MyFreeCams.can_handle_url("https://www.myfreecams.com/id=91234567"))

        # shouldn't match
        self.assertFalse(MyFreeCams.can_handle_url("http://www.myfreecams.com"))
        self.assertFalse(MyFreeCams.can_handle_url("https://www.myfreecams.com"))
        self.assertFalse(MyFreeCams.can_handle_url("https://www.myfreecams.com/#"))
        self.assertFalse(MyFreeCams.can_handle_url("https://www.myfreecams.com/id="))
