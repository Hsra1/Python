from math import sqrt


class vector:

    def __init__(self, vec):
        self.vec = vec

    def __add__(self, other):
        result = []
        for i in range(len(self.vec)):
            result.append(self.vec[i] + other.vec[i])
        return vector(result)

    def __sub__(self, other):
        result = []
        for i in range(len(self.vec)):
            result.append(self.vec[i] - other.vec[i])
        return vector(result)

    def __mul__(self, other):
        result = []
        for i in self.vec:
            result.append(i * other)
        return vector(result)

    def __truediv__(self, other):
        result = []
        for i in self.vec:
            result.append(i / other)
        return vector(result)

    def __getitem__(self, key):
        return self.vec[key]

    def __setitem__(self, key, value):
        self.vec[key] = value

    def mod(self):
        mod = 0
        for i in self.vec:
            mod += i * i
        return sqrt(mod)

    def dir(self):
        return self / self.mod()

    def dot(self, other):
        dot = 0
        for i in range(len(self.vec)):
            dot += self[i] * other[i]
        return dot

    def projection(self, other):
        return other * (self.dot(other) / other.mod() ** 2)
