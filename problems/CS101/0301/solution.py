##ID: 0301
##Course: CS101
##Title: Unique Words


text = raw_input("Enter a string: ").split()
unique = []
for word in text:
    meat = word.upper().strip()
    if not(meat in unique):
        unique.append(meat)
print len(unique)
