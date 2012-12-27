from autograder import getConnection, updateRoll, populateProblems, populateCourses

# This file is for generating test data only

def generateAttempts():
    # For testing only

    import random
    connection = getConnection()
    cursor = connection.cursor()
    next1 = 1
    cursor.execute("SELECT DISTINCT CourseNumber FROM Roll")
    courses = cursor.fetchall()
    base = 'INSERT INTO Attempts(UserID, CourseNumber, Timestamp, ProblemNumber, Outcome, Status)'
    for (course,) in courses:
        cursor.execute("SELECT ProblemNumber from Problems WHERE CourseNumber = '%s'" % course)
        probs = [p for (p,) in cursor.fetchall()]
        cursor.execute("SELECT DISTINCT SectionNumber FROM Roll WHERE CourseNumber = '%s'" % course)
        sections = cursor.fetchall()
        for (section, ) in sections:
            cursor.execute("""SELECT UserID FROM Roll
                               WHERE CourseNumber = '%s' AND SectionNumber = '%s'
                               """ % (course, section))
            students = [s for (s,) in cursor.fetchall()][:3]
            for student in students:
                days = sorted(random.sample(range(1,60),40), reverse=True)
                minute = 0
                for day in days:
                    for k in range(10):
                        p = random.sample(probs, 1)
                        query = """SELECT DISTINCT Outcome FROM Attempts WHERE
                                CourseNumber = '%s' AND ProblemNumber = %d AND
                                UserID = '%s'""" % (course, p[0], student)
                        cursor.execute(query)
                        results = [r for (r,) in cursor.fetchall()]
                        if not results:
                            status = 'new'
                        elif 'success' in results:
                            status = 'pending'
                        else:
                            status = 'old'
                        if random.random() > .6:
                            outcome = 'success'
                        else:
                            outcome = 'other'
                        cmd = base+"""VALUES('%s', '%s',
                                      DATE_ADD(DATE_SUB(NOW(), INTERVAL %d DAY), INTERVAL %d MINUTE), %d,
                              '%s', '%s')""" % (student,  course, day, minute, p[0], outcome, status)
                        cursor.execute(cmd)
                        minute += 1
    connection.commit()
    connection.close()
    
def initiateTestBed():
    # Once the schema is finalized, we can just run autograder.sql here, instead
    # of deleting all rows from the tables.

    connection = getConnection()
    cursor = connection.cursor()
    for table in ("Roll", "Attempts", "Problems"):
        cursor.execute("DELETE FROM %s" %table)
    connection.commit()
    #updateRoll('cs282', '1', 'cs441.csv')
    updateRoll('cs101', '1', 'mwf.csv')
    updateRoll('cs101', '2', 'tuth.csv')
    updateRoll('cs101', '3', '282.csv')
    populateProblems('cs101', 'probs2.txt')
    populateCourses([('cs101', "CS 101")])
    #populateProblems('cs282', 'probs.txt')
    generateAttempts()

    connection.close()
    
if __name__ == '__main__':
    initiateTestBed()
    
    