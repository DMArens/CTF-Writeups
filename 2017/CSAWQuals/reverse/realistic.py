#!/usr/bin/env python
from pprint import pprint
from z3 import *
import struct

s = Solver()
ZERO = IntVal(0)

def z3_abs(x):
    return If(x >= 0, x, -x)

def psadbw(xmm1, xmm2):
    first  = Sum([z3_abs(b1 - b2) for b1,b2 in zip(xmm1[:8], xmm2[:8])])
    second = Sum([z3_abs(b1 - b2) for b1,b2 in zip(xmm1[8:], xmm2[8:])])
    return (first, second)

_results = [
    (0x02df, 0x028f),
    (0x0290, 0x025d),
    (0x0209, 0x0221),
    (0x027b, 0x0278),
    (0x01f9, 0x0233),
    (0x025e, 0x0291),
    (0x0229, 0x0255),
    (0x0211, 0x0270)
] 

_xmm5s = [
    [0xb8, 0x13, 0x00, 0xcd, 0x10, 0x0f, 0x20, 0xc0, 0x83, 0xe0, 0xfb, 0x83, 0xc8, 0x02, 0x0f, 0x22],
]

for x in _results[:-1]:
    _xmm5s.append(list(map(ord, struct.pack('<Q', x[0]) + struct.pack('<Q', x[1]))))

xmm5s   = [ [IntVal(x) for x in row] for row in _xmm5s ]
results = [ [IntVal(x) for x in row] for row in _results ]

f = [Int('flag{:02}'.format(i)) for i in range(16)]
for char in f:
    s.add(char > 30, char < 127)

for i in range(8):
    xmm5 = xmm5s[i]
    xmm2 = list(f)
    xmm2[i] = ZERO
    xmm2[i+8] = ZERO
    high,low = psadbw(xmm5, xmm2)
    s.add(high == results[i][0])
    s.add(low == results[i][1])

print(s.check())
m = s.model()

solution = ''
sats = []
for d in m.decls():
    if 'flag' in d.name():
        solution += chr(m[d].as_long())
        sats.append((int(d.name()[4:]), chr(m[d].as_long())))
sats = sorted(sats, key=lambda x: x[0])
sats = [s[1] for s in sats]
flag = ''.join(sats)

# unshuffle the flag
flag = flag[12:] + flag[8:12] + flag[:8]
print('flag{}'.format(flag))
