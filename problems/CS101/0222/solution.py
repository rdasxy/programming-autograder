import BadFunction 

thingy = raw_input()
try: 
    print BadFunction.Bad(thingy) 
except TypeError: 
    print 'Sorry, not my type.' 
except ValueError: 
    print 'Bad value.' 
except IOError: 
    print 'EIE, an IO error.'
except KeyError:     
    print 'I am not the keymaster.'
    
    