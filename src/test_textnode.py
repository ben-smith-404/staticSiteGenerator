import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("another test case", TextType.CODE)
        node2 = TextNode("another test case", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("image", TextType.IMAGE, "testurl")
        node2 = TextNode("image", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode("wow", TextType.LINK, None)
        node2 = TextNode("wow", TextType.LINK, None)
        self.assertEqual(node, node2)
    

if __name__ == "__main__":
    unittest.main()