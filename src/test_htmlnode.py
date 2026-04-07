import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_propseq(self):
        node = HTMLnode(None, None, None,{
        "href": "https://www.google.com",
        "target": "_blank",
            })
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), node2)
    
    def test_propsnoteq(self):
        node = HTMLnode(None, None, None,{
        "href": "https://www.google.com",
        "target": "_blank",
            })
        node2 = 'href="https://www.google.com" target="_blank"'
        self.assertNotEqual(node.props_to_html(), node2)

    def test_propseq2(self):
        node = HTMLnode(None, None, None,{
        "href": "https://www.google.com",
        "target": "_blank", "bitch": "cunt "
            })
        node2 = ' href="https://www.google.com" target="_blank" bitch="cunt "'
        self.assertEqual(node.props_to_html(), node2)
    
    def test_propseq3(self):
        node = HTMLnode(None, None, None,{
        "href": "https://www.google.com",
            })
        node2 = ' href="https://www.google.com"'
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

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Click me!", {"src": "url/of/image.jpg", "alt": "Description of image"})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpg" alt="Description of image" />')

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

    def test_to_html_muti_leaf(self):
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
    
    def test_to_html_finalboss(self):
        head_child = LeafNode('meta', "", {"charset": "UTF-8"})
        head_child2 = LeafNode('title', 'My First Web Page')
        head = ParentNode('head', [head_child, head_child2])
        body_child = LeafNode('h1', 'Welcome to My Website')
        body_child2 = LeafNode('p', 'This is a simple paragraph of text.')
        body_child3 = LeafNode('a', 'Visit W3Schools', {"href": "https://www.w3schools.com"})
        body = ParentNode('body', [body_child, body_child2, body_child3])
        html = ParentNode('html', [head, body], {'lang': 'en'})

        self.assertEqual(html.to_html(), '<html lang="en"><head><meta charset="UTF-8"><title>My First Web Page</title></head><body><h1>Welcome to My Website</h1><p>This is a simple paragraph of text.</p><a href="https://www.w3schools.com">Visit W3Schools</a></body></html>')

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_plain(self):
        node = TextNode("This is a plain node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'p')
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

if __name__ == "__main__":
    unittest.main()