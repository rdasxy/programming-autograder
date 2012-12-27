


# 3rd major iteration - refactoring to break out setup, test, teardown functionality
# Use of .ini files to contain problem metadata

import os, sys
import subprocess
import random
import string
import winprocess
import win32pipe
import win32file
import pickle
import autograde_utilities


def ReadSystemConfig():
    try:
        F = open('c:/autograder.ini')
        Stuff = dict() 
        for line in F:
            Setting = line.split('=')
            if Setting[0]:
                Key = Setting[0].strip()
                Val=Setting[1].strip()
                Stuff[Key] = Val
        F.close()
    except IOError, KeyError:
        return None
    return Stuff

def ReadProblemINI(ProblemPath):
    try:
        F=open(os.path.join(ProblemPath, 'template.txt'))
    except IOError:
        return False
    ProblemDict=dict()
    for line in F:
        if len(line) > 2:
            thingy = line.split(':')
            if thingy[0]:
                Key = thingy[0].strip()
                Val=thingy[1].strip()
                ProblemDict[Key]=Val
    F.close()
    # Note: Some things might be lists. Convert them.
    try:
        SubmitList=[F.lower().strip() for F in ProblemDict['SubmissionFiles'].split()]
        ProblemDict['SubmissionFiles']=SubmitList
    except KeyError:
        pass
    try:
        ExtraList=[F.lower().strip() for F in ProblemDict['ExtraFiles'].split()]
        ExtraPath=os.path.join(ProblemPath, 'ExtraFiles')
        Extras = [os.path.join(ExtraPath, F) for F in ExtraList]
        ProblemDict['ExtraFiles']=Extras
    except KeyError:
        pass
    try:
        SubmitList=[F.lower().strip() for F in ProblemDict['IOPairs'].split()]
        TupList = list()
        while SubmitList:
            try:
                (i, o) = SubmitList[0], SubmitList[1]
                SubmitList.pop(0)
                SubmitList.pop(0)
            except IndexError:
                pass
            else:
                TupList.append((i, o))
        ProblemDict['IOPairs']=TupList
    except KeyError:
        pass
    try:
        IOPath=ProblemDict['IOPath']
    except KeyError:
        IOPath=''
    ProblemDict['IOPath'] = os.path.join(ProblemPath, IOPath)
    return ProblemDict
    
    
        

def SetUpSubmission(ProblemID, CodeFileNameList):
    Settings = ReadSystemConfig()
    if not Settings:
         return False, "Can't read system configuration"
    ProblemPath=os.path.join(Settings['ProblemPath'], ProblemID)
    if not os.path.isdir(ProblemPath):
        return False, "Can't find problem directory"
    else:
        Settings['ProblemPath'] = ProblemPath
    ProblemDict=ReadProblemINI(ProblemPath)
    if not ProblemDict:
        return False, "Can't read problem configuration"
    TempDir=autograde_utilities.TempName()
    ProblemDict['SandboxDir'] = os.path.join(Settings['SandboxDir'], TempDir)
    try:
        os.mkdir(ProblemDict['SandboxDir'])
    except WindowsError:
        ProblemDict['SandboxDir'] = None
        return False, "Can't configure problem." 
    
    return Settings, ProblemDict
    
    
             
     
def HandleSubmission(StudentID, ProblemID, CodeFileNameList):
    ''' handle the traffic-cop aspects of a submission.
    Parameters:
        StudentID: The student's UUID
        ProblemID: The identifier for which problem the student is submitting code for. 
        CodeFileNameList: The list of files uploaded by the student.
    Actions:
        For this problem, retrieve the list of system supplied files (if any) and list of (input,output) tuples.
        Feed the HandleFile function the problem, submission, and single (i, o) pairs until either:
            All input cases have been handled successfully; or
            Any submission has returned anything other than 'Success.'
    Returns: tuple, consisting of 1 bool & 2 strings. 
        If all submissions successful, return (True, 'Success', '')
        If any submission failed, return (False, ErrorTypeStr, ErrorMsg)
        '''
##    TempDir, StatusMsg, ErrMsg = SetUpSubmission(ProblemID, CodeFileNameList)
##    if ErrMsg:
##        return (False, StatusMsg, ErrMsg)

    Settings, ProblemDict = SetUpSubmission(ProblemID, CodeFileNameList)
    if not Settings:  # returned False & an error msg
        return (False, 'SystemError', ProblemDict)
    # Otherwise paths are set up & sandbox is ready.
    try:
        IOFiles = ProblemDict['IOPairs']
        FileToRun=os.path.join(ProblemDict['SandboxDir'], ProblemDict['Run'])
        if 'ExtraFiles' in ProblemDict:
            Extras = ProblemDict['ExtraFiles']
        else:
            Extras = []
    except KeyError:
        os.rmdir(ProblemDict['SandboxDir'])
        return (False, 'SystemError', 'Misread configuration data.')

    
    InputDir = ProblemDict['IOPath']
    # Now process each set of I/O files; continue until all done, or an error is hit. 
    for IOTuple in IOFiles:
        In, Out = IOTuple
        In = os.path.join(InputDir, In)
        Out = os.path.join(InputDir, Out)
        Res, Err = HandleFile(CodeFileNameList, In, Out, FileToRun, Extras)
        if Res != 'Correct':
            autograde_utilities.UpdateDatabase(StudentID, ProblemID, Res)
            os.rmdir(ProblemDict['SandboxDir'])
            return (False, Res, Err)

    # If we're here, then all files were processed correctly.

    autograde_utilities.UpdateDatabase(StudentID, ProblemID, Res) 
    
    os.rmdir(ProblemDict['SandboxDir'])
    return (True, 'Success', '')

