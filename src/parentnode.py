from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children:list, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("the ParentNode has no tag")
        if self.children == [] or self.children == None: 
            raise ValueError("the ParentNode has no children")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html