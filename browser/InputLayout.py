from browser.DrawRect import DrawRect
from browser.DrawText import DrawText
import tkinter
import tkinter.font

INPUT_WIDTH_PX = 200

class InputLayout:

    def __init__(self, node, parent, previous):
        self.size = 16
        self.FONTS = {}
        self.node = node
        self.children = []
        self.parent = parent
        self.previous = previous

    def layout(self):
        weight = self.node.style["font-weight"]
        style = self.node.style["font-style"]
        if style == "normal": style = "roman"
        size = int(float(self.node.style["font-size"][:-2]) * .75)
        self.font = self.get_font(size, weight, style)

        self.width = INPUT_WIDTH_PX

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
        bgcolor = self.node.style.get("background-color",
                                      "transparent")
        if bgcolor != "transparent":
            x2, y2 = self.x + self.width, self.y + self.height
            rect = DrawRect(self.x, self.y, x2, y2, bgcolor)
            display_list.append(rect)

        if self.node.tag == "input":
            text = self.node.attributes.get("value", "")
        elif self.node.tag == "button":
            text = self.node.children[0].text

        color = self.node.style["color"]
        display_list.append(
            DrawText(self.x, self.y, text, self.font, color))

