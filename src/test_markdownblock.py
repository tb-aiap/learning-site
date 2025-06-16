import unittest

from markdown_blocks import BlockType, block_to_blocktype, markdown_to_blocks


class TestMarkdownToBlock(unittest.TestCase):

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

    def test_markdown_to_blocks_newlines(self):
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

    def test_markdown_header_to_blocktype(self):
        block = "### This is header."
        result = block_to_blocktype(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_markdown_seven_header_raises_error(self):
        with self.assertRaises(ValueError):
            block = "####### This is header."
            block_to_blocktype(block)

    def test_markdown_improper_header_raises_error(self):
        with self.assertRaises(ValueError):
            block = "##!## This is not a proper header"
            block_to_blocktype(block)

    def test_code_block_to_blocktype(self):
        block = "```\nThis is a code block\n```"
        result = block_to_blocktype(block)
        self.assertEqual(result, BlockType.CODE)

    def test_quote_block_to_blocktype(self):
        block = ">this is a quteblock"
        result = block_to_blocktype(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list_to_block(self):
        block = "- this is an unodered list\n- with items"
        result = block_to_blocktype(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_to_block_error(self):
        with self.assertRaises(ValueError):
            block = "- this is an unodered list\n-with items"
            block_to_blocktype(block)

    def test_ordered_list_to_block(self):
        block = "1. this is an unodered list\n2. with items"
        result = block_to_blocktype(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_to_block_error(self):
        with self.assertRaises(ValueError):
            block = "1. this is an unodered list\n3. with items"
            block_to_blocktype(block)


if __name__ == "__main__":
    unittest.main()
