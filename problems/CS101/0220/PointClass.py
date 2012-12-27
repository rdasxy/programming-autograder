import math 

class Point(object):
        def __init__(self, x= 0, y = 0):
                self.X = x
                self.Y = y
                

        def Quadrant(self):
                if self.X >= 0 and self.Y >= 0: 
                        return 1
                elif self.X < 0 and self.Y >= 0:
                        return 2
                elif self.X < 0 and self.Y < 0: 
                        return 3
                else:
                        return 4

        def Distance(self, OtherPoint): 
                ''' Euclidean distance''' 
                if not isinstance(OtherPoint, Point):
                        raise TypeError 
                else:
                        DeltaX = self.X - OtherPoint.X
                        DeltaY = self.Y - OtherPoint.Y 
                        DeltaX *= DeltaX
                        DeltaY *= DeltaY
                        return math.sqrt(DeltaX + DeltaY)
                
        def OnXAxis(self):
                return self.Y == 0
        
        def OnYAxis(self): 
                return self.X == 0 
        
        def __str__(self):
                return '(%.4f, %.4f)' %(self.X, self.Y)
        
        
        
