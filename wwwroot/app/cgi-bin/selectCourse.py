import util
import time, cgi, cgitb
import autograder

cgitb.enable()
form = cgi.FieldStorage()

util.setHTMLContentType()
util.printHTMLHeaders()

course = form.getvalue('course')
loggedInUser = util.getLoggedInIISUser()

problemSet = autograder.getProblemsForCourse(loggedInUser, course)

if problemSet:
  print "<h3>" + problemSet.Title + "</h3>"
  print "<h5>" + problemSet.Description + "</h5><br/>"
  print "<h4>There are " + str(problemSet.nTotalProblems) + " in this set. You have attempted " + str(problemSet.nAttemptedProblems) + " and solved " + str(problemSet.nSolvedProblems) + "</h4>"
  print "<br/><br/><h6>* indicates unsolved and unattempted problems</h6>"
  for problem in problemSet.Probs:
    annotation = ""
    if problem.bSolved:
      annotation = "<i>Solved</i>"
    elif problem.bAttempted:
      annotation = "<i>Attempted</i>"
    else:
      annotation = "*"
    print "<h4><b><a href='./problem.py?course=" + course + "&problem=" + str(problem.ProblemId) + "'>" + str(problem.ProblemId) + ".</b> " + problem.Title + "</a> " + annotation + "</h4><br/>"
    print "<i>" + problem.ShortSummary + "</i><br/><br/>"
else:
  print "If you are seeing this message, an invalid ProblemSet object was returned"
util.printHTMLClosing()

