import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LISTS = "unordered lists"
    ORDERED_LISTS = "ordered lists"

def block_to_blocktype(block):
    if block[0] == "#":
        return BlockType.HEADING
    elif block[0:3] == "```" == block[-3:]:
        return BlockType.CODE
    elif block[0] == ">":
        return BlockType.QUOTE
    elif block[0:2] == "- ":
        return BlockType.UNORDERED_LISTS
    elif len(re.findall(r"([\d]\. .*?\n)", block)) > 0:
        return BlockType.ORDERED_LISTS
    return BlockType.PARAGRAPH

def strip_markdown_from_block(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return block.strip("# ")
        case BlockType.CODE:
            return block.strip("```\n")
        case BlockType.QUOTE:
            block = block.strip(">")
            block = block.strip("\n")
            block = block.strip(" ")
            return block
        case BlockType.UNORDERED_LISTS:
            list = []
            lines = block.split("\n")
            for line in lines:
                list.append(line.strip("- "))
            return list
        case BlockType.ORDERED_LISTS:
            list = []
            lines = re.findall(r"([\d]\. .*?\n)", block)
            for line in lines:
                to_strip = re.findall(r"([\d]\. )", line)
                line = line.strip(to_strip[0])
                line = line.strip("\n")
                list.append(line)
            return list
        case _:
            raise Exception("Nothing to")
