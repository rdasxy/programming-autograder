InpStr = raw_input('Enter two whole numbers: ')
try:
    X, Y = InpStr.split()
    print int(X) + int(Y)
except ValueError:
    print "That's not a number!"
    
