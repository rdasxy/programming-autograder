# FILES MUST BE IN THE SAME DIRECTORY AS THIS IS RUN

# read a file
# count the number of words in file
# close the file
# print the number of words counted

f = open(raw_input())
counting = f.read().split()
f.close()
print len(counting)
