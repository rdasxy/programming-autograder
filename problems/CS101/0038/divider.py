# Create a class called Divider.  It should have one method, Divider.divide, that takes two 
# integers x and y as parameters.  If y isn't 0, it should return the quotient x / y.  If 
# y is 0, it should raise a ValueError.

class Divider(object):
    def divide(self, x, y):
        try:
            return x / y
        except ZeroDivisionError:
            raise ValueError
            