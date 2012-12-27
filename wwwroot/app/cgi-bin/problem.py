import util
import time, cgi, cgitb
import autograder

cgitb.enable()

form = cgi.FieldStorage()

util.setHTMLContentType()
util.printHTMLHeaders()

course = form.getvalue('course')
problem = form.getvalue('problem')

loggedInUser = util.getLoggedInIISUser()

detailedProblem = autograder.getProblemDesc(loggedInUser, course, problem)

if detailedProblem:
  print "<h3>" + detailedProblem.Title + "</h3>"
  if detailedProblem.bSolved:
    print "<h4>You've already solved this problem</h4>"
  print "<h5>" + detailedProblem.Details + "</h5><br/>"
  print "Upload file(s)"
  print "<form method='post' action='./grade.py' enctype='multipart/form-data'>"
  print "<input name='course' type='hidden' value='" + course + "'/>"
  print "<input name='problem' type='hidden' value='" + problem + "'/>"
  print "<input name='fileCount' type='hidden' value='" + str(detailedProblem.nFiles) + "'/>"
  for i in range(0,detailedProblem.nFiles):
    print "<input type='file' name='file" + str(i) + "'/><br/><br/>"
  print "<input type='submit' value='submit'>"
  print "</form>"
else:
  print "If you are seeing this message, an invalid DetailedProblem object was returned"
util.printHTMLClosing()

