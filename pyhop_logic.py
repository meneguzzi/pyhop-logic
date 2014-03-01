"""
Logic-like helper methods for Pyhop 1.1.
Author: Felipe Meneguzzi <felipe.meneguzzi@pucrs.br>, March 1, 2014
This file should work correctly in both Python 2.7 and Python 3.2.
"""

import pyhop
from test.test_iterlen import len

"""
A function to add literals to a state.  
Literals are nested maps with a nesting depth equal to the number of arguments.
For example on(a,b) is represented in a state by a map on = {"a":{"b":True}}, and the call to 
addLiteral(state,'on','a','b') is equivalent to executing state.on = {"a":{"b":True}}
Literals can be 'removed' simply by setting their Truth value as false by executing state.on[a][b]=False
"""
def addLiteral(state,functor,*pars):
    d = None
    if(not (functor in vars(state))):
        if(len(pars)==0):
            d = True
        else:
            d = dict()
        setattr(state, functor, d)
    else: 
        d = getattr(state, functor)
    if(len(pars) > 0):
        oldMap = d
        for p in pars[0:-1]:
            if(p in oldMap): 
                newMap = oldMap[p]
            else: 
                newMap = dict()
                oldMap[p]=newMap
            oldMap=newMap
        oldMap[pars[-1]] = True

"""
A function to test literals within a state, assuming the state data structure may not contain them
"""
def testLiteral(state,functor,*pars):
    d = None
    if(not (functor in vars(state))):
        return False
    else:
        d = getattr(state, functor)
    if(len(pars) > 0):
        mp = None
        if(pars[0] in d):
            mp = d[pars[0]]
            if(mp == True):
                return True    
        else: return False
        for p in pars[1:]:
            if(p in mp):
                mp = mp[p]
            if(mp == True) : return True
    else: return (d==True)
    return False

"""
A function that returns true if there exists any literal with the specified parameters in state.
Parameters are either None (in which case any parameter will do) or have a set value (in which case it is a constraint)
E.g.
existsLiteral(state,'commitment','C1',None,'buyer',None) will be true if there is any literal
commitment(C1,_,buyer,_) where _ represents a wildcard variable
"""
def existsLiteral(state, functor, *pars):
    for lit in each(state,functor,*pars):
        if(not(lit is False)):
            return True
    return False

"""
A generator function that yields (as tuples) all possible 'unifications' of variables 
for a literal within a state, given certain parameters
Parameters are either None (in which case any parameter will do) 
or have a set value (in which case it is a constraint)
E.g. If state is initialized as follows:
state.commitment = {"C1":{"C1":{"merchant":{"customer":True}}},
                    "C2":{"C2":{"customer":{"merchant":True}}},
                    "C5":{"C5":{"merchant":{"customer":True}}}
                   } 
Then the code below prints 'C1C5' 
for (x,y,z,w) in each(state,'commitment',None,None,'merchant',None):
    print(x)
"""
def each(state, functor, *pars):
    d = None
    if(not (functor in vars(state))):
        d = dict()
        setattr(state, functor, d)
    else: 
        d = getattr(state, functor)
    
    for p in eachPar(d,pars):
#         print(p)
        if(p is not False): yield p
"""
A helper function for 'each' to enumerate the possible parameters 
"""
def eachPar(mp,pars):
#     print(keys)
    if(len(pars) == 0):
        if(mp):
            yield ()
        else: yield False
    elif(pars[0] is None):
        for k in mp:
            newMp = mp[k]
            for t in eachPar(newMp, pars[1:]):
                if(t is not False): yield (k,)+t
        yield False
    else:
        k = pars[0]
        if(k in mp): 
            newMp = mp[k]
            for t in eachPar(newMp, pars[1:]):
                if(t is not False): yield (k,)+t
            yield False
        else: yield False