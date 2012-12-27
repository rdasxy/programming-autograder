def Bad(thingy): 
    if not isinstance(thingy, str): 
        raise TypeError 
    elif len(thingy) > 10: 
        raise TypeError 
    elif len(thingy) > 5: 
        raise ValueError 
    elif 'z' in thingy: 
        raise IOError 
    elif 'q' in thingy: 
        raise KeyError 
    else:
        return 'OK' 
    
    