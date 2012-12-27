set1 = set(raw_input("Enter a string:"))
set2 = set(raw_input("Enter a second string:"))

set3 = set([(a,b) for a in set1 for b in set2])
for n in set3:
    print str(n)+' ',
print

