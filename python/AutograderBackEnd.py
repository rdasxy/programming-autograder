
# 4th major iteration - refactoring to deal with changed authentication procedures 
# and to deal with each problem in parallel. 

import os, sys
import subprocess
import random
import string
import winprocess
import win32pipe
import win32file
import pickle
import autograde_utilities
import thread 
import Queue
import time 
import datetime
import smtplib
import collections
import zipfile
import autograder

def ArchiveResults(JobTriple): 
    ''' Record this attempt in archive. 
    Gets 3-tuple: Job (itself a named tuple), result (string), error (string, possibly empty) 
    '''
    D = dict()
    D['UserID'] = JobTriple[0].UserID
    D['CourseNum'] = JobTriple[0].CourseNum
    D['ProblemNum'] = JobTriple[0].ProblemNum
    D['ProblemID']= JobTriple[0].ProblemID
    D['Timestamp'] = JobTriple[0].Timestamp
    D['Files']= JobTriple[0].Files
    D['Result'] = JobTriple[1]
    Path = 'c:/users/public/archive' 
    Fname = JobTriple[0].UserID + JobTriple[0].CourseNum + "%04d"%JobTriple[0].ProblemID + str(JobTriple[0].Timestamp).replace(' ', '').replace(':','')
    Fname = Fname +'.pkl'
    Fullname = os.path.join(Path, Fname)
    Zipname = os.path.join(Path, 'archive.zip')
    F = open(Fullname, 'wb')
    pickle.dump(D, F)
    F.close() 
    Z = zipfile.ZipFile(Zipname, 'a', zipfile.ZIP_DEFLATED)
    Z.write(Fullname, os.path.basename(Fullname))
    Z.close()
    os.remove(Fullname)
    

def EmailResults(AJob, Result, Error):
    # includes code from: http://www.mkyong.com/python/how-do-send-email-in-python-via-smtplib/
    # setup login information
    print "Emailing results."
    prefix = AJob.UserID
    if prefix in ('hareb', 'spatzs'):
        suffix = '@umkc.edu'
    else:
        suffix = '@mail.umkc.edu'
    Addy = prefix + suffix
    gmail_acct = 'umkcautograder@gmail.com'
    gmail_pwd = 'SaulAndBrian'
    # build message 
    Body = "\nThis is an automatically generated email from the autograder. Do not reply to this address. "
    Body += "Contact the course instructor if you have questions."
    Body += "\nHere are the results from your submission for problem %s, %s:\n" % (AJob.ProblemNum, AJob.CourseNum)
    Body += Result + '\n' + Error + '\n'
    header = 'To:' + Addy + '\n' + 'From: ' + gmail_acct + '\n' + 'Subject:Autograder results \n'
    msg = header + Body
    # Now deal with the smtp server 
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_acct, gmail_pwd)
    #print header
    smtpserver.sendmail(gmail_acct, Addy, msg)
    #print 'done!'
    smtpserver.close()
    
def PostResults(ResultQueue):
    ''' pull results from queue, deal w/ logging etc.
    This function is called as a separate thread. It blocks waiting for things to
    be added to the queue; if nothing is added, it blocks until the main process
    dies after a 30-sec or so timeout, taking this thread with it.
    Queue contains 3-tuples: Job (namedtuple), Result (str), ErrMsg (str, may be empty)'''
    # collections.namedtuple(JobType, ['UserID', 'CourseNum', 'ProblemNum', 'ProblemID', 'Timestamp', 'Files']) 

    while not ResultQueue.empty():
        print "Posting results, line 90"
        # TODO: Add code to save student's submission in archive. 
        NextJob = ResultQueue.get()  # this blocks as long as necessary.
        ArchiveResults(NextJob)
       # NextJob[0].Files = None 
        autograder.ReportGradeStatus(NextJob[0], NextJob[1])
        EmailResults(NextJob[0], NextJob[1], NextJob[2])
                          



