
import piddle as pid

class LimitChart(object):
    """
    A class that draws a bar chart with some kind
    of limit (eg, a bandwidth chart vs the quota)
    """
    
    def __init__(self, imgW, imgH, limit, data):
        self.imgW = imgW
        self.imgH = imgH
        self.limit = limit
        self.data = data

    def draw(self, canvas):
        self._autoScale()
        self._drawBackground(canvas)
        self._drawChart(canvas)
        self._drawLimit(canvas)
        self._drawBorder(canvas)

    def _autoScale(self):
        self._bigY = self.limit * 1.25
        for item in self.data:
            if item > self._bigY:
                self._bigY = item
                
    def _drawBackground(self, c):
        c.drawRect(0, 0, self.imgW-1, self.imgH-1,
                   pid.black, fillColor=pid.linen)

    def _drawChart(self, c):
        col = 0
        for item in self.data:
            x1 = col     * (self.imgW/len(self.data))
            x2 = (col+1) * (self.imgW/len(self.data))
            if item is None:
                color = pid.whitesmoke
                fill  = pid.white
                h = self.imgH
            else:
                color = pid.darkgreen
                fill = pid.teal
                h  = (self.imgH * (item*1.0/self._bigY))
            c.drawRect( x1, self.imgH,
                              x2, self.imgH-h,
                              color,
                              fillColor=fill)
            col += 1

    def _drawLimit(self, c):
        level = self.imgH - (self.imgH * (self.limit*1.0/self._bigY))
        c.drawLine(0, level, self.imgW, level, pid.yellowgreen, width=3)

    def _drawBorder(self, c):
        c.drawRect(0, 0, self.imgW-1, self.imgH-1, pid.black)

