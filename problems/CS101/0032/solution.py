def palindrome(word):
    if len(word) <= 1:
        return True
    word = [a.lower() for a in word if a.isalpha()]
    return (word[0] == word[-1]) and palindrome(word[1:-1])

word = raw_input("Enter a string:")
if palindrome(word):
    print "yes"
else:
    print "no"
    
                                              
                                            