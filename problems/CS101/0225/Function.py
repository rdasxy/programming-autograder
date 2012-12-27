def AddCommas(NumStr, depth=5):
    if depth == 0: 
        return "Error"
    elif len(NumStr) <= 3: 
        return NumStr
    else:
        Left = AddCommas(NumStr[:-3], depth-1)
        return Left + ',' + NumStr[-3:] 
    