import unittest

from text_functions import extract_title, markdown_to_blocks, markdown_to_html_node, split_nodes_image, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_textnodes
from textnode import TextNode, TextType

class TestFunctions(unittest.TestCase):
    def test_text_type_text(self):
        node = TextNode("testing", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "testing")
        self.assertEqual(html_node.to_html(), "testing")

    def test_text_type_bold(self):
        node = TextNode("testing", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "testing")
        self.assertEqual(html_node.to_html(), "<b>testing</b>")

    def test_text_type_italic(self):
        node = TextNode("testing", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "testing")
        self.assertEqual(html_node.to_html(), "<i>testing</i>")

    def test_text_type_code(self):
        node = TextNode("testing", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "testing")
        self.assertEqual(html_node.to_html(), "<code>testing</code>")

    def test_text_type_link(self):
        node = TextNode("testing", TextType.LINK, "https://test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "testing")
        self.assertEqual(html_node.props, {"href": "https://test.com"})
        self.assertEqual(html_node.to_html(), "<a href=\"https://test.com\">testing</a>")

    def test_text_type_image(self):
        node = TextNode("testing", TextType.IMAGE, "https://test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://test.com",
                                            "alt":"testing"})
        self.assertEqual(html_node.to_html(), "<img src=\"https://test.com\" alt=\"testing\"/>")

    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
    
    def test_split_nodes_italic_with_new_line(self):
        node = TextNode("_test_ and another _test_ what now?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("test", TextType.ITALIC),
            TextNode(" and another ", TextType.TEXT),
            TextNode("test", TextType.ITALIC),
            TextNode(" what now?", TextType.TEXT)
            ])
    
    def test_markdown_image_extraction(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_markdown_extraction_image_with_multiples(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and ![a second image](https://i.imgur.com/zjjcJKsZ.png) "
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), 
                              ("a second image", "https://i.imgur.com/zjjcJKsZ.png")], matches)
    
    def test_markdown_link_extraction(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_markdown_extraction_link_with_multiples(self):
        matches = extract_markdown_links(
            "This is text with a ![link](https://i.imgur.com/zjjcJKZ.png), and ![a second link](https://i.imgur.com/zjjcJKsZ.png) "
            )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), 
                              ("a second link", "https://i.imgur.com/zjjcJKsZ.png")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        self.assertEqual(text_to_textnodes(text), expected_nodes)

    def test_block_splitting(self):
        markdown = "# This is a heading"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks, 
            [
                "# This is a heading"
            ]
        )

    def test_block_splitting_2_lines(self):
        markdown = "# This is a heading\n\ntest"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks, 
            [
                "# This is a heading",
                "test"
            ]
        )
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_extract_title_1(self):
        header = extract_title("#header\n")
        self.assertEqual(header, "header")

    def test_extract_title_2(self):
        header = extract_title("#another header     \nthis is a test")
        self.assertEqual(header, "another header")
    