def Grade(JobList):
    ''' called by chron job--gets a named tuple representing the list of pending jobs. 
    Spins off new threads for dealing with each job. Snoozes a bit, then dies.''' 

    ResultsQueue = Queue.Queue()
    SandboxList = list()
    while JobList: 
        Settings = dict()
        ProblemDict = dict()
        Job = JobList.pop(0)
        if not Job.Files:  # Student didn't turn anything in
            ResultsQueue.put( (Job, 'SubmissionError', 'No files submitted'))
        Settings, ProblemDict = SetUpSubmission(Job)
        SandboxList.append(ProblemDict['SandboxDir'])
        if not Settings:  # Can't set up the problem
            ResultsQueue.put( (Job, 'SystemError', "Can't set up problem; see administrator"))
            return # and we're out of here.   
    
        # Otherwise paths are set up & sandbox is ready.
        try:
            #IOFiles = ProblemDict['IOPairs']
            ProblemDict['FileToRun']=os.path.join(ProblemDict['SandboxDir'], ProblemDict['Run'])
            if 'ExtraFiles' in ProblemDict:
                Extras = ProblemDict['ExtraFiles']
            else:
                Extras = []
        except KeyError:
            os.rmdir(ProblemDict['SandboxDir'])
            ResultsQueue.put( (Job, 'SystemError', 'Misread configuration data; see administrator'))
            return        
        #NextJob = JobList.pop(0)
##        ReportGradeStatus(NextJob.UserID, NextJob.CourseNum, NextJob.ProblemNum, 
##                 NextJob.Timestamp, 'Submitted')
        HandleSubmission(Job, Settings, ProblemDict, ResultsQueue)
        #thread.start_new_thread(HandleSubmission, (Job, Settings, ProblemDict, ResultQueue))
        #time.sleep(0.1)
    
    # HandleSubmission will post results to queue. Start 1 thread to handle 
    # results by pulling them off queue & dealing with them. 
    PostResults(ResultsQueue)
    #thread.start_new_thread(PostResults, (ResultQueue,))
    #time.sleep(15)  # which should be more than enough for everything to finish. 
    
    # When this function ends, all threads and the queue they're operating on 
    # go away. In the vast majority of cases, they're long since done anyway; 
    # the producer threads (HandleSubmission) are done and the consumer 
    # (PostResults) is waiting for results that will never come. But just in case
    # something was left over & blocked, the end of function will clean them up. 
    for Dir in SandboxList: 
        try:
            autograde_utilities.Cleanup(Dir)
            os.rmdir(Dir)
        except:   # if anything goes wrong, ignore it; utility script will fix later. 
            pass 



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
    except IOError:
        pass
    except KeyError:
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
    
def SetUpSubmission(Job):
    Settings = ReadSystemConfig()
    if not Settings:
        return False, "Can't read system configuration"
    ProblemPath=os.path.join(Settings['ProblemPath'], '%04d' % Job.ProblemID)
    if not os.path.isdir(ProblemPath):
        return False, "Can't find problem directory"
    else:
        Settings['ProblemPath'] = ProblemPath
    ProblemDict=ReadProblemINI(ProblemPath)
    if not ProblemDict:
        return False, "Can't read problem configuration"
    # Timestamp is a datetime object, and the string version of it has characters
    # that can't be part of a directory path. So fix it. 
    TimeStr = str(Job.Timestamp)
    for ch in ' :.,':
        TimeStr = TimeStr.replace(ch, '')
    # Sandbox dir looks something like: 
    #     Sandbox\abcxyz02072012-01-17120102030000\stuff goes here
    # for problem 0207 submitted by student 'abcxyz' on 2012-01-17 at 12:01:02.030000 PM 
    TempDir = Job.UserID + ('%04s' % str(Job.ProblemNum)) + TimeStr
    ProblemDict['SandboxDir'] = os.path.join(Settings['SandboxDir'], TempDir)
    try:
        os.mkdir(ProblemDict['SandboxDir'])
    except WindowsError:
        ProblemDict['SandboxDir'] = None
        return False, "Can't configure problem." 
    
    return Settings, ProblemDict
    
    
             
     
