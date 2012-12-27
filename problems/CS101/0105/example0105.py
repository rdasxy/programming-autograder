##Alg:
##print string index specified by user

string = raw_input(">>")
l = [i for i in string.split()]
reversed_l = l[::-1]
s = ""
for i in reversed_l:
    s += i
    s += " "
print s
