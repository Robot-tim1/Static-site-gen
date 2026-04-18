from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""     
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leafnodes must have values")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parentnodes must have a tag")
        if not self.children:
            raise ValueError("Must have child")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_parent = ParentNode('div', None, None)
    div_children = []  
    for block in blocks:
        block_type = block_to_block_type(block)
        parent_node = blocktype_to_parent_node(block_type, block)
        
        if block_type == BlockType.CODE:
            text = block.removeprefix('```\n').removesuffix('```')
            text_node = TextNode(text, TextType.TEXT, None)
            parent_node.children.children == text_node_to_html_node(text_node)
            div_children.append(parent_node)
            continue
        
        if block_type == BlockType.ORDERED or block_type == BlockType.UNORDERED:
            pass
        
def blocktype_to_parent_node(block_type, block_text: str):
    if block_type == BlockType.CODE:
        return ParentNode('pre', ParentNode(BlockType.CODE, None, None), None)
    if block_type == BlockType.HEADING:
        num = len(block_text.split()[0])
        return ParentNode(f'{BlockType.HEADING}{num}', None, None)
    return ParentNode(block_type, None, None)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes