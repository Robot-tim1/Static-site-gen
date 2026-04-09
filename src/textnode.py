from enum import Enum

class TextType(Enum):
    TEXT = "text"
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    clean_nodes = [] 
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            clean_nodes.append(TextNode(node.text, TextType.TEXT, node.url))
        else:
            clean_nodes.append(node)
    
    new_nodes = []
    
    for node in clean_nodes:
        stack = []
        for letter in range(len(node.text)):
            if len(delimiter) > 1:
                if (node.text[letter:letter + len(delimiter)]) == delimiter:
                    stack.append(delimiter)
            elif node.text[letter] == delimiter:
                stack.append(delimiter)
        if len(stack) < 2:
            raise Exception("Delimiter not found")
        text = node.text
        print(text)
        
            
def split_node_helper(text, delimiter):
    pass


node = TextNode("This is text `with a `italic block` word", TextType.TEXT)
split_nodes_delimiter([node], "`", TextType.CODE)