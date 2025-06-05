import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("a", "test")
        child2 = LeafNode("b", "test 2")
        node = ParentNode("g", [child1, child2])
        self.assertEqual(
            node.to_html(),
            "<g><a>test</a><b>test 2</b></g>"
        )

    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node1 = LeafNode("b", "grandchild1", {"key":"value", "a":"b"})
        grandchild_node2 = LeafNode("c", "grandchild2")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b key=\"value\" a=\"b\">grandchild1</b><c>grandchild2</c></span></div>"
        )