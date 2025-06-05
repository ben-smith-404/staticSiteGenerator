import unittest

from blocktype import BlockType, block_to_blocktype

class test_blocktype(unittest.TestCase):
    def test_block_to_blocktype_unordered_list(self):
        block = """- test
- test 2"""
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LISTS)

    def test_block_to_blocktype_ordered_list(self):
        block = """1. test
2. test 2"""
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LISTS)

    def test_block_to_blocktype_heading(self):
            block = "# sdkfnsdf"
            self.assertEqual(block_to_blocktype(block), BlockType.HEADING)

    def test_block_to_blocktype_code(self):
        block = "```sdkfnsdf```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        block = ">sdkfnsdf"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)