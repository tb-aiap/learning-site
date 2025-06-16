from enum import Enum


class TextType(Enum):
    TEXT = "normal_text"
    BOLD_TEXT = "bold_text"
    ITALIC_TEXT = "italic_text"
    CODE_TEXT = "code_text"
    LINKS = "url_link"
    IMAGE = "image_link"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"{__class__.__name__}({self.text}, {self.text_type.value}, {self.url})"


if __name__ == "__main__":
    tn = TextNode("something", TextType.WIL_TEXT)
    print(tn)
