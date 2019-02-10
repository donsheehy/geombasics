class NoneConstraint:
	def project(self, p):
		pass

class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __sub__(self, other):
		return self + (-other)

	def __mul__(self, other):
		try:
			return (self.x * other.x + self.y * other.y)
		except(AttributeError):
			return Vector(other * self.x, other * self.y)

	def length(self):
		return (self * self)**0.5

	def vect(self):
		return self

	def tup(self):
		return (self.x, self.y)

	def __rmul__(self, other):
		return self * other

	def __div__(self, other):
		if other == 0:
			return Vector(0, 0)
		return self * (1 / other)

	def orthogonal(self):
		return Vector(self.y, -self.x)

	def orient(self, other):
		return self * other.orthogonal() > 0

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class Point:
	def __init__(self, c1 = NoneConstraint(), c2 = NoneConstraint(), x = 0, y = 0):
		self.c1 = c1
		self.c2 = c2
		self.setxy(x,y)
		for i in range(50):
			self.c1.project(self)
			self.c2.project(self)
		if isinstance(self.c1, Circle) and isinstance(self.c2, Circle):
			if (self - self.c1.c).orient(self.c2.c - self.c1.c):
				newp = Point()
				newp.setxy(self.x(), self.y())
				L = Line(self.c1.c, self.c2.c)
				L.project(newp)
				self.pos = self.vect() + 2 * (newp - self)
		if isinstance(self.c1, Circle) and isinstance(self.c2, Line):
			self.circle_intersect_line(self.c1, self.c2, -1)
		if isinstance(self.c1, Line) and isinstance(self.c2, Circle):
			self.circle_intersect_line(self.c2, self.c1, 1)

	def circle_intersect_line(self, circle, line, orientation):
		newp = Point(line, line, circle.c.x(), circle.c.y())
		other = self + 2 * (newp - self)
		if (line.a - line.b) * orientation * (self - other) > 0:
			self.pos = other.pos

	def x(self):
		return self.pos.x

	def y(self):
		return self.pos.y

	def tup(self):
		return self.x(), self.y()

	def vect(self):
		return self.pos

	def setxy(self, x, y):
		self.pos = Vector(x, y)

	def __sub__(self, other):
		return self.pos - other.pos

	def __add__(self, other):
		newpos = self.pos + other.vect()
		p = Point()
		p.pos = newpos
		return p

class Line:
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def project(self, p):
		v = (self.b - self.a).orthogonal()
		normal = v * (1 / v.length())
		q = normal * (p - self.a)
		pp = p.vect() - (normal * q)

		p.setxy(pp.x, pp.y)

class Circle:
	def __init__(self, c, r):
		self.c = c
		self.r = r
		self.radius = (c-r).length()

	def project(self, p):
		v = (p - self.c)
		pp = self.c.vect() + v * (self.radius / v.length())
		p.setxy(pp.x, pp.y)

class Angle:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c
