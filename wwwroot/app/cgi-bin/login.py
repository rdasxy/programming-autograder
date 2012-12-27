import util
import cgi, cgitb
import autograder

cgitb.enable()

def listCourses(courses, loggedInUser):
  if courses:
    util.setHTMLContentType()
    util.printHTMLHeaders()
    print "Welcome " + loggedInUser
    print "<h3>Please select a course:</h3><br/>"
    for course in courses:
      print "<a href='./selectCourse.py?course=" + course.HTMLSafeName + "'>" + course.name + "</a><br/>"
  else:
    util.setHTMLContentType()
    util.printHTMLHeaders()
    print "You do not seem to be enrolled in a course that uses this system. If you think you've received this message in error, please contact your instructor."

#This is where execution starts
loggedInUser = util.getLoggedInIISUser()

courses = autograder.getCoursesForUser(loggedInUser)
listCourses (courses, loggedInUser)

