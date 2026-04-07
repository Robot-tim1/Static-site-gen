from textnode import *

class HTMLnode():
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
        lst = []
        for key, values in self.props.items():
            lst.append(f' {key}="{values}"')
        
        if len(lst) > 1:
            return "".join(lst)
        return lst[0]
        
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"
    
class LeafNode(HTMLnode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leafnodes must have values")
        if not self.tag:
            return f"{self.value}"
        
        match self.tag:
            case "p"|"b"|"i"|"code"|"blockquote"|"h1"|"h2"|"h3"|"h4"|"h5"|"h6"|"div"|"span"|"head"|"body"|"title":
                return f"<{self.tag}>{self.value}</{self.tag}>"
            case "a":
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            case 'img':
                return f'<{self.tag}{self.props_to_html()} />'
            case 'meta':
                return f'<{self.tag}{self.props_to_html()}>'
            case 'html':
                return f'<{self.tag}{self.props_to_html()}></{self.tag}>'
            
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.props}"


class ParentNode(HTMLnode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parentnodes must have a tag")
        if not self.children:
            raise ValueError("Must have child")
        lst = []
        for child in self.children:   
            lst.append(child.to_html())

        if self.tag != 'html':
            return f'<{self.tag}>{"".join(lst)}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{"".join(lst)}</{self.tag}>'

     def __repr__(self):
        return f"{self.tag}, {self.value}, {self.props}"   

def text_node_to_html_node(text_node: TextNode):
    if not text_node:
        raise Exception("Type does not exist")
    
    match text_node.text_type.value:
        case 'text':
            return LeafNode(None, text_node.text)
        case 'plain':
            return LeafNode('p', text_node.text)
        case 'bold':
            return LeafNode('b', text_node.text)
        case 'italic':
            return LeafNode('i', text_node.text)
        case 'code':
            return LeafNode('code', text_node.text)
        case 'link':
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case 'image':
            return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})
        
            