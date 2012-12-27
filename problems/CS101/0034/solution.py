# Prompt the user to "Enter a string ".  Find the first colon that occurs in the string.
# Delete everything that comes after the colon, and print the result.  If there is no colon, 
# the original string should be printed.

test = raw_input("Enter a string ")
idx = test.find(':')
if idx != -1:
    print test[:idx]
else:
    print test
    
