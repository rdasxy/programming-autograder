from __future__ import division
import pymysql, csv, codecs, os, re
import base64, uuid
from collections import namedtuple
from datetime import datetime, date, timedelta

JobType = namedtuple('JobType', 'UserID CourseNum ProblemNum ProblemID Timestamp Files')
Course = namedtuple('Course', 'HTMLSafeName name')
ProblemSet = namedtuple('ProblemSet', 'Title Description nTotalProblems nAttemptedProblems nSolvedProblems Probs')
ProblemSetItem = namedtuple('ProblemSetItem', 'Title ProblemId ShortSummary bSolved bAttempted')
DetailedProblem = namedtuple('DetailedProblem', 'Title Details bSolved nFiles')

class AutograderError(Exception):
    pass

def getConnection():
    try:
        params = {'host':'KC-csrv-mysql', "user":"SCEAutoGrdr",
             "passwd":"XNHyJ9V4HTaC","db":"SCE-AutoGrdr", "use_unicode": True}
        connection = pymysql.connect(**params)
    except pymysql.err.OperationalError:
        raise AutograderError("Database unavailable.  Please try again later.")
    return connection

def getCoursesForUser(userID):
    # Returns a possibly empty list of courses to which the user has access
    
    try:
        connection = getConnection()
        cursor = connection.cursor()
        query = "SELECT CourseNumber FROM Roll WHERE UserID = '%s'" % userID
        cursor.execute(query)
        courses = [c for (c,) in cursor.fetchall()]
        answer = []
        for course in courses:
            query = "SELECT * FROM Courses WHERE CourseNumber = '%s'" % course
            cursor.execute(query)
            answer.append(Course._make(cursor.fetchone()))
        connection.close()
    except AutograderError:
        raise
    return answer

def getProblemsForCourse(userID, course):
    try:
        connection = getConnection()
        cursor = connection.cursor()
        Problem = namedtuple("Problem", "title number desc")
        query = """SELECT DISTINCT ProblemNumber FROM Attempts WHERE 
                         UserId = '%s' AND CourseNumber = '%s'  """ %(userID, course)
        cursor.execute(query)
        nAttempted  = len(cursor.fetchall())
        query +="AND Outcome = 'success'"
        cursor.execute(query)
        nSolved  = len(cursor.fetchall())
        query = """SELECT Title, ProblemNumber, Description FROM Problems WHERE CourseNumber = '%s'""" %course
        cursor.execute(query)
        probs = map(Problem._make, cursor.fetchall())
        items = []
        for prob in probs:
            query = """SELECT DISTINCT Outcome FROM Attempts WHERE
                             UserId = '%s' AND CourseNumber = '%s' AND ProblemNumber = %d
                         """ %(userID, course, prob.number)
            cursor.execute(query)
            outcomes = [out for (out, ) in cursor.fetchall()]
            if not outcomes:
                bSolved = bAttempted = False
            else:
                bAttempted = True
                bSolved = 'success' in outcomes
            items.append(ProblemSetItem(prob.title, prob.number, prob.desc, bSolved, bAttempted))
        query = "SELECT CourseTitle FROM Courses WHERE CourseNumber = '%s'" % course
        cursor.execute(query)
        name = cursor.fetchone()[0]
        title = "Problems for %s" %name
        desc = ""
        answer = ProblemSet(title, desc, len(probs), nAttempted, nSolved, items)
        connection.close()
    except AutograderError:
        raise
    return answer

def getJobs():
    # returns a list of all pending jobs
    try:
        Job = namedtuple('Job', 'UserID CourseNumber ProblemNumber ProblemID Status SequenceNumber Timestamp')
        connection = getConnection()
        cursor = connection.cursor()
        answer = []
        cursor.execute("SELECT * FROM Jobs")
        jobs = map(Job._make, cursor.fetchall())
        for job in jobs:
            if job.Status != 'pending':
                continue
            query = "SELECT FileName, FileContents FROM JobFiles WHERE JobNumber = %s" %job.SequenceNumber
            cursor.execute(query)
            files = cursor.fetchall()
            answer.append(JobType(job.UserID, job.CourseNumber, job.ProblemNumber, job.ProblemID, job.Timestamp, files))
            cmd = "UPDATE Jobs SET Status = 'submitted' WHERE SequenceNumber = %d" % job.SequenceNumber
            cursor.execute(cmd)
        connection.commit()
        connection.close()
    except AutograderError:
        answer = []
    return answer
    
