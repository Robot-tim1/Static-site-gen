import unittest

from textnode import *


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
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is bold text with an ", TextType.BOLD),
                TextNode("this is a link", TextType.LINK, "linktolink.com"),
                TextNode(" and another ", TextType.BOLD),
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
        
if __name__ == "__main__":
    unittest.main()