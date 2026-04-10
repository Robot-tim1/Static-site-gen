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
    new_nodes = []
    delimiter_size = len(delimiter)
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            clean_nodes.append(node)
        else:
            new_nodes.append(node)
    
    front_point = 0
    back_point = front_point + delimiter_size
    start_point = 0
    last_start_point = start_point

    for node in clean_nodes:
        stack = [1,1]
        text = node.text
        while front_point != len(text):
            
            if len(stack) % 2 != 0 and text[front_point+1:back_point+1] == delimiter:
                front_point += 1
                back_point = front_point + delimiter_size
                continue

            if back_point == len(text):
                if text[front_point:back_point] == delimiter:
                    new_nodes.append(TextNode(text[start_point:back_point-1], text_type))
                    stack.append(1)
                else:
                    new_nodes.append(TextNode(text[start_point:back_point+1], TextType.TEXT))
                break
            
            if text[front_point:back_point] == delimiter and len(stack) % 2 == 0 and text[back_point] != " ":
                
                if text[start_point:front_point] != "" and text[start_point:front_point] != delimiter:
                    new_nodes.append(TextNode(text[start_point:front_point], TextType.TEXT))
                    stack.append(1)
                    last_start_point = start_point
                    start_point = back_point
            
            elif text[front_point:back_point] == delimiter and len(stack) % 2 != 0:
                
                
                if text[front_point-1] == " " and text[back_point] != " ":
                    new_nodes.pop()
                    stack.append(1)
                    new_nodes.append(TextNode(text[last_start_point:front_point], TextType.TEXT))
                    start_point = front_point

                if text[start_point:back_point].strip(delimiter) != "":
                    new_nodes.append(TextNode(text[start_point:back_point].strip(delimiter), text_type))
                    stack.append(1)
                    last_start_point = start_point
                    start_point = front_point + delimiter_size
                    temp = start_point
                    while text[temp:temp + delimiter_size] == delimiter or text[temp] == delimiter[0]:
                        temp += 1
                    start_point = temp

            front_point += 1
            back_point = front_point + delimiter_size
        
        if len(stack) % 2 != 0:
            raise Exception("invalid Markdown syntax, missing a closing delimiter")
        
    counter = 0
    for node in new_nodes:     
        if node.text_type == TextType.TEXT:
            counter += 1
    if counter == len(new_nodes):
        raise Exception("invalid Markdown syntax, no delimiter pairs")

    return new_nodes

node = TextNode("This is _text_ with a italic _block word_", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "_", TextType.BOLD)
print(new_nodes)