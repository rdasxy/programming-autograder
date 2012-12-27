def AddUp(A, B):
	return A+B 

def CommonItems(list1, list2): 
	Intersect = list()
	for thing in list1:
		if thing in list2:
			Intersect.append(thing)
	return sorted(Intersect)
	
	