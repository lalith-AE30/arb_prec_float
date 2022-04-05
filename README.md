
# Arbitrary Precsion Floating point number

Implements floating point numbers with the ability to specify the amount of digits of
precision. It can be used to perform calculation when built-in python datatypes may
 lose precision in the calculation and may give a "Result too large" error.

 Because the type is implemented entirely in Python using lists, its
 magnitudes slower than built-in types. The speed can be improved if they are
 re-implemented using bytes instead of lists.
## Usage

Install dependencies by running
```pip install -r requirements.txt```
from the root directory.

To import the class in another file, add ```arb_float.py``` into the same directory
as the file, then import the class in python with 
```
from arb_float import ArbFloat
```
Create an instance of the class by passing any number. For example:
```
x = ArbFloat(1.234)
y = ArbFloat(34.463)
```
All basic arithemetic operations are currently implemented(+,-,/,*) and can be called
just like any other data type. For example:
```
x = ArbFloat(1.234)
y = ArbFloat(34.463)
z = x+y*12
```
Note: Operations between the float and any other type implicitly converts the other type into
 ArbFloat, but should generally be avoided.

The type can be converted to float, int and str. The string representation gives the
number in scientific notation with full precision, so, if an instance has a precision
of 10,000 then the ```str()``` method returns all 10,000 digits.

## Documentation

#### Addtion
Addition between any two instances can be done in the same way as built-in types
```
a = ArbFloat(12.234)
b = ArbFloat(12387.234,prec=32)
print(a+b)
```
Addition between any two instances of ArbFloat returns the result with the precision
of the instance with greater precision. In the above example, `b` has a higher 
precision of 32, hence a precision of 32 is in the output.

#### Subtraction
Subtraction between any two instances can be done in the same way as built-in types
just like addition
```
a = ArbFloat(12.2370,prec=25)
b = ArbFloat(6.2134)
print(a-b)
```
Subtraction between any two instances of ArbFloat returns the result with the precision
of the instance with greater precision. In the above example, `a` has a higher precision of 25,
hence a precision of 25 is in the output.

#### Multiplication
Multiplication between any two instances can be done in the same way as built-in types
```
a = ArbFloat(2354.456)
b = ArbFloat(145.345)
print(a*b)
```
Multiplication between any two instances is different from addition and subtraction,
where the result has the minimum precision required for full precision in the output.
This is done as keeping the precision constant results in large loss of precision.
But additive precision results in slowdowns, hence the minimum precision which yields
full precision is taken.

#### Division
Division between any two instances can be done in the same way as built-in types
```
a = ArbFloat(2354.456)
b = ArbFloat(145.345)
print(a/b)
```
The precision of division is dependent on the precision of the denominator, this is
due to the fact that the division uses Newton-Raphson approximation till the inverse
stabilizes to the precision of the denominator.

### Comaparison
Comparison works as expected to normal types. such as:
```
a==b
a!=b
a<b
a>b
a>=b
a<=b
```

### Additional functions
#### ```raphson_inverse(steps=-1)```
A class method which returns the inverse (1/x) of the instance with the precision of
the instance. This method should be called when `1/x` is required but won't be 
further multplied by another number. If number of steps are specified, the algorithm
is only for specified instead of achieving input precision.

#### ```is_zero()```
Returns `True` is the instance is zero. Does not have any use other than for internal
methods.

#### ```arb_pow(x: ArbFloat, n: int, steps=-1) -> ArbFloat```
Returns `x` raised to the power of `n`. Steps specify the steps for the inverse if 
`n` is negative.
## References

Multiplication algorithm: https://en.wikipedia.org/wiki/Multiplication_algorithm#Long_multiplication

Newton-Raphson method: https://en.wikipedia.org/wiki/Division_algorithm#Newton%E2%80%93Raphson_division

Integer exponentiation: https://en.wikipedia.org/wiki/Exponentiation_by_squaring#Basic_method