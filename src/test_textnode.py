import unittest

from textnode import *
from htmlnode import *

class TestTextNode2(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteqtype(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_notequrl(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_equrl(self):
        node = TextNode("This is a text node", TextType.ITALIC, "boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "boot.dev")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a bitch text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with an !?[image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_link2(self):
        matches = extract_markdown_links("This is text with a link [to awsomesauce(https://www.awsomesauce)")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images2(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [this is a link](linktolink.com) and another [second link](secondlink.net)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("this is a link", TextType.LINK, "linktolink.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "secondlink.net"
                ),
            ],
            new_nodes,
        )
    
    def test_split_link2(self):
        node = TextNode(
            "This is text with an [this is a link](linktolink.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a [this is a second link](linktolinkgoob.coom)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("this is a link", TextType.LINK, "linktolink.com"),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("this is a second link", TextType.LINK, "linktolinkgoob.coom"),
            ],
            new_nodes,
        )

    def test_split_link3(self):
        node = TextNode(
            "This is bold text with an [this is a link](linktolink.com) and another [second link](secondlink.net)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is bold text with an ", TextType.TEXT),
                TextNode("this is a link", TextType.LINK, "linktolink.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "secondlink.net"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual([
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], 
            result,
            )
        
    def test_text_to_textnode2(self):
        result = text_to_textnodes("This is text with an **bold** word and a code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual([
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a code block and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], 
            result,
            )
        
    def test_text_to_textnode3(self):
        result = text_to_textnodes("This is text with an italic word and a code block and an !obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link](https://boot.dev)")
        self.assertListEqual([
                TextNode("This is text with an italic word and a code block and an !obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link](https://boot.dev)", TextType.TEXT),
            ], 
            result,
            )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph"
            ],
        )

    def test_markdown_to_blocks3(self):
        md = """
#### HEADING4

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

1. This is a list
2. with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "#### HEADING4",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "1. This is a list\n2. with items",
            ],
        )

    def test_markdown_block_heading(self):
        block = '#### heading'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.HEADING)

    def test_markdown_blocks_heading2(self):
        block = '####heading'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_markdown_blocks_code(self):
        block = '```\ncode block\nplus a bit more```'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.CODE)

    def test_markdown_blocks_quote(self):
        block = '> quote block'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.QUOTE)
    
    def test_markdown_blocks_quote2(self):
        block = '>quote block'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.QUOTE)

    def test_markdown_blocks_heading3(self):
        block = '####### heading'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_markdown_blocks_heading4(self):
        block = '# heading'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.HEADING)

    def test_markdown_blocks_unorderedlist(self):
        block = '- thing\n- thing2'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.UNORDERED)

    def test_markdown_blocks_orderedlist(self):
        block = '1. thing\n2. thing2'
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.ORDERED)


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
##### this is a _heading_
five
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h5>this is a <i>heading</i> five</h5></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote</blockquote></div>",
        )

    def test_blockquote2(self):
        md = """
>This is a blockquote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote</blockquote></div>",
        )

    def test_blockquote3(self):
        md = """
>This is a blockquote
>
> and stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote and stuff</blockquote></div>",
        )

    def test_unorderedlist(self):
        md = """
- item 1
- item 2
- item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>",
        )

    def test_orderedlist(self):
        md = """
1. item 1
2. item 2
3. item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item 1</li><li>item 2</li><li>item 3</li></ol></div>",
        )

    def test_alltogether(self):
        md = """
# this is a heading

this is a paragraph
that says stuff

> this is a blockquote

- list 1

1. list 2

```
this is a
code block
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is a heading</h1><p>this is a paragraph that says stuff</p><blockquote>this is a blockquote</blockquote><ul><li>list 1</li></ul><ol><li>list 2</li></ol><pre><code>this is a\ncode block\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()