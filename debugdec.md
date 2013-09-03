# debugdec

Debugdec contains functions and decorators useful for debugging.

## enabling debugdec

When you are running your code in production, you probably don't 
want it printing out reams of debugging statements. Nor do you want it 
slowed down by type checking. Do debugdec only does anything if you
set a flag in your code telling it to do so:

```python
import debugdec
from debugdec import printargs, typ, prvars

debugdec.debugging = True
```

## @printargs

The printargs decorator prints the arguments it was called with, and the
return value. Example:

```python
@printargs
def fact(n):
    if n<2: return 1
    return n*fact(n-1)
```

When `fact(4)` is run from the Python REPL, you get:

```python
>>> fact(4)
fact(4)
| fact(3)
| | fact(2)
| | | fact(1)
| | | fact(1) => 1
| | fact(2) => 2
| fact(3) => 6
fact(4) => 24
24
```

### limitations of @printargs

Printargs doesn't do anything about exceptions. It could be enhanced so 
that if an exception is raised by the decorated function, printargs
catches it, says so in the transcript and re-raises it.

## @typ

The typ decorator does type checking on a function's 
parameters, and optionally on its return value as well. Example:

```python
@typ(int, ret=int)
def square(x):
    return x*x
```

This checks that `square()` receives an `int` and returns an `int`. If
not, a `TypeError` is thrown.

You can also allow a parameter or return valure to be more than one type,
for example:

```python
@typ((int,float), ret=(int,float))
def square(x):
    return x*x
```

`@typ` works correctly if decorating a method, for example this works
as expected:

```python
class Foo:
    def __init__(self):
        self.v = 0
        
    @typ(int, ret=int)    
    def add(self, n):
        self.v += n
        return self.v
```

How does `@typ` know that a function is a method? It checks whether the 
name of the first parameter is `self`. So if you use the normal Python 
naming convention, it will work.

### limitations of @typ

1. It required that functions have a fixed number of arguments. A 
variable number of arguments is not supported, nor are keyword arguments.

2. It cannot compose types. By this I mean that you can say that an
argument is a `dict` but you can't say that it is a `dict` whose keys
are all strings and whose values are all ints.

## prvars()

The `prvars()` function prints the local variables of the function it is
called from. If it is called with no argument, it prints all local variables:

```python
>>> from debugdec import *
>>> def foo():
...     x = 1
...     y = 2
...     prvars()
...     return 3
... 
>>> 
>>> foo()
foo():4 x=1 y=2
3
```

As you can see from the above, `prvars()` prints the name of the function 
and the line number withing the file where `prvars()` was called. This is
so that you can have multiple `prvars()` statements within the same function, 
and your output will make it clear which one is being executed.

You can also tell `prvars()` which variables to print. To do this, you
put them in a string, separated by spaces, so `prvars("x y z")`
will print the `x`, `y` and `z` variables.


