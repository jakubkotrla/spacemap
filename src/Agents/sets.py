# -*- coding: UTF-8 -*-

def SetUnion(a,b):
    return a+filter(lambda x:x not in a,b)

def SetIntersection(a,b):
    return filter(lambda x:x in a,b)

def SetDifference(a,b):
    return filter(lambda x:x not in b,a)
    
def SetDistinct(a,b):
    return filter(lambda x:x not in b,a)+filter(lambda x:x not in a,b)
    
def SetFirstDifference(a,b):
    difference = SetDifference(a,b)
    if len(difference) == 0:
        return None
    return difference[0]
