##Alg:
##get input
##print every odd number in the list

inp = raw_input(">>")
for i in inp.split():
    i = int(i)
    if i%2 == 1:
        print i,
