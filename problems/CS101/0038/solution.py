# solution.py

from divider import Divider

x = int(raw_input())
y = int(raw_input())

d = Divider()
try:
    print "Quotient is %d" % d.divide(x, y)
except ValueError:
    print "Cannot divide by zero"
    