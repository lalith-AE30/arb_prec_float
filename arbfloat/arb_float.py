"""Module containing the ArbFloat class"""
import copy
import numpy as np


class ArbFloat:
    """Defines the class for arbitrary precision floats"""
    def __init__(self, x=0, prec=10):
        self.prec = prec

        if isinstance(x, ArbFloat):
            self.digits = copy.copy(x.digits)
            while len(self.digits) > self.prec:
                self.digits.pop()
            while len(self.digits) < self.prec:
                self.digits.append(0)
            if len(self.digits) != self.prec:
                raise Exception("Length of digits not equal to precision")
            self.exp = x.exp
            self.sign = x.sign
            return

        self.sign = False
        if x < 0:
            self.sign = True
            x *= -1
        if x == 0:
            self.exp = 0
            self.digits = [0 for _ in range(self.prec)]
            return

        i = str(x)
        r = i.find('.')
        if r == -1:
            i = i+'.'
        r = i.find('.')
        j = i[:r]
        if len(j.replace('0', '')) == 0:
            i = i[r+1:]
            self.exp = len(i.lstrip('0'))-len(i)-1
        else:
            self.exp = len(j)-1
        self.digits = [0 for _ in range(self.prec)]
        for q in range(prec):
            i = i.strip('0').replace('.', '')
            if not q < len(i):
                break
            self.digits[q] = int(i[q])

    def __str__(self):
        out = '-' if self.sign else ''
        for i, d in enumerate(self.digits):
            out += str(d)
            if i == 0:
                out += '.'
        return out+f' x 10^{self.exp}'

    def __mul__(self, other):
        if not isinstance(other, ArbFloat):
            return self*ArbFloat(other)
        if other.is_zero() or self.is_zero():
            return ArbFloat(0, self.prec)
        n1 = np.array(self.digits[::-1])
        n2 = np.array(other.digits[::-1])
        out = ArbFloat(0, self.prec+other.prec)
        product = np.array(out.digits[::-1])
        for b_i in range(other.prec):
            carry = 0
            for a_i in range(self.prec):
                product[a_i+b_i] += carry + n1[a_i] * n2[b_i]
                carry = int(product[a_i+b_i]/10)
                product[a_i+b_i] = product[a_i+b_i] % 10
            product[b_i + self.prec] = carry
            if (other.prec-b_i == 1 and carry != 0):
                out.exp = 1
        out.digits = list(product[::-1])
        while out.digits[0] == 0:
            out.digits.pop(0)
        while out.digits[-1] == 0:
            out.digits.pop()

        out.exp += self.exp+other.exp

        out.sign = self.sign ^ other.sign

        out.prec = len(out.digits)
        return out

    def __rmul__(self, other):
        return other*self

    def __add__(self, other):
        if not isinstance(other, ArbFloat):
            return self+ArbFloat(other)

        if self.sign and other.sign:
            self.sign = False
            other.sign = False
            out = self+other
            out.sign = True
            self.sign = True
            other.sign = True
            return out
        
        if self.sign:
            self.sign = False
            out = other-self
            self.sign = True
            return out
        
        if other.sign:
            other.sign = False
            out = self-other
            other.sign = True
            return out
        
        a = self.digits[:]
        b = other.digits[:self.prec]
        
        for _ in range(max(0, self.prec-other.prec)):
            b.append(0)
        add_a = other.exp > self.exp
        if add_a == True:
            for _ in range(other.exp-self.exp):
                b.append(0)
        else:
            for _ in range(self.exp-other.exp):
                a.append(0)
        a = a[::-1]
        b = b[::-1]
        if add_a:
            for _ in range(other.exp-self.exp):
                a.append(0)
        else:
            for _ in range(self.exp-other.exp):
                b.append(0)

        a = np.array(a)
        b = np.array(b)
        out = ArbFloat(0, self.prec+1)
        summand = []
        carry = 0
        for i, _ in enumerate(a):
            s = a[i]+b[i]+carry
            summand.append(s % 10)
            carry = int(s/10)
        if carry != 0:
            out.exp = 1
            summand.append(carry)

        out.digits = summand[::-1]
        out.exp += self.exp if self.exp > other.exp else other.exp
        return out

    def __radd__(self, other): return other+self

    def __sub__(self, other):
        if not isinstance(other, ArbFloat):
            return self-ArbFloat(other)

        if self == other:
            return ArbFloat(0, self.prec)
        
        if self < other:
            out = other-self
            out.sign = True
            return out
        
        if self.sign and not other.sign:
            self.sign = False
            out = self+other
            self.sign = True
            out.sign = True
            return out
        
        if other.sign and not self.sign:
            other.sign = False
            out = self + other
            other.sign = True
            return out
        
        if other.sign and self.sign:
            other.sign = False
            self.sign = False
            out = other-self
            other.sign = True
            self.sign = True
            return out

        a = self.digits[:]
        b = other.digits[:self.prec]
        for _ in range(max(0, self.prec-other.prec)):
            b.append(0)
        add_a = True if other.exp > self.exp else False
        if add_a:
            for _ in range(other.exp-self.exp):
                b.append(0)
        else:
            for _ in range(self.exp-other.exp):
                a.append(0)
        a = a[::-1]
        b = b[::-1]
        if add_a:
            for _ in range(other.exp-self.exp):
                a.append(0)
        else:
            for _ in range(self.exp-other.exp):
                b.append(0)
        a = np.array(a)
        b = np.array(b)
        
        diff = np.zeros(len(a),dtype=np.int8)
        for i, _ in enumerate(a):
            d = a[i]-b[i]
            if d < 0:
                a[i+1] -= 1
                d = a[i]+10-b[i]
            diff[i]=d

        out = ArbFloat(0, self.prec)
        out.digits = list(diff[::-1])
        while len(out.digits) > self.prec:
            out.digits.pop()
        while out.digits[0] == 0:
            out.digits.pop(0)
            out.exp -= 1
        while len(out.digits) < self.prec:
            out.digits.append(0)
        out.exp += self.exp if self.exp > other.exp else other.exp
        return out

    def __rsub__(self, other): return -(other-self)

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("Division by Zero")
        if not isinstance(other, ArbFloat):
            return self/ArbFloat(other)
        return self * other.raphson_inverse()

    def __rtruediv__(self, other): return ArbFloat(other)/self

    def __floordiv__(self, other): return ArbFloat(int(self/other))

    def __rfloordiv__(self, other): return ArbFloat(
        int(ArbFloat(other)/self))

    def __lt__(self, other):
        if not isinstance(other, ArbFloat):
            return self < ArbFloat(other)

        if self.is_zero():
            return not other.sign
        if other.is_zero():
            return self.sign
        flip = False
        if self.sign and not other.sign:
            return True
        if other.sign and not self.sign:
            return False
        if self.sign and other.sign:
            flip = True
        if self.exp < other.exp:
            return True ^ flip
        if self.exp > other.exp:
            return False ^ flip

        a = self.digits[:]
        b = other.digits[:self.prec]
        for _ in range(max(0, self.prec-other.prec)):
            b.append(0)
        b = np.array(b)
        for i, _ in enumerate(a):
            if a[i] < b[i]:
                return True ^ flip
            if a[i] > b[i]:
                return False ^ flip
        return False ^ flip

    def __eq__(self, other):
        if not isinstance(other, ArbFloat):
            return self == ArbFloat(other)

        if self.is_zero() and other.is_zero():
            return True
        if self.sign ^ other.sign:
            return False
        if self.exp != other.exp:
            return False
        a = np.array(self.digits[:])
        b = other.digits[:self.prec]
        for _ in range(max(0, self.prec-other.prec)):
            b.append(0)
        b = np.array(b)
        for i, _ in enumerate(a):
            if a[i] != b[i]:
                return False
        return True

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        out = ArbFloat(self, self.prec)
        out.sign = not out.sign
        return out

    def __pos__(self): return self

    def __abs__(self):
        out = ArbFloat(self, self.prec)
        out.sign = False
        return out

    def __float__(self):
        sstring = self.__str__()
        sig_digits = float(sstring.split('x')[0])
        return 10**self.exp*sig_digits

    def __int__(self):
        return int(self.__float__())

    def raphson_inverse(self,steps=-1):
        """Returns the raphson inverse of number. (1/x)"""
        if self == 0:
            raise ZeroDivisionError("Division by Zero")
        x = ArbFloat(1, self.prec)
        x.exp = -(self.exp+1)
        a2 = ArbFloat(2)
        if steps!=-1:
            for _ in range(steps):
                x = ArbFloat(x*(a2-self*x), self.prec)
            return x
        while True:
            px = x
            x = ArbFloat(x*(a2-self*x), self.prec)
            if px == x:
                return x

    def is_zero(self):
        """tests if given number is zero"""
        digs = np.array(self.digits)
        for d in digs:
            if d != 0:
                return False
        return True


def arb_pow(x: ArbFloat, n: int, steps=-1) -> ArbFloat:
    """
    Returns x raised to the power of n.

    Parameters
    ----------
    x : ArbFloat
        Base
    n : int
        Power
    steps : int, optional
        The number of steps to be taken in Raphson-inverse, leave blank for
        full input precision.

    Returns
    -------
    ArbFloat

    """
    if n < 0:
        return arb_pow(x.raphson_inverse(steps=steps), -n)
    if n == 0:
        return ArbFloat(1)
    if n % 2 == 0:
        return arb_pow(x*x, n/2)
    return x * arb_pow(x*x, (n-1)/2)
