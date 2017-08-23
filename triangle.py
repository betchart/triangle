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
    
    def open(self, p):
        i,j = p
        return (0 <= i < self.size and
                0 <= j <= i and
                p not in self.points)

    def remove(self, p):
        self.points.remove(p)
        return

    def add(self, p):
        if not self.open(p):
            raise Exception("Occupied", p)
        self.points.add(p)
        return

    def move(self, p1, p2):
        self.remove(p1)
        self.add(p2)
        return

    def neighbors(self,p):
        i,j = p
        return filter(lambda ij: ij in self.points,
                      [(i+irel,j+jrel) for irel,jrel in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)]])

    def leapfrog(self, leaper, frog, removeFrog=True):
        pad = tuple(2 * f - l for l,f in zip(leaper,frog))
        if not self.open(pad):
            return None
        self.move(leaper, pad)
        if removeFrog:
            self.remove(frog)
        return pad

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
    
    def calc(self):
        for p in self.b.points:
            for neighbor in self.b.neighbors(p):
                bc = self.b.copy()
                res = bc.leapfrog(p, neighbor)
                if res == None:
                    continue
                sbc = TriSolutions(bc)
                if sbc.valid:
                    self.valid = True;
                    self.solutions.append(sbc)
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

    valid = filter(lambda s: s.valid, starts)

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
