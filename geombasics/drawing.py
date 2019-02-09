from svghelper import *
from geombasics.geometry import Point, Line, Circle, Angle
from contextlib import contextmanager

@contextmanager
def svg(width = 300, height = 300):
    c = Canvas(width, height)
    yield c
    print(c)

class Canvas(SVGEngine):
    def __init__(self, width = 300, height = 300):
        SVGEngine.__init__(self, width, height)
        self.style = 'pencil'

    def draw(self, obj):
        if isinstance(obj, Line):
            self.line(obj.a, obj.b)
        elif isinstance(obj, Point):
            self.point(obj)
        elif isinstance(obj, Circle):
            self.circle(obj)
        elif isinstance(obj, Angle):
            self.angle(obj)

    def drawin(self, style, objects):
        self.style = style
        for obj in objects:
            self.draw(obj)

    def _arcends(self, angle, r = 25):
        a, b, c = angle.a, angle.b, angle.c
        v1 = a - b
        v2 = c - b
        v1 = v1 * (r / v1.length())
        v2 = v2 * (r / v2.length())
        if v1.orient(v2):
            v1, v2 = v2, v1
        start = b + v1
        finish = b + v2
        return start, finish

    def angle(self, angle, r = 25):
        start, finish = self._arcends(angle, r)
        newstyle = self.style + ' nostroke'
        self.draw_wedge(angle.b.tup(), start.tup(), finish.tup(), r, **{'class':newstyle})
        self.draw_arc(start.tup(), finish.tup(), r, **{'class':self.style})

    def line(self, a, b):
        self.draw_line(a.tup(), b.tup(), **{'class':self.style})

    def point(self, a):
        self.draw_circle(a.tup(), 2, **{'class':self.style + " fill"})

    def circle(self, obj):
        a, b = obj.c, obj.r
        c = a-b
        r = (c.x**2 + c.y**2) ** 0.5
        self.draw_circle(a.tup(), r, **{'class':self.style})
