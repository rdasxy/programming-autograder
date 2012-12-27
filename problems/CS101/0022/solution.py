text = raw_input("Type in a string").split()
freq = dict()
for word in text:
    if not word in freq:
        freq[word] = 1
    else:
        freq[word] += 1
often = max(freq.values())
times = len([word for word in freq if freq[word] == often])
print often
print times


