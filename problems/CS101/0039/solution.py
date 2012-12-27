# poker.py
# Prompt the user to "Enter a hand: "
# The user should enter 5 characters, separated by spaces
# If all the characters are different, print "Bust"
# If two characters are the same,and all the rest are different, print "Pair"
# If there are two pairs of equal characters, and the fifth character is different,
# print "Two pair"
# If there are three equal characters and the other two are different, print "Three of a kind"
# If there are three characters of one value, and two of a second value, print "Full house"
# If there are four equal characters, and the other character is different, print "Four of a kind"
# If all characters are the same, print "Five of a kind"


# Example:
# Enter a hand A Q 8 9 8
# Pair

hand = raw_input("Enter a hand ").split()
hand.sort()

ranks = set(hand)
if len(ranks) == 1:
    print "Five of a kind"
elif len(ranks) == 5:
    print "Bust"
elif  len(ranks) == 4:
    print "Pair"
elif len(ranks) == 3:
    for card in hand:
        if hand.count(card) == 3:
            print "Three of a kind"
            break
        if hand.count(card) == 2:
            print "Two pair"
            break
elif len(ranks) == 2:
    for card in hand:
        if hand.count(card) in (1,4):
            print "Four of a kind"
            break
        if hand.count(card) in (2, 3):
            print "Full house"
            break

    