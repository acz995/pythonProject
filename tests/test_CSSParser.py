from unittest import TestCase

from browser.CSSParser import CSSParser
from browser.DescendantSelector import DescendantSelector
from browser.TagSelector import TagSelector


class TestCSSParser(TestCase):
    def test_whitespace(self):
        self.fail()

    def test_word(self):
        self.fail()

    def test_literal(self):
        self.fail()

    def test_pair(self):
        self.fail()

    def test_body(self):
        self.fail()

    def test_ignore_until(self):
        self.fail()

    def test_selector(self):
        self.fail()



    def test_parse(self):
        parser = CSSParser("h1 { color: red; }")
        properties = parser.parse()
        self.assertEqual(1, len(properties))
        self.assertEqual("red", properties["color"])
        self.assertTrue("color" in properties.keys())


