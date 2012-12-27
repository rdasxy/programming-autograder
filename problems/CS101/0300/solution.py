#import student's function
import four
import pickle

fname = raw_input("file:")

f = open(fname, "rU")

d = pickle.load(f)

newDict = four.switchDict(d)

print newDict
