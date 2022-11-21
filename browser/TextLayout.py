import tkinter
import tkinter.font
from browser.DrawText import DrawText

class TextLayout:
    def __init__(self, node, word, parent, previous):
        self.size = 16
        self.FONTS = {}
        self.node = node
        self.word = word
        self.children = []
        self.parent = parent
        self.previous = previous

    def layout(self):
        weight = self.node.style["font-weight"]
        style = self.node.style["font-style"]
        if style == "normal": style = "roman"
        size = int(float(self.node.style["font-size"][:-2]) * .75)
        self.font = self.get_font(size, weight, style)

        self.width = self.font.measure(self.word)

        if self.previous:
            space = self.previous.font.measure(" ")
            self.x = self.previous.x + space + self.previous.width
        else:
            self.x = self.parent.x

        self.height = self.font.metrics("linespace")

    def get_font(self, size, weight, slant):
        key = (size, weight, slant)
        if key not in self.FONTS:
            font = tkinter.font.Font(size=self.size, weight=weight, slant=slant)
            self.FONTS[key] = font
        return self.FONTS[key]

    def paint(self, display_list):
        color = self.node.style["color"]
        display_list.append(
            DrawText(self.x, self.y, self.word, self.font, color))
