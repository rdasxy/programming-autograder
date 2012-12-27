# Takes a list of 3 integers and returns the greatest common divisor


def GCD3(List):
    a = int(List[0])
    b = int(List[1])
    c = int(List[2])

    return GCD(GCD(a,b), GCD(a,c))

def GCD(a ,b ):
    if a%b == 0:
        return b
    else:
        return GCD(b, (a%b))
    
def main():

    temp = raw_input("Please enter three integers: ")
    l = temp.split()
    
    result=GCD3(l)
    print result

main()
