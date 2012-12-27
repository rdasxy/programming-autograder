import PointClass

X, Y = raw_input().split()
X = float(X.strip())
Y = float(Y.strip())
APoint = PointClass.Point(X, Y) 
X, Y = raw_input().split()
X = float(X.strip())
Y = float(Y.strip())
BPoint = PointClass.Point(X, Y) 

if APoint.Distance( PointClass.Point(0,0)) < BPoint.Distance(PointClass.Point(0,0)):
    print APoint
else:
    print BPoint 
    
    