def HandleSubmission(Job, Settings, ProblemDict, ResultsQueue): 
    ''' handle the traffic-cop aspects of a submission.
    Parameters:
        Job : The job that we're about to process. a named tuple
        ResultsQueue: The queue that we should post results to for later processing. 
    Actions:
        For this problem, retrieve the list of system supplied files (if any) and list of (input,output) tuples.
        Feed the HandleFile function the problem, submission, and single (i, o) pairs until either:
            All input cases have been handled successfully; or
            Any submission has returned anything other than 'Correct.'
        If any case returned anything other than 'Correct': 
           Post this job, Status, ErrMsg to results queue. 
             Example:  job, 'SyntaxError', traceback
             or:       job, 'OutputError', 'Excessive output detected.' 
        otherwise: 
            Post this job, 'Correct', '' to results queue 
    Returns: Nothing 
        '''
    #InputDir = ProblemDict['IOPath']
    # Now process each set of I/O files; continue until all done, or an error is hit. 
    for IOTuple in ProblemDict['IOPairs']:
        if 'Extras' not in ProblemDict:
            ProblemDict['Extras'] = None
        Res, Err = HandleFile(Job, 
                              os.path.join(ProblemDict['IOPath'], IOTuple[0]), 
                              os.path.join(ProblemDict['IOPath'], IOTuple[1]),
                              ProblemDict)
        if Res != 'Correct':
            ResultsQueue.put((Job, Res, Err))  # Post results & exit early 
            #os.rmdir(ProblemDict['SandboxDir'])
            return 
        
    # If we're here, then all files were processed correctly.

    #autograde_utilities.ReportGradeStatus(StudentID, ProblemID, Res) 
    ResultsQueue.put( (Job, 'Correct', ''))
    #os.rmdir(ProblemDict['SandboxDir'])
    return 

def HandleFile(Job, InputFileName, CorrectOutputFileName, ProblemDict): #FileNameToRun, SystemSuppliedFileList=None):
    '''
    Process one student's submission on one set of input data.
    Parameters:
        Job: The named tuple containing, among other things, the files submitted by the student and their contents. 
        InputFileName: The name (including path if needed) of the ONE file with sample input for this test.
        CorrectOutputFileName: The name (including path if needed) of the ONE file with correct output for
            the specified input.
        FileNameToRun: The name (excluding path) of the ONE file that is to run 
          to test the student's code. This must be present in Job or 
          SystemSuppliedFileList.
        SystemSuppliedFileList: The (possibly empty or missing) list of other   
          files (including paths) which are needed to run this problem's code 
          (class files, driver programs, etc)
    Returns:
        tuple of strings (Res, Err). Res is a brief description ('Correct', 
          'Runtime exceeded', etc), and Err is an error message (possibly empty 
          string).
    ''' 
    # set up some labels for later (exit codes)
    ExitMsg = {1:'Translation Error', 2:'Time Limit Exceeded', 3:'Windows Error', \
               4:'Excessive Output', 5:'Submission Error'}

    # Make sure we've got everything we're expecting; if we don't, skip all this. 
    ExpectedFiles = [Filename for (Filename, contents) in Job.Files] 
    try:
        ExpectedFiles += ProblemDict['Extras'] # SystemSuppliedFileList
    except (TypeError, KeyError):  # if there was no list of other needed files. 
        pass
    Expected = [os.path.basename(name).lower().strip() for name in ExpectedFiles]
    if os.path.basename(ProblemDict['Run']).lower().strip() not in Expected:
        Res = "File " + ProblemDict['Run'] + " was expected, but not found."
        Err = ExitMsg[5]
        return Err, Res  
    # even if we're going ahead, we can free up some memory
    del(ExpectedFiles)
    del(Expected)
        
    # Create working (temporary) directory, copy files into it
