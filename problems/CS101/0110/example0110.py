def concat(list1, list2):
    myDict = dict()
    for i in range(0, len(list1)):
        myDict[list1[i]] = list2[i]
    return myDict
