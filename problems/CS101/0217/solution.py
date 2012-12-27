import PointClass

X, Y = raw_input().split()
X = float(X.strip())
Y = float(Y.strip())
APoint = PointClass.Point(X, Y) 
print APoint.Quadrant() 
