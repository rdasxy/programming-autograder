##ID: 0303
##Course: CS101
##Title: Backwards Words 

meat = raw_input("Enter a string: ")
meatList = meat.split()
backwardsList =  meatList[::-1]
for word in backwardsList:
    print word,
