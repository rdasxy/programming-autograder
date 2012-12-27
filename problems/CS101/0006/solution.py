sentence = raw_input("Type in a sentence.").split()
maxlen = -1
for word in sentence:
    if len(word) > maxlen:
        longest = word
        maxlen = len(word)
print(longest)

