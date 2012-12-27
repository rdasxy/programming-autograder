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
        return ADict[AString]
    except KeyError:
        raise ValueError

def H(x):
  if x <= 0:
          return 0.0
  elif x <= 1:
          return 1.0
  else:
          return 1.25*H(x/2.0)
        