def updateRoll(course, section, filename):

    # filename is a Blackbard CSV roster
    # students not already on the roll are added
    # If a student is already on the roll in a different course, he gets the same UUID

    try:
        roll = csv.DictReader(codecs.open(filename,'rb', encoding = 'utf-8-sig'))
        connection = getConnection()
        cursor = connection.cursor()
        cn = course
        sn = section
        cursor.execute("SELECT DISTINCT UserID from Roll")
        onDB = [s for (s,) in cursor.fetchall()]
        cursor.execute("SELECT UserID from Roll where CourseNumber = '%s'" %course)
        inCourse = [s for (s,) in cursor.fetchall()]
        base = 'INSERT INTO Roll (CourseNumber, SectionNumber,  UserID, UUID, FirstName, LastName)'
        for student in roll:
            un = student['Username']
            if un not in inCourse:
                fn = student['First Name']
                ln = student['Last Name']
                if  un not in onDB:
                    uu = base64.urlsafe_b64encode(uuid.uuid4().bytes_le)
                else:
                    cursor.execute("SELECT UUID FROM Roll WHERE UserID = '%s'" % un)
                    (uu,) = cursor.fetchone()
                cmd = base + "VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (cn, sn, un, uu, fn, ln)
                cursor.execute(cmd)
        cursor.close()
        connection.commit()
        connection.close()
    except AutograderError:
        raise

def ReportGradeStatus(attempt, outcome):
# (JobType, string) --> None

# Record the outcome in Attempts table
# Delete the job from the Jobs table
# Delete associated files from the JobFiles table
    
    try:
        connection = getConnection()
        cursor = connection.cursor()
        user = attempt.UserID
        course = attempt.CourseNum
        problemId = attempt.ProblemID
        timestamp = attempt.Timestamp
        query = """SELECT ProblemNumber FROM Problems WHERE 
                         CourseNumber = '%s' AND
                         ProblemID = %d""" % (course, problemId)
        cursor.execute(query)
        problemNum = cursor.fetchone()[0]
        query = """SELECT DISTINCT Outcome FROM Attempts WHERE
                   UserID = '%s' AND CourseNumber = '%s'
                   AND ProblemNumber = %d""" % (user, course, problemNum)
        cursor.execute(query)
        results = [out for (out,) in cursor.fetchall()]
        if not results:
            status = 'new'
        elif 'success' in results:
            status = 'old'
        else:
            status = 'pending'
        cmd = 'INSERT INTO Attempts(UserId, CourseNumber, Timestamp, ProblemNumber, Outcome, Status)'
        cmd += "VALUES('%s', '%s', NOW(), %d, '%s', '%s')" % (user, course, problemNum, outcome, status)
        cursor.execute(cmd)
        
        query = """SELECT SequenceNumber FROM Jobs WHERE
                          CourseNumber = '%s' AND 
                          ProblemID = %s AND 
                          Userid = '%s' AND
                          Timestamp = '%s'
                    """ %(course, problemId, user, timestamp)
        cursor.execute(query)
        seq = cursor.fetchone()[0]
        
        cmd = """DELETE FROM JobFiles WHERE JobNumber = %d""" % seq
        cursor.execute(cmd)
        cmd = """DELETE FROM Jobs WHERE SequenceNumber = %d""" % seq
        cursor.execute(cmd)
        
        cmd = """UPDATE Attempts SET Status = '%s' WHERE
                          CourseNumber = '%s' AND 
                          ProblemNumber = %s AND 
                          Userid = '%s' AND
                          Timestamp ='%s'
                    """ %(outcome, course, problemNum, user, timestamp)
        cursor.execute(cmd)
        connection.commit()
        connection.close()
    except AutograderError:
        raise

