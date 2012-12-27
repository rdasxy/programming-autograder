def index(a, b):
    # maximum number of times that b divides a
    if a  % b != 0:
        return 0
    else:
        return 1 + index(a/b, b)
    
a = int(raw_input("Enter an integer:"))
b = int(raw_input("Enter a second integer:"))

print index(a, b)
