from browser.Text import Text
from browser.InlineLayout import InlineLayout

BLOCK_ELEMENTS = [
        "html", "body", "article", "section", "nav", "aside",
        "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header",
        "footer", "address", "p", "hr", "pre", "blockquote",
        "ol", "ul", "menu", "li", "dl", "dt", "dd", "figure",
        "figcaption", "main", "div", "table", "form", "fieldset",
        "legend", "details", "summary"
    ]
WIDTH, HEIGHT = 800, 600
SCROLL_STEP = 100
HSTEP, VSTEP = 13, 18

class BlockLayout:


    def __init__(self, node, parent, previous):
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []
        self.y = 0
        self.x = 0
        self.width = 0
        self.height = 0

    def paint(self, display_list):
        for child in self.children:
            child.paint(display_list)

    def layout(self):
        previous = None
        for child in self.node.children:
            if BlockLayout.layout_mode(child) == "inline":
                next = InlineLayout(child, self, previous)
            else:
                next = BlockLayout(child, self, previous)
            self.children.append(next)
            previous = next


        self.width = self.parent.width
        self.x = self.parent.x
        if self.previous:
            self.y = self.previous.y + self.previous.height
        else:
            self.y = self.parent.y
        for child in self.children:
            child.layout()
        self.height = sum([child.height for child in self.children])




    def layout_mode(node):
        if isinstance(node, Text):
            return "inline"
        elif node.children:
            for child in node.children:
                if isinstance(child, Text): continue
                if child.tag in BLOCK_ELEMENTS:
                    return "block"
            return "inline"
        else:
            return "block"

    def __repr__(self) -> str:
        return f"BlockLayout(y={self.y}, height={self.height})"


