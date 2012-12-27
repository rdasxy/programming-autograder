import PointClass

X, Y = raw_input().split()
X = float(X.strip())
Y = float(Y.strip())
APoint = PointClass.Point(X, Y) 
X, Y = raw_input().split()
X = float(X.strip())
Y = float(Y.strip())
BPoint = PointClass.Point(X, Y) 

if APoint.Quadrant() == BPoint.Quadrant(): 
    print 'Yes'
else:
    print 'No'
    
    