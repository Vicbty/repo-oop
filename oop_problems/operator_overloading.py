"""OOP Problems - Operator overloading.

Exercises from the course gist "OOP Problems" (B. Dallard, AIDAMS 2A).
Run: python operator_overloading.py
"""
import math


# ---------------------------------------------------------------------------
# Problem 1: complex numbers with + and -
# ---------------------------------------------------------------------------
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"


# ---------------------------------------------------------------------------
# Problem 2: Person compared by age with >
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        return self.age > other.age


# ---------------------------------------------------------------------------
# Problem 4: dot product of two 3D vectors with *
# ---------------------------------------------------------------------------
class Vector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


# ---------------------------------------------------------------------------
# Problem 5: all comparison operators for circles (by radius)
# ---------------------------------------------------------------------------
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __le__(self, other):
        return self.radius <= other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __eq__(self, other):
        return self.radius == other.radius

    def __ne__(self, other):
        return self.radius != other.radius


# ---------------------------------------------------------------------------
# Problem 6: 2D points compared by Euclidean distance to the origin
# ---------------------------------------------------------------------------
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __le__(self, other):
        return self.distance() <= other.distance()

    def __gt__(self, other):
        return self.distance() > other.distance()

    def __ge__(self, other):
        return self.distance() >= other.distance()

    def __eq__(self, other):
        return self.distance() == other.distance()

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# ---------------------------------------------------------------------------
# Problem 7: matrix multiplication with *
# ---------------------------------------------------------------------------
class Matrix:
    def __init__(self, rows):
        self.rows = rows
        self.n = len(rows)
        self.m = len(rows[0])

    def __mul__(self, other):
        if self.m != other.n:
            raise ValueError("Incompatible dimensions")
        result = []
        for i in range(self.n):
            row = []
            for j in range(other.m):
                row.append(sum(self.rows[i][k] * other.rows[k][j] for k in range(self.m)))
            result.append(row)
        return Matrix(result)

    def __eq__(self, other):
        return self.rows == other.rows

    def __repr__(self):
        return "\n".join(" ".join(str(v) for v in r) for r in self.rows)


if __name__ == "__main__":
    # Problem 1
    a, b = Complex(2, 3), Complex(1, -1)
    assert a + b == Complex(3, 2)
    assert a - b == Complex(1, 4)
    print("P1:", a + b, "|", a - b)

    # Problem 2
    p1, p2 = Person("Ana", 30, "F"), Person("Bo", 25, "M")
    assert p1 > p2 and not p2 > p1
    print("P2:", p1 > p2, p2 > p1)

    # Problem 4
    assert Vector(1, 2, 3) * Vector(4, 5, 6) == 32
    print("P4:", Vector(1, 2, 3) * Vector(4, 5, 6))

    # Problem 5
    c1, c2 = Circle(2), Circle(5)
    assert (c1 < c2, c1 <= c2, c1 > c2, c1 >= c2, c1 == c2, c1 != c2) == (True, True, False, False, False, True)
    print("P5:", c1 < c2, c1 <= c2, c1 > c2, c1 >= c2, c1 == c2, c1 != c2)

    # Problem 6
    pa, pb = Point(3, 4), Point(1, 1)
    assert pa > pb and pa == Point(5, 0)
    print("P6:", sorted([pa, pb, Point(0, 2)]))

    # Problem 7
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[5, 6], [7, 8]])
    assert A * B == Matrix([[19, 22], [43, 50]])
    print("P7:\n" + repr(A * B))

    print("All operator overloading tests passed.")
