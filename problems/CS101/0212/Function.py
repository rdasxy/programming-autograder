def AddUp(A, B):
	return A+B 

def EitherOr(list1, list2): 
	S1 = set(list1)
	S2 = set(list2)
	return sorted(S1.symmetric_difference(S2))
	
def WordCount(WordList): 
	WordDict = dict()
	for word in WordList: 
		if word.lower() in WordDict:
			WordDict[word.lower()] += 1
		else:
			WordDict[word.lower()] = 1
	return sorted(WordDict.items())
	
def FirstFive(WordList): 
	return WordList[:5] 
	
def CheckKey(ADict, AString):
        try:
                print ADict[AString]
        except KeyError:
                print "Key not found."
                
