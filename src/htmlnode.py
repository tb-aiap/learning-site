"""Module for creating HTML Parent and Leaf nodes."""

from __future__ import annotations

from textnode import TextNode, TextType


class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list[HTMLNode] = None,
        props: dict[str, str] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        """Return a dict[str, str] into html properties."""
        if self.props is None:
            return ""
        return "".join([f" {k}={v}" for k, v in self.props.items()])

    def __repr__(self):
        """ "Print properties for htmlNode."""
        print(f"{self.tag=}{self.value=}{self.children=}{self.props=}")


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag=None,
        value=None,
        props=None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value.")

        # self.value = self.value.replace("\n", " ")
        if self.tag is None:
            return str(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag,
        children,
        props=None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag cannot be none.")
        if self.children is None:
            raise ValueError("children cannot be none for parent node.")

        result_start = f"<{self.tag}{self.props_to_html()}>"
        result = ""
        result_end = f"</{self.tag}>"
        for child in self.children:
            result += child.to_html()

        return result_start + result + result_end


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    """Convert a text node into html node."""
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE_TEXT:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINKS:
        return LeafNode("a", text_node.text, props={"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"invalid text type: {text_node.text_type}")
