# Prompt the user to "Enter a string: ".  
# Print characters 3 through 6
# Replace characters 3 through 6 by the string "hello", and print the result.

test = raw_input("Enter a string: ")
print test[3:6]
test = test[:3] + "hello" + test[6:]
print test

