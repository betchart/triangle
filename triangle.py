#!/usr/bin/env python

import copy

class TriBoard(object):
    def __init__(self, size):
        self.size = size
        self.points = set()
        return

    def copy(self):
        cpy = TriBoard(self.size)
        cpy.points = copy.deepcopy(self.points)
        return cpy
    
    def remove(self, p):
        self.points.remove(p)
        return

    def add(self, p):
        i, j = p
        assert 0 <= i < self.size
        assert 0 <= j <= i
        if p in self.points:
            raise Exception("Occupied", p)
        self.points.add(p)
        return

    def move(self, p1, p2):
        self.remove(p1)
        self.add(p2)
        return

    def leapfrog(self, p, axis="_", sign=1, remove=True):
        i,j = p
        a,b = p
        if axis is "_":
            j += 2*sign
            b += sign
        elif axis is "/":
            i += 2*sign
            a += sign
        elif axis == "\\":
            b += sign
            a += sign
            j += 2*sign
            i += 2*sign
        else:
            raise Exception('Bad Axis', axis)
        self.move(p, (i,j))
        if remove:
            self.remove((a,b))
        return

    def __str__(self):
        rtn = ""
        for i in range(self.size):
            rtn += (self.size-i) * ' '
            for j in range(i+1):
                rtn += ('X' if (i,j) in self.points else '.')
                rtn += ' '
            rtn += '\n'
        return rtn
    pass
    
class TriSolutions(object):
    def __init__(self, triBoard):
        self.b = triBoard
        self.solutions = []
        self.valid = len(self.b.points) == 1
        if not self.valid:
            self.calc()
        return

    def isValid(self):
        return self.valid
    
    def calc(self):
        for p in self.b.points:
            for axis in "\\_/":
                for sign in [-1,1]:
                    try:
                        bc = self.b.copy()
                        bc.leapfrog(p, axis, sign)
                        sbc = TriSolutions(bc)
                        if sbc.isValid():
                            self.valid = True;
                            self.solutions.append(sbc)
                    except Exception as e:
                        pass
        return
    
                    
def FullTriBoard(size):
    b = TriBoard(size)
    for i in range(size):
        for j in range(i+1):
            b.add((i,j))
    return b


def triangleSolutions(size):
    b = FullTriBoard(size)
    starts = []
    for p in b.points:
        c = b.copy()
        c.remove(p)
        starts.append(TriSolutions(c))
        print "."

    valid = filter(lambda s: s.isValid(), starts)

    print len(valid)

    current = valid[0]
    while len(current.b.points) > 1:
        print current.b
        print current.b.points
        current = current.solutions[0]
    print current.b


    print
    print
    print
    print "======================="
    for v in valid:
        print v.b

    
if __name__ == "__main__":
    triangleSolutions(4)
