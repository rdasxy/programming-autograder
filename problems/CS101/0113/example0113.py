# FILES MUST BE IN THE SAME DIRECTORY THAT THIS IS RUN IN

# opens a file and splits the data into a list
# generates a copy of the lowercase letters in the english alphabet
# count how many words start with that letter (case in-sensetive)

import string
letters = string.ascii_lowercase

sentence = open('input.txt', 'r')
data = sentence.read().split()

for letter in letters:
    count = 0
    for word in data:
        if word[0] == letter:
            count += 1
        if word[0] == letter.upper():
            count += 1
    print letter, count
