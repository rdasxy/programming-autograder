# for each problem, list its keywords. 

import os 
Listing = dict()
Home = os.getcwd() 
Subdirs = os.listdir(Home) 
for sub in Subdirs: 
    if os.path.isdir(sub):
        os.chdir(sub)
        try: 
            lines = open('template.txt', 'r').readlines()
        except IOError: 
            print "No template file for", sub
            continue 
        else:
            for line in lines: 
                Words = line.split(':')
                if Words[0].startswith('Keyword'):
                    Listing[sub] = Words[1].strip()
        finally:
            os.chdir(Home)
            
for k in sorted(Listing):
    print "%s:   %s" % (k, Listing[k])
    
                    