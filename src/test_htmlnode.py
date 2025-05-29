import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "string", None, {"test":"A test"})
        self.assertEqual(node.props_to_html(), " test=\"A test\"")

    def test_print_self(self):
        node = HTMLNode("a", "string")
        expected = "Tag: a\nValue: string\n"
        self.assertEqual(node.print_self(), expected)

    def test_print_children(self):
        node = HTMLNode("a", "string")
        node1 = HTMLNode("b", "int")
        node2 = HTMLNode("c", "float", [node, node1])
        node3 = HTMLNode("d", "list", [node2])
        self.assertEqual(node3.print_children(), "Child 1:\nTag: c\nValue: float\nChildren: [Child 1:\nTag: a\nValue: string\nChild 2:\nTag: b\nValue: int\n]")
