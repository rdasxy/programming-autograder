FName = raw_input('Enter filename: ') 
try: 
    Text = open(FName, 'r').read()
    print Text
except IOError: 
    print "The file could not be opened." 
    