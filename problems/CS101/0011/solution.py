rows = int(raw_input("Enter the number of rows:"))
cols = int(raw_input("Enter the number of columns:"))

for row in range(rows):
    for col in range(cols):
        if col == 0:
            print "%4d" %((row+1)*(col+1)),
        else:
            print "%3d" %((row+1)*(col+1)),
    print
    
