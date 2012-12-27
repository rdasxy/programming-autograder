import cgitb, os, Cookie
cgitb.enable()

def setHTMLContentType():
  print "Content-Type: text/html"

def printHTMLHeaders():
  print #Signals end of HTML headers

  print """
  <html>
    <head>
      <title>UMKC SCE Autograder</title>
    </head>
    <body>
    <center>
      <img src='../imgs/UMKC.png'/>
      <h1>UMKC School of Computing and Engineering Autograding System</h1>
    </center>
    <hr>
  """

def printHTMLClosing():
  print """
    <hr>
    <center>
      <h4>UMKC School of Computing and Engineering</h4>
      <br/>
      <img src='../imgs/titlebar.jpg'/>
    </center>
    </body>
  </html>
  """

def getLoggedInIISUser():
  return os.environ['LOGON_USER'] if  os.environ.has_key('LOGON_USER') else None