def populateProblems(course, filename):
    # Update the problem list for a course
    # Problem numbers are assigned automatically

    def escape(s):
        return re.sub(r"'", r"\'", s)  # escape single quotes in string s

    try:
        baseDir = os.path.join('C:\\users','public','problems',course)
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT ProblemNumber FROM Problems WHERE CourseNumber = '%s'" % course)
        nums = [num for (num,) in cursor.fetchall()]
        next1 = 1 + ( max(nums) if nums else 0 )
    
        cursor.execute("SELECT ProblemId FROM Problems WHERE CourseNumber = '%s'" % course)
        probs = cursor.fetchall()
        base = 'INSERT INTO Problems(ProblemId, CourseNumber, ProblemNumber, Title, Description, NumFiles)'
        with open(filename) as fin:
            for prob in fin:
                prob = int(prob)
                if (prob,) in probs:
                    print("Problem %s already assigned to %s" % (prob, course))
                    continue
                probDir = os.path.join(baseDir, "%04d" % prob)
                desc = open(os.path.join(probDir, 'desc.html')).read()
                with open(os.path.join(probDir, 'template.txt')) as fin:
                    for line in fin:
                        if line.startswith('Title:'):
                            title = line[6:].strip()
                        elif line.startswith('Upload:'):
                            numFiles = len(line.split()) - 1
                cmd = base + ("VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (prob, course, next1, escape(title), escape(desc), numFiles))
                cursor.execute(cmd)
                next1 += 1
        connection.commit()
        connection.close()
    except AutograderError:
        raise

def getProblemID(course, problemNumber):
    # Return the problem ID, given the course number and problem number

    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT ProblemID FROM Problems where CourseNumber = '%s' and ProblemNumber = %d"
                       % (course, problemNumber))
        ident = cursor.fetchone()
        connection.close()
    except AutograderError:
        raise
    return ident

def getProblemDesc(UserID, course, problemNumber):
    try:
        Detail = namedtuple("Detail", "title summary numFiles")
        connection = getConnection()
        cursor = connection.cursor()
        query = """SELECT DISTINCT Outcome FROM Attempts WHERE
                          UserId = '%s' AND CourseNumber = '%s' AND ProblemNumber = %s""" % (UserID, course, problemNumber)
        cursor.execute(query)
        try:
            outcomes = [out for (out,) in cursor.fetchall()]
        except pymysql.Error:
            solved = False
        else:
            solved = 'success' in outcomes
        query = """SELECT Title, Description, NumFiles FROM Problems WHERE
                          CourseNumber = '%s' AND
                          ProblemNumber = %s""" % (course, problemNumber)
        cursor.execute(query)
        ans = cursor.fetchone()
        d = Detail(*ans)
        answer = DetailedProblem(d.title, d.summary, solved, d.numFiles) 
        connection.close()
    except AutograderError:
        raise
    return answer
    
def grade(UserID, course, problemNumber, files):
    # Adds job to Jobs table for later execution
    try:
        connection = getConnection()
        cursor = connection.cursor()
        query = """SELECT ProblemId FROM Problems WHERE CourseNumber = '%s' AND
                         ProblemNumber = %s""" % (course, problemNumber)
        cursor.execute(query)
        pid = cursor.fetchone()[0]
        cmd = """INSERT INTO Jobs(Userid, CourseNumber, ProblemNumber, ProblemID, Status, SequenceNumber, Timestamp)"""
        cmd += " VALUES('%s', '%s', %s, %s, 'pending',  NULL, NOW()) " % (UserID, course, problemNumber, pid)
        cursor.execute(cmd)
        for fileitem in files:
            cmd = "INSERT INTO JobFiles(JobNumber, FileName, FileContents)"
            # For MySQL, we escape single quotes in the file contents by doubling them: ' --> ''
            # The first argument to re.sub is a duble-quoted single quote.
            # The second argument is two single quotes, double-quoted.
            cmd += "VALUES(LAST_INSERT_ID(), '%s', '%s')" % (fileitem.filename, re.sub("'","''",fileitem.value)) 
            cursor.execute(cmd)
        connection.commit()
        connection.close() 
    except AutograderError:
        raise
                 
