import time
import random
from arb_float import ArbFloat

td1 = [random.random()+1*10**random.randint(-2, 2) for _ in range(32)]
td2 = [random.random()+1*10**random.randint(-2, 2) for _ in range(32)]

comp_err = 0
for t1 in td1:
    for t2 in td2:
        at1 = ArbFloat(t1)
        at2 = ArbFloat(t2)
        if (t1 == t2) ^ (at1 == at2):
            comp_err += 1
        if (t1 != t2) ^ (at1 != at2):
            comp_err += 1
        if (t1 <= t2) ^ (at1 <= at2):
            comp_err += 1
        if (t1 >= t2) ^ (at1 >= at2):
            comp_err += 1
        if (t1 < t2) ^ (at1 < at2):
            comp_err += 1
        if (t1 > t2) ^ (at1 > at2):
            comp_err += 1

a_err = 0
m_err = 0
s_err = 0
d_err = 0
for t1 in td1:
    for t2 in td2:
        at1 = ArbFloat(t1)
        at2 = ArbFloat(t2)
        a_err += abs((t1+t2)-float(at1+at2))
        m_err += abs((t1*t2)-float(at1*at2))
        d_err += abs((t1/t2)-float(at1/at2))
        s_err += abs((t1-t2)-float(at1-at2))

with open('ArbFloat_test.txt', 'w') as file:
    for t1 in td1:
        for t2 in td2:
            at1 = ArbFloat(t1)
            at2 = ArbFloat(t2)
            file.write(f"built-in: {t1},{t2}   | ArbFloat: {at1},{at2}\n")
            file.write(f"built-in sum: {t1+t2} | ArbFloat sum: {at1+at2}\n")
            file.write(f"built-in mul: {t1*t2} | ArbFloat mul: {at1*at2}\n")
            file.write(f"built-in sub: {t1-t2} | ArbFloat sub: {at1-at2}\n")
            file.write(f"built-in div: {t1/t2} | ArbFloat div: {at1/at2}\n\n")
        file.write(
            '-----------------------------------------------------------------------\n\n')
    file.write(
        f"addition error: {a_err}, multiplication error: {m_err}, subtraction error: {s_err}, division error: {d_err}, comparison fails: {comp_err}")


builtin = 0
arbfloat = 0
for t1 in td1:
    for t2 in td2:
        at1 = ArbFloat(t1)
        at2 = ArbFloat(t2)
        a1 = time.perf_counter_ns()
        at1+at2
        at1*at2
        at1-at2
        at1/at2
        a2 = time.perf_counter_ns()
        arbfloat += a2-a1
        b1 = time.perf_counter_ns()
        t1+t2
        t1*t2
        t1-t2
        t1/t2
        b2 = time.perf_counter_ns()
        builtin += b2-b1

print(f"built-in time:{builtin}, ArbFloat time:{arbfloat}")
