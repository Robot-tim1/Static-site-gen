import unittest

from htmlnode import *
from textnode import *
from page_generation import *

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
    
    def test_propseq(self):
        node = HTMLNode(None, None, None,{
        "href": "https://www.google.com",
        "target": "_blank",
            })
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), node2)
    
    def test_propsnoteq(self):
        node = HTMLNode(None, None, None,{
        "href": "https://www.google.com",
        "target": "_blank",
            })
        node2 = 'href="https://www.google.com" target="_blank"'
        self.assertNotEqual(node.props_to_html(), node2)

    def test_propseq2(self):
        node = HTMLNode(None, None, None,{
        "href": "https://www.google.com",
        "target": "_blank", "bitch": "cunt "
            })
        node2 = ' href="https://www.google.com" target="_blank" bitch="cunt "'
        self.assertEqual(node.props_to_html(), node2)
    
    def test_propseq3(self):
        node = HTMLNode(None, None, None,{
        "href": "https://www.google.com",
            })
        node2 = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), node2)

    def test_propseq4(self):
        node = HTMLNode(None, None, None,{
        "href": 132,
            })
        node2 = ' href="132"'
        self.assertEqual(node.props_to_html(), node2)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "Hello, world!")
        self.assertEqual(node.to_html(), "<code>Hello, world!</code>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_to_html_block(self):
        node = LeafNode("blockquote", "Hello, world!")
        self.assertEqual(node.to_html(), "<blockquote>Hello, world!</blockquote>")

    def test_leaf_to_html_pnoteq(self):
        node = LeafNode("b", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_pnoteq2(self):
        node = LeafNode("b", {"5": 'p'})
        self.assertNotEqual(node.to_html(), "<b>5</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children2(self):
        child_node = LeafNode("span", {"child": 'game'})
        parent_node = ParentNode("div", [child_node])
        self.assertNotEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children3(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", None)
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_muti_leaf(self):
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

    def test_empty(self):
        with self.assertRaises(ValueError):
            node = TextNode("", None)
            html_node = text_node_to_html_node(node)
        
    def test_plain(self):
        node = TextNode("This is a plain node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a plain node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "goob.rom")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props, {'href': 'goob.rom'})
        self.assertEqual(html_node.value, "This is a link node")

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "goob.rom")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props, {'src': 'goob.rom', 'alt': 'This is a image node'})
        self.assertEqual(html_node.value, '')
    
    def test_AttributeError(self):
        with self.assertRaises(AttributeError):
            node = TextNode("This is a rat node", TextType.RAT)  

    def test_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode('p', None, 5)
            node.to_html()

    def test_split_node(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("italic block", TextType.ITALIC),
    TextNode(" word", TextType.TEXT),])
        
    def test_split_node_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bold block", TextType.BOLD),
    TextNode(" word", TextType.TEXT),])
        
    def test_split_node_bold2(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is text with a ***bold block**** word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
    def test_split_node_italic2(self):
        node = TextNode("_This is text with_ a italic block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
    TextNode("This is text with", TextType.ITALIC),
    TextNode(" a italic block word", TextType.TEXT),])
    
    def test_split_node_failure(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text **with a **bold block** word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_node_failure2(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is text **with* a **bold block** word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_node_multiple(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        node2 = TextNode("This is _text_ with a italic _block word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("italic block", TextType.ITALIC),
    TextNode(" word", TextType.TEXT), 
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.ITALIC),
    TextNode(" with a italic ", TextType.TEXT),
    TextNode("block word", TextType.ITALIC),])
        
    def test_extract_title(self):
        header = extract_title('# Hello')
        self.assertEqual(header, 'Hello')

    def test_extract_title2(self):
        header = extract_title('#   Title and stuff  ')
        self.assertEqual(header, 'Title and stuff')

    def test_extract_title3(self):
        header = extract_title('paragraph before title who cares\n\n# This is the title')
        self.assertEqual(header, 'This is the title')

    def test_extract_title_exception(self):
        with self.assertRaises(Exception):
            header = extract_title('paragraph who cares')

if __name__ == "__main__":
    unittest.main()