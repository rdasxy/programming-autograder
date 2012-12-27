def vowels(sent):
    sum = 0
    for x in 'aeiouAEIOOU':
        sum += sent.count(x)
    return sum

    