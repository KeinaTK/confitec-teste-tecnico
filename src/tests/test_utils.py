import unittest

from utils import urljoin


class TestUtils(unittest.TestCase):
    def test_urljoin_without_querystrings(self):
        assert urljoin("a", "very", "long", "path") == "a/very/long/path"

    def test_urljoin_with_querystrings(self):
        url = urljoin(
            "a", "very", "long", "path", with_some="querystrings", sort_by="test"
        )

        assert url == "a/very/long/path?with_some=querystrings&sort_by=test"
