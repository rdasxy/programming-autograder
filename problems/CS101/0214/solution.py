import Function
import pickle

fname = raw_input()
ADict = pickle.load(open(fname, 'rb'))
try:
    print Function.CheckKey(ADict, 'a')
except ValueError:
    print "Key not found."
