import unittest

from browser.HTMLParser import HTMLParser


class HTMLParserTestCase(unittest.TestCase):


    def test_attributes(self):
        parser = HTMLParser("<html><body></body></html>")
        tag, attrs = parser.get_attributes("tagname foo=\"Hallo\"")

        self.assertEqual(1, len(attrs))
        self.assertEqual("tagname", tag)
        self.assertTrue("foo" in attrs.keys())

        parser = HTMLParser("<html><body></body></html>")
        _, attrs = parser.get_attributes("tagname foo=\"Hallo\"")

        self.assertTrue("foo" in attrs.keys())



if __name__ == '__main__':
    unittest.main()
