import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
):

    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        splitted_nodes = []
        splitted_txt = node.text.split(delimiter)
        if len(splitted_txt) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed properly.")
        for i in range(len(splitted_txt)):
            if splitted_txt[i] == "":
                continue

            if i % 2 == 0:
                splitted_nodes.append(TextNode(splitted_txt[i], TextType.TEXT))
            else:
                splitted_nodes.append(TextNode(splitted_txt[i], text_type))

        result.extend(splitted_nodes)
    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # sample  = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"

    image_regex = r"!\[([^\]]+)\]\(([^\)]+)\)"
    result = re.findall(image_regex, text)
    return result


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # sample  = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)"

    # links_regex = r"(?<!!)\[([^\]]+)\]\((https?://.+?)\)"
    links_regex = r"(?<!!)\[([^\]]+)\]\(([^\)]+)\)"
    result = re.findall(links_regex, text)
    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_images(node.text)
        if len(links) == 0:
            result.append(node)
            continue
        link_text = node.text
        for text, link in links:
            separator = f"![{text}]({link})"
            r = link_text.split(separator, maxsplit=1)
            if len(r) != 2:
                raise ValueError(
                    f"invalid markdown, image markdown format not closed. {r=}"
                )
            link_text = r[1]
            if r[0]:
                text_before = TextNode(r[0], TextType.TEXT)
                result.append(text_before)
            link_before = TextNode(text, TextType.IMAGE, link)
            result.append(link_before)
        if link_text:
            result.append(TextNode(link_text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Splits Textnode that has a link markdown into link node and text node."""
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            result.append(node)
            continue
        link_text = node.text
        for text, link in links:
            separator = f"[{text}]({link})"
            r = link_text.split(
                separator, maxsplit=1
            )  # returns 2 empty list['', ''] if only link in text
            if len(r) != 2:
                raise ValueError(
                    f"invalid markdown, link markdown format not closed. {r=}"
                )
            link_text = r[1]
            if r[0]:
                text_before = TextNode(r[0], TextType.TEXT)
                result.append(text_before)
            link_before = TextNode(text, TextType.LINKS, link)
            result.append(link_before)
        if link_text:
            result.append(TextNode(link_text, TextType.TEXT))
    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    """Each functions returns a list of nodes, while splitting its required function."""
    text_node: list[TextNode] = [TextNode(text, TextType.TEXT)]
    bold_arr: list[TextNode] = split_nodes_delimiter(
        text_node, "**", TextType.BOLD_TEXT
    )
    italic_arr: list[TextNode] = split_nodes_delimiter(
        bold_arr, "_", TextType.ITALIC_TEXT
    )
    code_arr: list[TextNode] = split_nodes_delimiter(
        italic_arr, "`", TextType.CODE_TEXT
    )
    image_arr: list[TextNode] = split_nodes_image(code_arr)
    link_arr: list[TextNode] = split_nodes_link(image_arr)

    return link_arr


if __name__ == "__main__":
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    print(new_nodes)
