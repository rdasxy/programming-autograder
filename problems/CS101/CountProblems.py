import os 

Tallies = dict() 
Home = os.getcwd()
Subdirs = os.listdir(Home)
for Subdir in Subdirs: 
    if os.path.isdir(Subdir):
        os.chdir(Subdir)
        try: 
            Template = open('template.txt', 'rU').readlines()
        except IOError: 
            print "No template file found in", Subdir
        else:  # template file opened OK. 
            for line in Template: 
                if line.startswith('Keywor'):
                    Tup = line.strip().split(':')
                    Keys = Tup[1].split()
                    while Keys: 
                        K = Keys[0].lower().strip()
                        try:
                            Tallies[K] += 1
                        except KeyError:
                            Tallies[K] = 1
                        Keys.pop(0)
        finally:
            os.chdir(Home)
for (k,v) in sorted(Tallies.items()):
    print '%s\t\t%d' % (k, v)
    
                    
                    
                    
