from enum import Enum
import re

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
    
    new_nodes = [[]]
    delimiter_size = len(delimiter)
    counter = -1

    for clean_node in old_nodes:
        if clean_node.text_type != TextType.TEXT:
            new_nodes[counter].append(clean_node)
            continue
        counter += 1
        stack = [1,1]
        front_point = 0
        back_point = front_point + delimiter_size
        start_point = 0
        last_start_point = start_point
        text = clean_node.text
        
        if len(new_nodes) <= counter:
            new_nodes.append([])
        
        while front_point != len(text):
            
            if len(stack) % 2 != 0 and text[front_point+1:back_point+1] == delimiter:
                front_point += 1
                back_point = front_point + delimiter_size
                continue

            if back_point == len(text):
                if text[front_point:back_point] == delimiter:
                    new_nodes[counter].append(TextNode(text[start_point:back_point-1].strip(delimiter), text_type))
                    stack.append(1)
                else:
                    new_nodes[counter].append(TextNode(text[start_point:back_point+1], TextType.TEXT))
                break
            
            if text[front_point:back_point] == delimiter and len(stack) % 2 == 0 and text[back_point] != " ":
                
                if delimiter in text[start_point:front_point]:
                    temp = start_point
                    for i in text[temp:front_point]:
                        start_point += 1
                new_nodes[counter].append(TextNode(text[start_point:front_point], TextType.TEXT))
                stack.append(1)
                last_start_point = start_point
                start_point = back_point
            
            elif text[front_point:back_point] == delimiter and len(stack) % 2 != 0:
                
                if text[front_point-1] == " " and text[back_point] != " ":
                    new_nodes[counter].pop()
                    stack.append(1)
                    new_nodes[counter].append(TextNode(text[last_start_point:front_point], TextType.TEXT))
                    start_point = front_point

                elif text[start_point:back_point].strip(delimiter) != "":
                    new_nodes[counter].append(TextNode(text[start_point:back_point].strip(delimiter), text_type))
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
        
        if new_nodes[counter][0].text == "":
            del new_nodes[counter][0]
        
        if len(new_nodes) > 1:
            for i in range(1, len(new_nodes)):     
                new_nodes[0].extend(new_nodes[1])
                del new_nodes[1]
                counter -= 1      

    counter2 = 0
    for node in new_nodes[0]:
        if node.text_type == TextType.TEXT:
            counter2 += 1
    if counter2 == len(new_nodes[0]):
        raise Exception("invalid, no things to delimit here")
 
    return new_nodes[0]

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    
    new_nodes = [[]]
    node_counter = -1

    for node in old_nodes:

        node_counter += 1
        text = node.text
        
        if len(new_nodes) <= node_counter:
            new_nodes.append([])

        if extract_markdown_links(text) == []:
            new_nodes[node_counter].append(TextNode(text, node.text_type, node.url))
            continue
        
        while extract_markdown_links(text) != []:
            
            matches = extract_markdown_links(text)
            link_text = matches[0][0]
            link = matches[0][1]
            delimiter = f"[{link_text}]({link})"
            sections = text.split(delimiter, 1)
            
            if sections[0] != "":
                new_nodes[node_counter].append(TextNode(sections[0], node.text_type))
            new_nodes[node_counter].append(TextNode(link_text, TextType.LINK, link))
            
            text = sections[1]
        if text != "":
            new_nodes[node_counter].append(TextNode(text, node.text_type))

    if len(new_nodes) > 1:
        for i in range(1, len(new_nodes)):     
            new_nodes[0].extend(new_nodes[1])
            del new_nodes[1]

    return new_nodes[0]

def split_nodes_image(old_nodes):
    
    new_nodes = [[]]
    node_counter = -1

    for node in old_nodes:
        
        node_counter += 1
        text = node.text
        
        if len(new_nodes) <= node_counter:
            new_nodes.append([])

        if extract_markdown_images(text) == []:
            new_nodes[node_counter].append(TextNode(text, node.text_type, node.url))
            continue
        
        while extract_markdown_images(text) != []:
            
            matches = extract_markdown_images(text)
            image_text = matches[0][0]
            image = matches[0][1]
            delimiter = f"![{image_text}]({image})"
            sections = text.split(delimiter, 1)
            
            if sections[0] != "":
                new_nodes[node_counter].append(TextNode(sections[0], node.text_type))
            new_nodes[node_counter].append(TextNode(image_text, TextType.IMAGE, image))
            
            text = sections[1]
        if text != "":
            new_nodes[node_counter].append(TextNode(text, node.text_type))
    
    if len(new_nodes) > 1:
        for i in range(1, len(new_nodes)):     
            new_nodes[0].extend(new_nodes[1])
            del new_nodes[1]

    return new_nodes[0]

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
   
    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    return nodes
            
print(text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))