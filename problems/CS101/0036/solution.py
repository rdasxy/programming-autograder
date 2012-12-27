# Prompt the use to "Enter some numbers: "
# The user should enter a few numbers, separated by spaces, all on one line
# Print every other number, starting with the first, one to a line

seq = raw_input("Enter some numbers: ")
seq = [int(s) for s in seq.split()]
for s in seq[::2]:
    print s
    