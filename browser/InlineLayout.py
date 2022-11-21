import tkinter
import tkinter.font
from browser.Text import Text
from browser.DrawText import DrawText
from browser.DrawRect import DrawRect
from browser.Element import Element
from browser.TextLayout import TextLayout
from browser.LineLayout import LineLayout

WIDTH, HEIGHT = 800, 600
SCROLL_STEP = 100
HSTEP, VSTEP = 13, 18


class InlineLayout:

    def __init__(self, node, parent, previous):
        self.FONTS = {}
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []

    def paint(self, display_list):
        bgcolor = self.node.style.get("background-color",
                                      "transparent")
        if bgcolor != "transparent":
            x2, y2 = self.x + self.width, self.y + self.height
            rect = DrawRect(self.x, self.y, x2, y2, bgcolor)
            display_list.append(rect)

        for child in self.children:
            child.paint(display_list)

    def layout(self):
        self.width = self.parent.width
        self.x = self.parent.x
        if self.previous:
            self.y = self.previous.y + self.previous.height
        else:
            self.y = self.parent.y

        self.new_line()
        self.recurse(self.node)
        for line in self.children:
            line.layout()
            
        self.height = sum([line.height for line in self.children])
        # self.height = self.cursor_y - self.y

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


    def text(self, node):
        color = self.node.style["color"]
        weight = self.node.style["font-weight"]
        style = self.node.style["font-style"]
        if style == "normal":
            style = "roman"
        size = int(float(self.node.style["font-size"][:-2]) * .75)
        font = self.get_font(size, weight, style)
        for word in node.text.split():
            w = font.measure(word)
            if self.cursor_x + w > self.width - HSTEP:
                self.new_line()
                # self.cursor_y += font.metrics("linespace") * 1.25
                cursor_x = HSTEP
            line = self.children[-1]
            text = TextLayout(node, word, line, self.previous_word)
            line.children.append(text)
            self.previous_word = text
            self.cursor_x += w + font.measure(" ")

    def new_line(self):
        self.previous_word = None
        self.cursor_x = self.x
        last_line = self.children[-1] if self.children else None
        new_line = LineLayout(self.node, self, last_line)
        self.children.append(new_line)

    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x, word, font, color in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font, color in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font, color))
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

    def recurse(self, node):
        if isinstance(node, Text):
            self.text(node)
        else:
            if node.tag == "br":
                self.flush()
            for child in node.children:
                self.recurse(child)

    def __repr__(self) -> str:
        return f"InlineLayout(y={self.y}, height={self.height})"

