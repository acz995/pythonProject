import tkinter
import tkinter.font
from browser.Text import Text
from browser.DrawText import DrawText
from browser.DrawRect import DrawRect
from browser.Element import Element

WIDTH, HEIGHT = 800, 600
SCROLL_STEP = 100
HSTEP, VSTEP = 13, 18


class InlineLayout:

    def __init__(self, node, parent, previous):
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []

    def paint(self, display_list):
        if isinstance(self.node, Element) and self.node.tag == "pre":
            x2, y2 = self.x + self.width, self.y + self.height
            rect = DrawRect(self.x, self.y, x2, y2, "gray")
            display_list.append(rect)
        for x, y, word, font in self.display_list:
            display_list.append(DrawText(x, y, word, font))

    def layout(self):

        self.FONTS = {}
        self.display_list = []
        self.x = HSTEP
        self.y = VSTEP
        self.cursor_x = self.x
        self.cursor_y = self.y
        self.weight = "normal"
        self.height = self.cursor_y - self.y
        self.style = "roman"
        self.size = 16
        self.line = []
        self.recurse(self.node)
        self.flush()

    def open_tag(self, tag):
        if tag == "i":
            self.style = "italic"
        elif tag == "b":
            self.weight = "bold"
        elif tag == "small":
            self.size -= 2
        elif tag == "big":
            self.size += 4
        elif tag == "br":
            self.flush()

    def close_tag(self, tag):
        if tag == "/i":
            self.style = "roman"
        elif tag == "/b":
            self.weight = "normal"
        elif tag == "/small":
            self.size += 2
        elif tag == "/big":
            self.size -= 4
        elif tag == "/p":
            self.flush()
            self.cursor_y += VSTEP

    # def token(self, tok):
    #     if isinstance(tok, Text):
    #         self.text(tok)
    #     elif tok.tag == "i":
    #         self.style = "italic"
    #     elif tok.tag == "/i":
    #         self.style = "roman"
    #     elif tok.tag == "b":
    #         self.weight = "bold"
    #     elif tok.tag == "/b":
    #         self.weight = "normal"
    #     elif tok.tag == "small":
    #         self.size -= 2
    #     elif tok.tag == "/small":
    #         self.size += 2
    #     elif tok.tag == "big":
    #         self.size += 4
    #     elif tok.tag == "/big":
    #         self.size -= 4
    #     elif tok.tag == "br":
    #         self.flush()
    #     elif tok.tag == "/p":
    #         self.flush()
    #         self.cursor_y += VSTEP


    def text(self, tok):
        font = self.get_font(self.size, self.weight, self.style)
        for word in tok.text.split():
            w = font.measure(word)
            if self.cursor_x + w > WIDTH - HSTEP:
                self.flush()
                # self.cursor_y += font.metrics("linespace") * 1.25
                cursor_x = HSTEP
            self.line.append((self.cursor_x, word, font))
            self.cursor_x += w + font.measure(" ")


    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        self.cursor_x = self.x
        self.line = []
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent

    def get_font(self, size, weight, slant):
        key = (size, weight, slant)
        if key not in self.FONTS:
            font = tkinter.font.Font(size=self.size, weight=weight, slant=slant)
            self.FONTS[key] = font
        return self.FONTS[key]

    def recurse(self, tree):
        if isinstance(tree, Text):
            self.text(tree)
        else:
            self.open_tag(tree.tag)
            for child in tree.children:
                self.recurse(child)
            self.close_tag(tree.tag)

