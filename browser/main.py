# This is a sample Python script.

import socket
import tkinter
import tkinter.font

from browser.Text import Text
from browser.Element import Element
from browser.InlineLayout import InlineLayout
from browser.HTMLParser import HTMLParser
from browser.DocumentLayout import DocumentLayout
from browser.BlockLayout import BlockLayout

WIDTH, HEIGHT = 800, 600
SCROLL_STEP = 100
HSTEP, VSTEP = 13, 18

class Browser:

    WIDTH, HEIGHT = 800, 600
    SCROLL_STEP = 100
    HSTEP, VSTEP = 13, 18

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.bi_times = tkinter.font.Font(
            family="Times",
            size=16,
            weight="bold",
            slant="italic",
        )
        self.weight = "normal"
        self.style = "roman"


    def scrolldown(self, e):
        max_y = self.document.height - HEIGHT
        self.scroll = min(self.scroll + SCROLL_STEP, max_y)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT: continue
            if cmd.bottom < self.scroll: continue
            cmd.execute(self.scroll, self.canvas)

    def load(self, url):

        headers, body = request(url)
        self.nodes = HTMLParser(body).parse()
        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        self.display_list = []
        self.document.paint(self.display_list)
        self.draw()


def request(url):
    #assert url.startswith("http://")
    #url = url[len("http://"):]

    schema, host_path = url.split("://", 1)
    host, path = host_path.split("/", 1)

    path = "/" + path

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    s.connect((host, 80))
    s.send("GET {} HTTP/1.0\r\n".format(path).encode("utf8") +
           "Host: {}\r\n\r\n".format(host).encode("utf8"))
    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)
    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
    assert "transfer-encoding" not in headers
    assert "content-encoding" not in headers
    body = response.read()
    s.close()
    return headers, body

def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")


def load(url):

    headers, body = request(url)
    show(body)

def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)


if __name__ == "__main__":
    import sys

    url = 'http://example.org/index.html'
    Browser().load(url)

    headers, body = request(url)
    nodes = HTMLParser(body).parse()
    print_tree(nodes)

    WIDTH, HEIGHT = 800, 600
    #window = tkinter.Tk()
    #canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT)
    #canvas.pack()

    tkinter.mainloop()
