import pickle
import Function
f = open(raw_input())
X = pickle.load(f)
Y = pickle.load(f)
f.close() 
print Function.EitherOr(X, Y)
