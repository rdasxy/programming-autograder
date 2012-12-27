from __future__ import division
n = int(raw_input("Enter an integer:"))
largest = n
while True:
    if n == 1:
        break
    if n & 1:
        n = 3*n +1
    else:
        n //= 2
    largest = max(largest, n)
print(largest)

        
