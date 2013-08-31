# debugdec.py = decorators useful for debugging

import math

#---------------------------------------------------------------------

GL_PRINTARGS_DEPTH = 0
GL_PRINTARGS_INDENT = "| "

def printargs(fn):
    def wrapper(*args, **kwargs):
        global GL_PRINTARGS_DEPTH
        argStr = ", ".join([repr(a) for a in args])
        kwargStr = ", ".join(["%s=%r"%(k,v) for v,k in enumerate(kwargs)])
        comma = ""
        if argStr and kwargStr: comma = ", "
        akStr = argStr + comma + kwargStr
        print '%s%s(%s)' % (GL_PRINTARGS_INDENT * GL_PRINTARGS_DEPTH,
           fn.__name__, akStr)
        GL_PRINTARGS_DEPTH += 1
        retVal = fn(*args, **kwargs)
        GL_PRINTARGS_DEPTH -= 1
        if retVal != None:
            print "%s%s(%s) => %r" % (GL_PRINTARGS_INDENT * GL_PRINTARGS_DEPTH,
               fn.__name__, akStr,
               retVal)
        return retVal
    return wrapper

#---------------------------------------------------------------------
"""
Type checking works like this:

@typ(int, ret=int)
def foo(x)
    return x*x

"""

def typeName(ty):
    """ Reyturn the name of a type, e.g.:
    typeName(int) => 'int'
    typeName(Foo) => 'foo'
    typeName((int,str)) => 'int or str'
    @param ty [type|tuple of type]
    @return [str]
    """
    if isinstance(ty, tuple):
        return " or ".join(t.__name__ for t in ty)
    else:
        return ty.__name__

class typ:
    """ decorator to check a functions argument type """

    def __init__(self, *argTypes, **retType):
        self.argTypes = argTypes
        if retType.has_key('ret'):
            self.ret = retType['ret']
        else:    
            self.ret = None
        
        
    def __call__(self, fn):
        """ return a new function that when called, checks
        the arguments before calling the original function. 
        """
        def wrapper(*args):
            # check number of args
            if len(args)<len(self.argTypes):
                msg = ("%s() called with too few args (%d), should be >=%d"
                    % (fn.__name__, len(args), len(self.argTypes)))
                raise TypeError(msg)
            # check args
            for ix, arg in enumerate(args):
                sbType = self.argTypes[ix] # what the type should be
                if sbType!=None and not isinstance(arg, sbType):
                    msg = ("calling %s(), arg[%d]==%r had type of %s,"
                        " should be %s") % (fn.__name__, 
                        ix, arg,
                        type(arg).__name__,
                        typeName(sbType))
                    raise TypeError(msg)
            retval = fn(*args)
            # check return type
            if self.ret!=None and not isinstance(retval, self.ret):
                msg = ("%s() returns type of %s,"
                        " should be %s") % (fn.__name__, 
                        type(retval).__name__,
                        typeName(self.ret))
                raise TypeError(msg)
            return retval
        return wrapper  

#---------------------------------------------------------------------

@typ((int,float), ret=(int,float))
def square(x): 
    return x*x

print square(30)   
print square(34)    
#print square('x')    
    
#---------------------------------------------------------------------

#test:

@printargs
def baz(x, y):
    return x*x + y*y

@printargs
def bar(a):
    #print "in bar"
    return baz(a, 5)

@printargs
def foo(a, b, c):
    return a + b*bar(c)

foo(10, 20, 30)

foo(10, 20, c=4)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(%r,%r)" % (self.x, self.y)

    #@printargs
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)


p = Point(4,5)
print p.length()

@printargs
def xyz(): pass

xyz()

#---------------------------------------------------------------------

# print values

def _prVarsSelf(cLocals, vn):
    selfOb = cLocals['self']
    value = selfOb.__dict__[vn[5:]]
    r = " %s=%r" % (vn, value)
    return r

def prvars(varNames =None):
    import inspect
    if isinstance(varNames, str):
       vnList = varNames.split()   
    caller = inspect.stack()[1]
    cLocals = caller[0].f_locals # local variables of caller
    #print cLocals
    fileLine = caller[2]
    functionName = caller[3]
    filename = caller[0].f_code.co_filename
    output = "%s():%d" % (functionName, fileLine)
    outputForSelf = " "*len(output)
    printAllSelf = False
    if varNames==None:
        for vn in sorted(cLocals.keys()):
            output += " %s=%r" %(vn, cLocals[vn])
        if cLocals.has_key('self'): printAllSelf = True
    else:    
        for vn in vnList:
            if vn.startswith("self."):
               output += _prVarsSelf(cLocals, vn)     
            elif cLocals.has_key(vn):
               output += " %s=%r" %(vn, cLocals[vn]) 
               if vn=='self': printAllSelf = True
    if printAllSelf:
        selfOb = cLocals['self']
        for insVar in sorted(selfOb.__dict__.keys()):
           val = selfOb.__dict__[insVar]
           output += "\n" + outputForSelf + " self.%s=%r"%(insVar,val)
    print output        
    

def afun(zzz):    
    x = 45
    y = "hello"
    prvars("x y")
    d = (1,2,3)
    prvars()
    
afun(345)

class MyClass:
    def __init__(self, x, y):
        self.x = x
        prvars()
        self.y = y
        prvars("x y self.x")
        prvars()

mc = MyClass(44,55)

class MyNewClass(object):
    def __init__(self, x, y):
        self.x = x
        prvars()
        self.y = y
        prvars("x y self.x")
        prvars()

mnc = MyNewClass(44,55)

#---------------------------------------------------------------------


#end
