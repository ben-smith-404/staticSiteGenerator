import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_p_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_a_to_html_p(self):
        node = LeafNode("a", "Hello, world!", {"link":"test", "style":"align"})
        self.assertEqual(node.to_html(), "<a link=\"test\" style=\"align\">Hello, world!</a>")

    def test_strong_to_html_p(self):
        node = LeafNode("strong", "Hello, world!")
        self.assertEqual(node.to_html(), "<strong>Hello, world!</strong>")

    def test_i_to_html_p(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")
            
    def test_no_tag_to_html_p(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")