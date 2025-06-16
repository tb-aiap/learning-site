"""Module for converting markdown to html."""

from pathlib import Path

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from markdown_blocks import BlockType, block_to_blocktype, markdown_to_blocks
from raw_to_textnode import text_to_textnodes
from textnode import TextNode, TextType

"""
html that are parentnode
- div 
- ol > li
- ul > li

"""


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:

    dir_path_content: Path = Path(dir_path_content)
    template_path: Path = Path(template_path)
    dest_dir_path: Path = Path(dest_dir_path)

    for file in dir_path_content.iterdir():
        if file.is_file():
            dest_path_html = Path(dest_dir_path, "index.html")
            generate_page(file, template_path, dest_path_html)
        if file.is_dir():
            new_dest_dir = Path(dest_dir_path, file.name)
            generate_pages_recursive(file, template_path, new_dest_dir)

    return


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Creating page from {from_path} to {dest_path} using {template_path}")

    from_path = Path(from_path)
    template_path = Path(template_path)
    dest_path: Path = Path(dest_path)

    with open(from_path, "r") as f:
        content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(content)
    html_content = markdown_to_html_node(content).to_html()

    template_with_title = template.replace("{{ Title }}", title)
    template_content = template_with_title.replace("{{ Content }}", html_content)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_content)

    print(f"Completed creating {dest_path}")


def extract_title(markdown: str) -> str:
    blocks = [t for t in markdown.split("\n") if t]
    if not blocks[0].startswith("# "):
        raise Exception("expecting header 1 as first line.")
    return blocks[0][2:]


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    main_children = []
    for block in blocks:
        b = block_to_blocktype(block)
        if b == BlockType.PARAGRAPH:
            # text = text_to_textnodes(block.replace("\n", " "))
            # children_node = [text_node_to_html_node(t) for t in text]
            children_node = _text_to_children(block.replace("\n", " "))
            main_children.append(ParentNode(tag="p", children=children_node))

        if b == BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError(f"invalid code block: {block}")

            text = block.strip("`").strip() + "\n"
            text_node = TextNode(text=text, text_type=TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            code_node = ParentNode(tag="code", children=[html_node])
            main_children.append(ParentNode(tag="pre", children=[code_node]))

        if b == BlockType.HEADING:
            header_hash, header_text = block.split(" ", maxsplit=1)
            heading_tag = f"h{len(header_hash)}"
            main_children.append(LeafNode(tag=heading_tag, value=header_text))

        if b == BlockType.UNORDERED_LIST:
            li_children = []
            for li in block.split("\n"):
                li_text = li.strip("- ")
                li_html_node = _text_to_children(li.strip("- "))
                li_node = ParentNode(tag="li", children=li_html_node)
                li_children.append(li_node)
            main_children.append(ParentNode(tag="ul", children=li_children))

        if b == BlockType.ORDERED_LIST:
            li_children = []
            for li in block.split("\n"):
                _, li_text = li.split(" ", maxsplit=1)
                li_html_node = _text_to_children(li_text)
                li_node = ParentNode(tag="li", children=li_html_node)
                li_children.append(li_node)
            main_children.append(ParentNode(tag="ol", children=li_children))

        if b == BlockType.QUOTE:
            quote_text = block.replace(">", "").replace("\n", "")[
                1:
            ]  # to remove the first spacing.
            quote_text_node = text_to_textnodes(quote_text)
            quote_html_node = [text_node_to_html_node(t) for t in quote_text_node]
            main_children.append(ParentNode(tag="blockquote", children=quote_html_node))

    return ParentNode(tag="div", children=main_children)


def _text_to_children(text: str) -> list[HTMLNode]:
    """Convert raw text into list of html nodes."""
    text_node = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(t) for t in text_node]
    return html_nodes
