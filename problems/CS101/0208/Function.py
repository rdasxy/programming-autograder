def AddUp(A, B):
	return A+B 

def EitherOr(list1, list2): 
	S1 = set(list1)
	S2 = set(list2)
	return sorted(S1.symmetric_difference(S2))
	
	
	