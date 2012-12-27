def consonants(sent):
    sum = 0
    for x in sent:
        if ('a' <= x <= 'z' or 'A' <= x <= 'Z') and x not in 'aeiouAEIOU':
            sum += 1
    return sum

    