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
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

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

def markdown_to_blocks(markdown):
    markdown = markdown.split("\n\n")
    markdown = list(filter(lambda mark: False if mark == '' else True ,map(lambda mark: mark.strip("\n"), markdown)))
    return markdown