def gradeCourse(course):
    # Produce a listing of solutions to date
    # A solved problem is counted only once
    # Report by section, alphabetically by last name within section
    # Score is total for semester to date, and should REPLACE any prior grade

    try:
        Grade = namedtuple('Grade', 'Section UserID LastName FirstName Score')
        connection = getConnection()
        cursor = connection.cursor()
        query = """SELECT SectionNumber, UserID, LastName, FirstName, COUNT(*) FROM
                   (SELECT DISTINCT UserID, ProblemNumber FROM Attempts
                        WHERE CourseNumber = '%s' AND Outcome = 'success') AS Successes
                    INNER JOIN
                   (SELECT * FROM Roll WHERE SectionNumber AND CourseNumber = '%s') AS Enrollees
                    USING(UserID)
                    GROUP BY UserID ORDER BY SectionNumber, LastName""" % (course  , course)
        cursor.execute(query)
        grades = map(Grade._make, cursor.fetchall())
        sections = set([g.Section for g in grades])
        for section in sections:
            print "\nSection %s" %section
            print "%15s %15s %15s %s\n" % ('UserID', 'LastName', 'FirstName', 'Score')
            for grade in [g for g in grades if g.Section == section]:
                print "%15s %15s %15s %3d" %grade[1:]
        connection.close()
    except AutograderError:
        raise

def studentReport(userID, course, mode='verbose'):

    Attempt = namedtuple('Attempt', 'time prob outcome status')

    def trim(attempt):
        return Attempt(attempt.time.date(), attempt.prob, attempt.outcome, attempt.status)

    def summary(rows, period):
        today = datetime.today().date()
        epoch  = today - timedelta(days = period)
        current  = [row for row in rows if row.time >= epoch]
        currentSolns = [r.prob for r in current if r.outcome == 'success']
        currentSet = set(currentSolns)
        newAttempts = [r for r in current if r.status == 'new']
        newSolns = [r for r in current if r.outcome == 'success' and 'r.status' != 'old']


        print('Past %d Days:' % period)
        print('%8d Total Attempts' % len(current))
        print('%8d Total Solutions' % len(currentSolns))
        print('%8d Distinct Solutions' % len(currentSet))
        print('%8d New Problems Solved' % len(newAttempts))
        print('%8d New Problems Attempted' %len(newSolns))
        print

    try:
        connection = getConnection()
        cursor = connection.cursor()
        parms = (userID, course)
    
        cursor.execute("SELECT FirstName, LastName FROM Roll WHERE UserID = '%s' AND CourseNumber = '%s'" % parms)
        user = cursor.fetchone()
        if not user:
            print("No student '%s' in '%s'" % parms)
            connection.close()
            return
        (fn, ln) = user
        print fn, ln
        if mode == 'verbose':
            print "\n%s %s %12s %12s\n" % ('   Date   ', ' Problem', 'Result', 'Status')
            query = """SELECT Timestamp, ProblemNumber, Outcome, Status FROM Attempts
                       WHERE UserId = '%s' AND CourseNumber = '%s'""" % parms
            cursor.execute(query)
            rows = map(Attempt._make, cursor.fetchall())
            for idx, row in enumerate(rows):
                if idx == 0 or row.time.date() != rows[idx-1].time.date():
                    print "%s %8d %12s %12s" % (row.time.date().strftime('%m/%d/%Y'), row.prob, row.outcome, row.status)
                else:
                    print "%10s %8d %12s %12s" % ('', row.prob, row.outcome, row.status)
            print
            print 'Semester to Date:'
            print "%8d Total Attempts" % len(rows)
            good = [r.prob for r in rows if r.outcome == 'success']
            print "%8d Total Solutions" % len(good)
            print "%8d Distinct Solutions" % len(set(good))
            attempted = set([r.prob for r in rows])
            solved = set(good)
            unsolved = list(attempted.difference(solved))
            unsolved.sort()
            print "         Solved:",
            for p in solved:
                print p,
            print
            print "         Unsolved:",
            for p in unsolved:
                print p,
            print
            print
    
            rows = map(trim, rows)
            summary(rows, 28)
            summary(rows, 14)
            summary(rows, 7)
    
            connection.close()
    except AutograderError:
        raise

