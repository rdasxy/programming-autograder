levels = int(raw_input("How many levels?"))
C = dict()
for n in range(levels):
    C[(n,0)] = 1
    C[(n,n)] = 1
    for k in range(1,n):
        C[(n,k)] = C[(n-1, k-1)] + C[(n-1, k)]
for n in range(levels):
    for k in range(n+1):
        print C[(n,k)],
    print       
        