from __future__ import division
n = int(raw_input("Enter an integer:"))
while True:
    print(n)
    if n == 1:
        break
    if n & 1:
        n = 3*n +1
    else:
        n //= 2
        
