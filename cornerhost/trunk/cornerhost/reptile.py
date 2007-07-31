
## reptile #################################################

from __future__ import generators
import os
import zebra

class Tile:
    def render(self, model):
        raise NotImplementedError

class SimpleTile(Tile):
    def render(self, model):
        return model.out

class ZebraTile(Tile):
    path = "."
    def __init__(self, file):
        self.file = file
    def render(self, model):
        return zebra.fetch(
            os.path.join(ZebraTile.path,self.file),
            model).encode("utf-8")
        
class CompositeTile(Tile):
    def __init__(self, h=[],b=[],f=[]):
        self.h, self.b, self.f = h,b,f

    def head(self): return self.h
    def body(self): return self.b
    def foot(self): return self.f

    def children(self):
        for t in self.head(): yield t
        for t in self.body(): yield t
        for t in self.foot(): yield t

    def render(self, model):
        return "".join([child.render(model) for child in self.children()])
