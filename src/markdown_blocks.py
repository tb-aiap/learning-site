"""Modules for processing markdown raw text."""

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    """Process markdown text to blocks."""
    result = [t.strip() for t in text.split("\n\n") if t]
    return result


def block_to_blocktype(block: str) -> BlockType:
    if block.startswith("#"):
        header, _ = block.split(" ", maxsplit=1)
        if len(set(header)) != 1:
            raise ValueError(f"expecting header # but received {header}")
        if len(header) > 6:
            raise ValueError(f"expecting header # up to 6, but received more {header}")
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        each_line = block.split("\n")
        for line in each_line:
            if not line.startswith(">"):
                raise ValueError(
                    "expecting quote > in each line." f"but received {line}"
                )
        return BlockType.QUOTE

    if block.startswith("- "):
        each_line = block.split("\n")
        for line in each_line:
            if not line.startswith("- "):
                raise ValueError(
                    "expecting unordered - in each line." f"but received {line}"
                )
        return BlockType.UNORDERED_LIST

    if block.startswith("1."):
        each_line = block.split("\n")
        i = 1
        ordered_arr = []
        for line in each_line:
            order_num = str(i) + "."
            ordered_arr.append(order_num)
            if not line.startswith(order_num):
                raise ValueError(
                    "expecting ordered number in each line."
                    f"but received {ordered_arr}"
                )
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
