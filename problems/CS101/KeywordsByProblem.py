# for each keyword, list all problems connected to it. 

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
                    keywords = Words[1].split()
                    for key in keywords: 
                        try:
                            Listing[key.lower().strip()].append(sub.strip())
                        except KeyError:
                            Listing[key.lower().strip()] = [sub.strip()]
        finally:
            os.chdir(Home)
            
for k in sorted(Listing):
    print "%s:   %s" % (k, Listing[k])
    
                    