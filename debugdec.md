# debugdec

## @printargs

The printargs decorator prints the arguments it was called with, and the
return value. Example:

```
@printargs
def fact(n):
    if n<2: return 1
    return n*fact(n-1)
```

When `fact(4)` is run from the Python REPL, you get:

```
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

## @typ

The typ decorator does type checking on a function's 
parameters, and optionally on its return value as well. Example:

```
@typ(int, ret=int)
def square(x):
    return x*x
```

This checks that square() receives an `int` and returns an `int`. If
not, a `TypeError` is thrown.




