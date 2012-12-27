set1 = set(raw_input("Enter a string:"))
set2 = set(raw_input("Enter a second string:"))
           
set3 = set1.symmetric_difference(set2)
for n in set3:
    print n+' ',
print