def CourseReport(course):
    try:
        Attempt = namedtuple('Attempt', 'section userid lastname firstname prob outcome')
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT SectionNumber FROM Roll WHERE CourseNumber = '%s'" %course)
        sections = sorted([s for (s,) in cursor.fetchall()])
        query = """SELECT SectionNumber, UserID, LastName, FirstName, ProblemNumber, Outcome FROM
                   (SELECT UserID, ProblemNumber, Outcome FROM Attempts
                        WHERE CourseNumber = '%s' AND NOT Status = 'old'
                        AND DATE(Timestamp) >= SUBDATE(CURDATE(), INTERVAL 7 DAY)) AS Tries
                    INNER JOIN
                   (SELECT * FROM Roll WHERE SectionNumber AND CourseNumber = '%s') AS Enrollees
                    USING(UserID)
                    ORDER BY SectionNumber, LastName""" % (course, course)
        cursor.execute(query)
        attempts = map(Attempt._make, cursor.fetchall())
        for section in sections:
            print "%s Section %s Activity Last Seven Days\n" % (course, section)
            print "%sName%s Solutions Attempts Ratio\n"  %(8*' ', 8*' ')
            students = set([(a.lastname, a.firstname, a.userid) for a in attempts if a.section == section])
            for (last, first, userID) in sorted(students):
                tries = [a for a in attempts if a.userid == userID]
                solns = len([a for a in tries if a.outcome == 'success'])
                tries = len(tries)
                ratio = 100*(solns/tries)
                print "%-20s %9d %8d %5.0f %%" % ((last +', ' + first)[:20], solns, tries, ratio)
            print
        print ("Generated %s" % datetime.now().strftime("%I:%M %p %m/%d/%Y"))
        connection.close()
    except AutograderError:
        raise