def HandleFile(CodeFileNameList, InputFileName, CorrectOutputFileName, FileNameToRun, SystemSuppliedFileList=None):
    '''
    Process one student's submission on one set of input data.
    Parameters:
        CodeFileNameList: The non-empty list of files submitted by the student.
        InputFileName: The name (including path if needed) of the ONE file with sample input for this test.
        CorrectOutputFileName: The name (including path if needed) of the ONE file with correct output for
            the specified input.
        FileNameToRun: The name (excluding path) of the ONE file that is to run to test the student's code.
            This must be present in CodeFileNameList or SystemSuppliedFileList.
        SystemSuppliedFileList: The (possibly empty or missing) list of other files (including paths) which
            are needed to run this problem's code (class files, driver programs, etc)
    Returns:
        tuple of strings (Res, Err). Res is a brief description ('Correct', 'Runtime exceeded', etc), and
            Err is an error message (possibly empty string).
    ''' 
    # set up some labels for later (exit codes)
    ExitMsg = {1:'Translation Error', 2:'Time Limit Exceeded', 3:'Windows Error', \
               4:'Excessive Output', 5:'Submission Error'}

    # Make sure we've got everything we're expecting; if we don't, skip all this. 
    ExpectedFiles = CodeFileNameList[:]
    try:
        ExpectedFiles += SystemSuppliedFileList
    except TypeError:  # if there was no list of other needed files. 
        pass
    Expected = [os.path.basename(name).lower() for name in ExpectedFiles]
    if os.path.basename(FileNameToRun).lower().strip() not in Expected:
        Res = "File " + FileNameToRun + " was expected, but not found."
        Err = ExitMsg[5]
        return Res, Err
    # even if we're going ahead, we can free up some memory
    del(ExpectedFiles)
    del(Expected)
    
    # Goose the random number generator just a bit, to be sure every process
    # generates different temporary names.
    #random.jumpahead(os.getpid())
        
    # Create working (temporary) directory, copy files into it
    StartPath = os.getcwd()
    #TmpDir = autograde_utilities.TempName()
    #os.mkdir(TmpDir)

    ReadPath = StartPath
    WritePath = os.path.dirname(FileNameToRun)

    try: 
        for f in CodeFileNameList:
            Code = open(f).read()
            open(WritePath+'/'+os.path.basename(f),'w').write(Code)
  
        if SystemSuppliedFileList:
            for f in SystemSuppliedFileList:
                Code = open(f).read()
                open(WritePath+'/'+os.path.basename(f),'w').write(Code)
                
    except IOError:
        #print "System Error. Can't copy necessary file. Contact administrator"
        # try to clean up 
        autograde_utilities.Cleanup(WritePath)
        os.chdir(StartPath)
        #os.rmdir(WritePath)
        return ('SystemError', 'Contact Administrator or Instructor')
        
    # Setup I/O for program we're testing. 
    Input = open(InputFileName).read()
    os.chdir(WritePath)
    open('input.txt','w').write(Input)

##    TODO: Pipes are more efficient, as they spare the disk operations. Therefore pipes to
##    connect to stdout and stderr of the child process would be more efficient. Given that we're
##    waiting 5 seconds for the process to run, this isn't a huge deal, but may become a factor if
##    we need to scale this up to higher capacity.
    
    In = open('input.txt')
    Out = open('output.txt', 'w')
    Err = open('error.txt', 'w')

    # Run that sucker!
    try:
        ExitCode = winprocess.run('notepad.exe',login='KC-SCE-AUTOGRDR\nAutogradeScript\nCoffeeCup99', desktop='')
        #ExitCode = winprocess.run('python %s' % FileNameToRun, stdin=In, stdout=Out, stderr=Err, mSec=5000,login='KC-SCE-AUTOGRDR\nAutogradeScript\nCoffeeCup99', desktop='')
    except WindowsError, msg:
        if 'timeout exceeded' in str(msg):
            ExitCode = 2 # time out
        else:
            ExitCode = 3  # some other Windows error
    # Exit code of 0 indicates no error, as usual. 

    #Done with files. 
    In.close()
    Out.close()
    Err.close()

    #  Grab output 
    if os.path.getsize('output.txt') < 1.0e7:
        Out = open('output.txt').read()
    else:    # more than 10 megabytes output, something's wrong
        ExitCode = 4  # so set error flag
        Out = ''      # & set Out to a safe value, but don't touch file.  

    # grab error message if any. 
    Err = open('error.txt').read()
    
    # Cleanup temporary directory
    autograde_utilities.Cleanup(WritePath)
    os.chdir(StartPath)
#    os.rmdir(WritePath)

    # Check output for validity.
    Correct = str(open(CorrectOutputFileName).read())
    Out = Out.replace('\r', '')
    Correct = Correct.replace('\r', '')

    try:
        Result = ExitMsg[ExitCode] 
    except KeyError:
        Result = autograde_utilities.CompareWithFormatting(Correct, Out)

    return Result, Err        

if __name__ == '__main__':
    OK, Res, Err = HandleSubmission(1, '0102', ['example0102.py'])
    print "Your result:", Res
    if Err:
        print "Error message:\n", Err
        
    if OK:
        print '\tNeed to update database if this is first success on this problem.'
    else:
        print '\tNeed to update database if this is first attempt on this problem.'
        
