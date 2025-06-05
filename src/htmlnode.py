class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("this method is not implemented")
    
    def props_to_html(self):
        props = ""
        if self.props == None:
            return props
        for key, value in self.props.items():
            props += f" {key}=\"{value}\""
        return props
    
    def print_children(self):
        printable = ""
        i = 1
        if self.children == None:
            return printable
        for child in self.children:
            printable += f"Child {i}:\n{child.print_self()}"
            i += 1
        return printable
    
    def __repr__(self):
        self.print_self()

    def print_self(self):
        printable = ""
        if self.tag != None:
            printable += f"Tag: {self.tag}\n"
        if self.value != None:
            printable += f"Value: {self.value}\n"
        if self.children != None:
            printable += f"Children: [{self.print_children()}]"
        if self.props != None:
            printable += f"Properties: {self.props_to_html()}\n"
        return printable