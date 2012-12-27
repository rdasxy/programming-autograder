import util
import time, cgi, cgitb
import autograder

cgitb.enable()

loggedInUser = util.getLoggedInIISUser()
form = cgi.FieldStorage()
course = form.getvalue('course')
problem = form.getvalue('problem')

util.setHTMLContentType()
util.printHTMLHeaders()

fileCount = int(form.getvalue('fileCount'))
files = []

for i in range (0, fileCount):
  fileitem = 'file' + str(i)
  if (form.has_key(fileitem)):
    files.append(form[fileitem])
autograder.grade(loggedInUser, course, problem, files)
print "<h1>You file(s) have been successfully uploaded!</h1><br/>"
print "<h2>You should hear back from us in an email.</h2>"
util.printHTMLClosing()
