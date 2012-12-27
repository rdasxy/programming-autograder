#Take an integer from the console, and calculate the cubic root.  this program
#uses the student provided file solution.py with the funcition cube_root that
#takes an integer argument and returns the integer, if the cubic root does not
#exist, the function should return -1


import solution

def power(a, b, origb, count):

    if b > a:
        return count
    elif (float(a)/float(b)) != a/b:
        return count 
    
    if a%b == 0:
        count +=1
    
    newb = b*origb
    return power(a, newb, origb, count)

def cube_root(num):
    
    count = 0

    while count <= int(num/3):
        if (count*count*count) == num:
            return count
        else:
            count+=1

    return -1


def main():
    count = 0
    for count in range(5):
        temp = int(raw_input())
    
        #result = solution.root(temp)
        print [temp, solution.cube_root(temp)]
        count+=1
    
main()
