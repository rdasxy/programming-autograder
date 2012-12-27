import pickle
import Function
f = open(raw_input(), 'rb')
X = pickle.load(f)
f.close() 
print Function.FirstFive(X)
