# DividerTest.py

from divider import Divider

d = Divider()

for x, y in [(8,4), (4,0)]:
    try:
        print "Quotient is %d" % d.divide(x, y)
    except ValueError:
        print "Cannot divide by zero"
        

