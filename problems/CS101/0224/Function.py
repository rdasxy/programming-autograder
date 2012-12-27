def AddCommas(NumStr): 
    if len(NumStr) <= 3: 
        return NumStr
    else:
        Left = AddCommas(NumStr[:-3])
        return Left + ',' + NumStr[-3:] 
    