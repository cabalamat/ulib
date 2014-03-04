# test_debugdec.py = testing debugdec

import lintest

import debugdec
from debugdec import printargs, typ, prvars

debugdec.debugging = True

#---------------------------------------------------------------------
# test printargs decorator

@printargs
def fact(n):
    if n<2: return 1
    return n*fact(n-1)
 
    
class T_printargs(lintest.TestCase):
    
    def test_1(self):
        r = fact(5)
        self.assertSame(r, 120, "fact(5) is 120")
        
    
#---------------------------------------------------------------------
# test typ() decorator

@typ(int, ret=int)
def square(x): 
    return x*x
    
@typ((int,float), ret=(int,float))
def square2(x): 
    return x*x

# square3() checks that typ isn't used when debugging is switched off    
debugdec.debugging = False    
@typ(int, ret=int)
def square3(x): 
    return x*x
debugdec.debugging = True   
 
class Foo:
    def __init__(self):
        self.v = 0
        
    @typ(int, ret=int)    
    def add(self, n):
        self.v += n
        return self.v
        
class xTypeError: pass 
 
class T_typ(lintest.TestCase):
    def test_int(self):
        r = square(4)
        self.assertSame(r, 16)
        try:
            r = square(4.3)
            self.failed("typ() should raise TypeError exception")
        except TypeError:
            self.passed("typ() correctly raises TypeError")
                       
    def test_intfloat(self):
        r = square2(4)
        self.assertSame(r, 16)
        
        r = square2(1.5)
        self.assertSame(r, 2.25)
            
    def test_switchedOff(self):
        """ check that typ() is switched off when the debugging
        flag is false. 
        """
        global debugdec
        print debugdec.debugging
        r = square3(4)
        self.assertSame(r, 16)
        r = square3(1.5)
        self.assertSame(r, 2.25, "doesn't check that argument is an integer")
        
    def test_method(self):
        """ test typ() on as method """
        f = Foo()
        r = f.add(1)
        self.assertSame(r, 1)
        r = f.add(4)
        self.assertSame(r, 5)
        try:
            r = f.add(7.7)
            self.failed("typ() should raise TypeError exception")
        except TypeError:
            self.passed("typ() correctly raises TypeError")
        
#---------------------------------------------------------------------
# test prvars function

def afun(zzz):    
    x = 45
    y = "hello"
    prvars("x y")
    d = (1,2,3)
    prvars()
    
class MyClass:
    def __init__(self, x, y):
        self.x = x
        prvars()
        self.y = y
        prvars("x y self.x")
        prvars()

class MyNewClass(object):
    def __init__(self, x, y):
        self.x = x
        prvars()
        self.y = y
        prvars("x y self.x")
        prvars()

class T_prvars(lintest.TestCase):
    def test_afun(self):
        afun(345)
        
    def test_MyClass(self):
        mc = MyClass(44, 55)
        
    def test_MyNewClass(self):
        mnc = MyNewClass(44, 55)

#---------------------------------------------------------------------

def getFooBar():
    cl = debugdec.getCallerLocals()
    return cl['foo'], cl['bar']
    
def getFoo():
    f = debugdec.getCallerLocal('foo')
    return f

class T_getCallerLocals(lintest.TestCase):
    
    def test_getCallerLocals(self):
        foo = 345
        bar = "I like bars"
        f, b = getFooBar()
        self.assertSame(f, foo, "f has the same value as foo")
        self.assertSame(b, bar, "b has the same value as bar")
        
    def test_getCallerLocal(self):
        foo = 6789
        f = getFoo()
        self.assertSame(f, foo, "f has the same value as foo")
        
#---------------------------------------------------------------------

group = lintest.TestGroup()
group.add(T_printargs)
group.add(T_typ)
group.add(T_prvars)
group.add(T_getCallerLocals)

if __name__=="__main__": group.run()

#end