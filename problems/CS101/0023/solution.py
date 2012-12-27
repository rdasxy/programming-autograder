shift = int(raw_input("How many numbers to shift?"))
text = raw_input("Type in a string")
caesar = dict()
for idx, letter in enumerate('abcdefghijklmnopqrstuvwxyz'):
    caesar[letter] = chr( ord('a') + (idx+shift) % 26)

output = ''
for t in text:
    output += caesar[t]
print output

    