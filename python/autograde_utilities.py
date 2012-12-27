import random
import os 
import string

def UpdateDatabase(StudentID, ProblemID, Result):
    print "Updating database: Student", StudentID, " Problem", ProblemID, " Result", Result

    
def Cleanup(SomePath):
    ''' remove all files & subdirectories from a given folder
    NOTE!!! This function is potentially dangerous; make sure top level directory is
    a 'safe' one, e.g. NOT c:\\ ! '''

    if SomePath.startswith('c:/users/public/sandbox/'):
        for Root, Dir, Files in os.walk(SomePath, topdown=False):
            for f in Files:
                os.remove(os.path.join(Root, f))
            for d in Dir:
                os.rmdir(os.path.join(Root, d))
    
def TempName():
    ''' generate 20-character random alphanumeric string'''
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    Nam = ''
    for i in range(20):
        Nam += random.sample(chars, 1)[0]
    return Nam 

def CompareIgnoreFormatting(Out1, Out2):
    ''' compare 2 strings, ignoring whitespace ''' 
    for ch in string.whitespace:
        Out1 = Out1.replace(ch, '')
        Out2 = Out2.replace(ch, '')
    if Out1.lower() == Out2.lower():
        return "success"
    else:
        return "Wrong Answer"

def CompareWithFormatting(Out1, Out2):
    ''' compare 2 strings, counting whitespace. if different, calls
    CompareWithFormatting to see if it's substantively wrong or only a whitespace issue'''
    if Out1 == Out2:
        return "success"
    elif "success" == CompareIgnoreFormatting(Out1, Out2):
        return "Format Error"
    else:
        return "Wrong Answer" 

