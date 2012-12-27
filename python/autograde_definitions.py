import collections

collections.namedtuple(JobType, ['UserID', 'CourseNum', 'ProblemNum', 'ProblemID', 'Timestamp', 'Files']) 

#Expectations: 
#    UserID: This is the SSO ID. 
#    CourseNum: CS101, CS282, etc. 
#    ProblemNum: The number of the problem as it's presented on the website. 
#    ProblemID: The number of the problem as it's stored on the back-end (the 4 digit number we assigned @ Python & Pizza) 
#    Timestamp: A datetime object, the time it was submitted to the website. 
#    Files: A list of tuples: [('Filename1', 'Contents of file1'), ('Filename2', 'Contents of file2'), etc] 
    
#Question: If this is defined somewhere else, does the back end need to run the function or 
 #declare the namedtuple again? Or can it just have a parameter called Job and start 
 #referring to Job.UserID? 