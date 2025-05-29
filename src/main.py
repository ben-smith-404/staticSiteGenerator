from textnode import TextNode, TextType

def main():
    text_node = TextNode("testing", TextType.BOLD, "https://test.com")
    print(text_node)

main()