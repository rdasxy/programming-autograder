import Function
import pickle

fname = raw_input()
ADict = pickle.load(open(fname, 'rb'))
Function.CheckKey(ADict, 'a')

##f = open('data4.txt', 'wb')
##D = {'b':'banana', 'q':'quicksand', 'a':'this is the last input data.'}
##pickle.dump(D, f)
##f.close()
