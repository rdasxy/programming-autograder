# Prompt the use to "Enter some numbers: "
# The user should enter a few numbers, separated by spaces, all on one line
# Sort the resulting sequence, then print all the numbers but the first two and the last two,
# one to a line.

seq = raw_input("Enter some numbers: ")
seq = [int(s) for s in seq.split()]
seq.sort()
for s in seq[2:-2]: 
    print s