#    StartPath = os.getcwd()
#    ReadPath = StartPath
    ProblemDict['WritePath'] = os.path.dirname(ProblemDict['FileToRun']) #FileNameToRun)

    try: 
        for f in Job.Files:
            Fname = f[0]
            Code = f[1]
            open(ProblemDict['WritePath']+'/'+os.path.basename(Fname),'w').write(Code)
  
        if ProblemDict['Extras']: # SystemSuppliedFileList:
            for f in ProblemDict['Extras']:
                Code = open(f).read()
                open(ProblemDict['WritePath']+'/'+os.path.basename(f),'w').write(Code)
                
    except IOError:
        #print "System Error. Can't copy necessary file. Contact administrator"
        # try to clean up 
        # autograde_utilities.Cleanup(ProblemDict['WritePath'])
        #os.chdir(StartPath)
        #os.rmdir(WritePath)
        return ('SystemError', 'Contact Administrator or Instructor')
        
    # Setup I/O for program we're testing. 
    Input = open(InputFileName).read()
    os.chdir(ProblemDict['WritePath'])
    open(os.path.join(ProblemDict['WritePath'], 'input.txt'),'w').write(Input)
    
    In = open('input.txt')
    Out = open('output.txt', 'w')
    Err = open('error.txt', 'w')

    # Run that sucker!
    try:
        ExitCode = winprocess.run('python %s' % ProblemDict['Run'], stdin=In, \
                                  stdout=Out, stderr=Err, mSec=5000, desktop='')
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
    if os.path.getsize('output.txt') < 5.0e6:
        Out = open('output.txt').read()
    else:    # more than 5 megabytes output, something's wrong
        ExitCode = 4  # so set error flag
        Out = ''      # & set Out to a safe value, but don't touch file.  

    # grab error message if any. 
    Err = open('error.txt').read()
    
    # Cleanup temporary directory
    autograde_utilities.Cleanup(ProblemDict['WritePath'])
    #os.chdir(StartPath)
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

def RunTest():
    JobType = collections.namedtuple('JobType', ['UserID', 'CourseNum', 'ProblemNum', 'ProblemID', 'Timestamp', 'Files'])
    JobList = list()
    UserID = 'hareb'
    CourseNum="CS101"
    ProblemNum='1'
    ProblemID='0102'
    Timestamp=str(time.localtime())
    f = open('c:/users/public/problems/cs101/0102/example0102.py').read()
    Files = list()
    Files.append( ('solution.py', f))
    Job = JobType(UserID, CourseNum, ProblemNum, ProblemID, Timestamp, Files)
    JobList.append(Job)
    f = open('c:/users/public/problems/cs101/0103/example0103.py').read()
    Files = list()
    Files.append( ('example0103.py', f) ) 
    Timestamp = str(time.localtime())
    Job = JobType(UserID, CourseNum, '002', '0103', Timestamp, Files)
    JobList.append(Job)
    Grade( JobList )
    # print "Done."
    
    
    

if __name__ == '__main__':
    
    connection = autograder.getConnection()
    Cursor = connection.cursor()
    cmd = """UPDATE Jobs SET Status = 'pending' WHERE SequenceNumber = 21"""
    Cursor.execute(cmd)
    connection.commit()
    connection.close()
    Jobs = autograder.getJobs()
    Grade(Jobs)       
    #RunTest()
##    
##    OK, Res, Err = HandleSubmission(1, '0102', ['example0102.py'])
##    print "Your result:", Res
##    if Err:
##        print "Error message:\n", Err
##        
##    if OK:
##        print '\tNeed to update database if this is first success on this problem.'
##    else:
##        print '\tNeed to update database if this is first attempt on this problem.'
##        
