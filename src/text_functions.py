import re

from blocktype import BlockType, block_to_blocktype, strip_markdown_from_block
from parentnode import ParentNode
from textnode import TextNode, TextType
from leafnode import LeafNode
from htmlnode import HTMLNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, 
                                        "alt": text_node.text})
        case _:
            raise Exception("Text type is not set correctly")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text_type_to_add = TextType.TEXT
            split_list = node.text.split(delimiter)
            for item in split_list:
                if item != "":
                    new_nodes.append(TextNode(item, text_type_to_add))
                if text_type_to_add == text_type:
                    text_type_to_add = TextType.TEXT
                else:
                    text_type_to_add = text_type
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            string = node.text
            images = extract_markdown_images(string)
            for image in images:
                image_string = f"![{image[0]}]({image[1]})"
                position = string.find(image_string)
                split_string = string.split(image_string, 1)
                if len(split_string) == 1 and position == 0: #image at start of string
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    string = split_string[0]
                elif len(split_string) == 1 and position != 0: #image at end of string
                    new_nodes.append(TextNode(split_string[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    string = ""
                elif len(split_string) == 2:
                    new_nodes.append(TextNode(split_string[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    string = split_string[1]
            if len(string) > 0:
                new_nodes.append(TextNode(string, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            string = node.text
            for image in extract_markdown_images(string):
                string.replace(f"![{image[0]}]({image[1]})", "")
            links = extract_markdown_links(string)
            for link in links:
                link_string = f"[{link[0]}]({link[1]})"
                position = string.find(link_string)
                split_string = string.split(link_string, 1)
                if len(split_string) == 1 and position == 0: #image at start of string
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    string = split_string[0]
                elif len(split_string) == 1 and position != 0: #image at end of string
                    new_nodes.append(TextNode(split_string[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    string = ""
                elif len(split_string) == 2:
                    new_nodes.append(TextNode(split_string[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    string = split_string[1]
            if len(string) > 0:
                new_nodes.append(TextNode(string, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text = text.strip('\n')
    text = text.strip()
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        if block != "":
            blocks.append(block.strip())
    return blocks

def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        match block_to_blocktype(block):
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block)))

            case BlockType.HEADING:
                i = 0
                while block[i] == "#":
                    i += 1
                children.append(LeafNode(f"h{i}", strip_markdown_from_block(block, BlockType.HEADING)))

            case BlockType.CODE:
                text_node = TextNode(strip_markdown_from_block(block, BlockType.CODE), TextType.TEXT)
                children.append(ParentNode("pre", [ParentNode("code", [text_node_to_html_node(text_node)])]))

            case BlockType.QUOTE:
                text_node = TextNode(strip_markdown_from_block(block, BlockType.QUOTE), TextType.TEXT)
                children.append(
                    ParentNode("blockquote", [text_node_to_html_node(text_node)])
                )

            case BlockType.UNORDERED_LISTS:
                list = strip_markdown_from_block(block, BlockType.UNORDERED_LISTS)
                children.append(
                    ParentNode("ul", lists_to_html_nodes(list))
                )

            case BlockType.ORDERED_LISTS:
                list = strip_markdown_from_block(block, BlockType.ORDERED_LISTS)
                children.append(
                    ParentNode("ol", lists_to_html_nodes(list))
                )
                
            case _:
                raise Exception("Unknown type")
    return ParentNode("div", children)

def text_to_children(text):
    html_nodes = []
    for text_node in text_to_textnodes(text):
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def lists_to_html_nodes(list):
    nodes = []
    for item in list:
        nodes.append(ParentNode("li", text_to_children(item)))
    return nodes

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:1] == "#" and line[0:2] != "##":
            return line.strip("# ")
    raise Exception("there is no header in this document")