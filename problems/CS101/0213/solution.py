import Function
import pickle

fname = raw_input()
ADict = pickle.load(open(fname, 'rb'))
try:
    print Function.CheckKey(ADict, 'a')
except KeyError:
    print "Key not found."
