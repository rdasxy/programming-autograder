# FILES MUST BE IN THE SAME DIRECTORY AS THIS IS RUN IN

# opens a file that contains two different file names
# then opens those files and creates a dictionary
#   using inputOne as the key
#   using inputTwo as the values
# opens a file named output.txt
# then prints the dictionary as a str() into output.txt

f = open('input.txt', 'r')
names = f.read().split()
f.close()
inputOne = open(names[0], 'r')
inputTwo = open(names[1], 'r')

inputKeys = inputOne.read().split()
inputValues = inputTwo.read().split()

inputOne.close()
inputTwo.close()

myDict = {}

i = 0
for key in inputKeys:
    myDict[key] = inputValues[i]
    i = i+1

writeOut = open('output.txt', 'w')
writeOut.write(str(myDict))
writeOut.close()