def problemReport(course):
    from decimal import Decimal  # for some reason, the query is returning decimal.Decimal objects

    class ReportLine(object):
        def __init__(self, r):

            f = lambda x: int(x) if x else 0

            # attr names: s = semester, m = month,, w = week, t = tries, g = good, r = ratio

            (self.id, self.st, self.sg, self.mt, self.mg, self.wt, self.wg) = map(f, r)

            self.sr = 100 * self.sg // self.st if self.st else 0
            self.mr = 100 * self.mg // self.mt if self.mt else 0
            self.wr = 100 * self.wg // self.wt if self.wt else 0

        def __str__(self):
            return ("%7d%9d%5d%6d %%%6d%5d%6d %%%5d%5d%6d %%"
                   %(self.id, self.st, self.sg, self.sr, self.mt, self.mg, self.mr, self.wt, self.wg, self.wr))

    def printTitles():
        print "               Semester         Last 4 Weeks        Last Week"
        print "Problem    Tries Okay Ratio   Tries Okay Ratio  Tries Okay Ratio"

    try:
        connection = getConnection()
        cursor = connection.cursor()
    
        cmd = "DROP TABLE Tries, Good"
        try:
            cursor.execute(cmd)
        except pymysql.Error:
            pass
    
        cmd = """CREATE TABLE Tries
                  SELECT ProblemNumber AS Id, DATE(Timestamp) AS Date, COUNT(*) As Freq
                    FROM Attempts INNER JOIN Roll USING(UserID, CourseNumber)
                      WHERE CourseNumber = '%s'
                        AND NOT Status = 'old'
                        AND SectionNumber
                    GROUP By Id, Date
                    ORDER BY Id, Date""" %course
        cursor.execute(cmd)
    
        cmd = """CREATE TABLE Good
                  SELECT ProblemNumber AS Id, DATE(Timestamp) AS Date, COUNT(*) As Freq
                    FROM Attempts INNER JOIN Roll USING(UserID, CourseNumber)
                      WHERE CourseNumber = '%s'
                        AND Outcome = 'success'
                        AND NOT Status = 'old'
                        AND SectionNumber
                    GROUP BY Id, Date
                    ORDER BY Id, Date""" %course
        cursor.execute(cmd)
    
        query = """SELECT Id, St.Cnt, Sg.Cnt, Mt.Cnt, Mg.Cnt, Wt.Cnt, Wg.Cnt FROM
                    (SELECT Id, SUM(Freq) AS Cnt FROM Tries GROUP BY Id) AS St
                    LEFT JOIN
                    (SELECT Id, SUM(Freq) AS Cnt FROM Good GROUP BY Id) AS Sg
                    Using(Id)
                    LEFT JOIN
                    (SELECT Id, SUM(Freq) AS Cnt FROM Tries WHERE
                       Date >= DATE_SUB(DATE(NOW()), INTERVAL 28 DAY) GROUP BY Id) AS Mt
                    Using(Id)
                    LEFT JOIN
                    (SELECT Id, SUM(Freq) AS Cnt FROM Good WHERE
                       Date >= DATE_SUB(DATE(NOW()), INTERVAL 28 DAY) GROUP BY Id) AS Mg
                    Using(Id)
                    LEFT JOIN
                    (SELECT Id, SUM(Freq) AS Cnt FROM Tries WHERE
                       Date >= DATE_SUB(DATE(NOW()), INTERVAL 7 DAY) GROUP BY Id) AS Wt
                    Using(Id)
                    LEFT JOIN
                    (SELECT Id, SUM(Freq) AS Cnt FROM Good WHERE
                       Date >= DATE_SUB(DATE(NOW()), INTERVAL 7 DAY) GROUP BY Id) AS Wg
                    Using(Id)
                    ORDER BY Id"""
        cursor.execute(query)
        results = map(ReportLine, cursor.fetchall())
    
        for idx, r in enumerate(results):
            if idx % 25 == 0:
                print
                printTitles()
            if idx % 5 == 0:
                print
            print r
    
        print ("\nGenerated %s" % datetime.now().strftime("%I:%M %p %m/%d/%Y"))
    
        cmd = "DROP TABLE Tries, Good"
        cursor.execute(cmd)
        connection.commit()
        connection.close()
    except AutograderError:
        raise

def populateCourses(courses):
    try:
        connection = getConnection()
        cursor = connection.cursor()
        base = "INSERT INTO Courses(CourseNumber, CourseTitle)"
        for course in courses:
            cmd = base+"VALUES('%s', '%s')" %course
            cursor.execute(cmd)
        connection.commit()
        connection.close()
    except AutograderError:
        raise

if __name__ == '__main__':
    #initiateTestBed()
    #gradeCourse('cs282')
    #gradeCourse('cs101')
    #print validate('spatzs')
    #v = validate('aappb')
    #print UUIDCourses(v[0][1])
    #studentReport('spatzs', 'cs101')
    #generateAttempts()
    #studentReport('aappb', 'cs101')
    #generateAttempts()
    #gradeCourse('cs101')
    #studentReport('aemz86', 'cs101')
    #CourseReport('cs282')
    #problemReport('cs101')
    #answer = getTimes()
    #answer = getTimes()
    #print answer
    #print type(answer)
    #getProblemsForCourse('dasrid', 'cs101')
    #getProblemDesc('spatzs', 'cs101', '1')
   #grade('spatzs', 'cs101', '1', [])
    getProblemsForCourse('spatzs', 'cs101')
    pass

    
    



