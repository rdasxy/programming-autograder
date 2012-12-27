import PointClass

X, Y = raw_input().split()
X = float(X.strip())
Y = float(Y.strip())
APoint = PointClass.Point(X, Y) 
X, Y = raw_input().split()
X = float(X.strip())
Y = float(Y.strip())
BPoint = PointClass.Point(X, Y) 

D = APoint.Distance(BPoint) 
print "%.3f" % D 
