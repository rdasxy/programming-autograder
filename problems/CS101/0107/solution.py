##Alg
##get input
##split on spaces
##convert input1 to int
##convert input2 to float
##compare types
##print bool result

inp1, inp2 = raw_input(">>").split()
inp1 = int(inp1)
inp2 = float(inp2)
if type(inp1) == type(inp2):
    boolean = "True"
else:
    boolean = "False"
print "type(%d) == type(%f) = %s" %(inp1, inp2, boolean)


