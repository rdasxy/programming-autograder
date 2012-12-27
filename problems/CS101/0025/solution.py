atWt = {'H':1.0, 'C':12.0, 'N':14.0, 'O':16.0, 'F':19.0, 
        'S':32.1, 'P': 31.0, 'K':39.1, 'B': 10.8}
formula = raw_input("What's the chemical formula?")

def weight(formula):
    if not formula:
        return 0
    if len(formula) == 1:
        return atWt[formula]
    if formula[1].isdigit():
        return int(formula[1]) * atWt[formula[0]] + weight(formula[2:])
    else:
        return atWt[formula[0]] + weight(formula[1:])
            
print weight(formula)





        
        
        
        



