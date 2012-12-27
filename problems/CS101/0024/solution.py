abbrev = dict()
abbrev['u'] = 'you'
abbrev['ur'] = 'your'
abbrev['c'] = 'see'
abbrev['l8r'] = 'later'
abbrev['fyi'] = 'for your information'
abbrev['<3'] = 'love'
abbrev['lo'] = 'laugh out loud'
abbrev[':)'] = 'smiley face'
text = raw_input("Input a string").split()
for word in text:
    try:
        print abbrev[word],
    except KeyError:
        print word,
        



       