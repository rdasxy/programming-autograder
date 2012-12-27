#This script looks for a file called solution.py (can be changed in code). 
#It searches for files beginning with 'input'. For each, it calls the 
#command-line interpreter and runs solution.py on it, producing an output file
#similarly named ('in' replaced by 'out', so 'inputfile1.txt' produces 'outputfile1.txt') 
#
#There will also be a file called err.txt, containing any data sent to the error 
# stream (stderr). If the program ran correctly, this file will be empty.
#
# Place this script in the folder with the solution & input files, to generate
# the output files. 

import os 
Home = os.getcwd()
ProgName = 'solution.py'  # CHANGE THIS IF NEEDED. 
FileList = os.listdir(os.getcwd())
for f in FileList: 
    if f.startswith('input'): 
        OutName = f.replace('in', 'out')
        InName = f
        CmdLine = 'python %s <%s >%s 2>%s' % (ProgName, InName, OutName, 'err.txt')
        os.system(CmdLine)
        ErrMsg = open('err.txt').read()
        if len(ErrMsg) > 2:
            print "Error with", f
            break
        #print InName, '>>>', OutName 

 
