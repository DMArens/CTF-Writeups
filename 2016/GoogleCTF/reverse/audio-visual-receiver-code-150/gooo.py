#!/usr/bin/env python
def up(s):
    st = s & 0xFF
    s = (s + s) & 0xFF
    s = (s + st) & 0xFF
    return s

def down(s):
    s = (s >> 1) & 0xFF
    st = s
    s = (s << 3) & 0xFF
    s = (s - st) & 0xFF
    return s

def left(s):
    s = (s + s) & 0xFF
    return s

def right(s):
    st = (s << 5) & 0xFF
    s = (s >> 3) & 0xFF
    s = (st | s) & 0xFF
    return s

def a(s):
    st = (s >> 4) & 0xFF
    s = (s << 4) & 0xFF
    s = (s | st) & 0xFF
    if s == 0xef6825:
        print('you win! {}'.format(s))
    else:
        print('reset')
    return s

def b(s):
    s = (~s) & 0xFF
    return s

dirs = [up, down, left, right, a, b]
dirn = ['up', 'down', 'left', 'right', 'a', 'b']
FLAG = [0x46, 0x5b, 0x6b, 0xe1, 0x6f, 0x5e, 0xa3, 0xd3, 0xa2, 0x1c, 0x82, 0xed, 0x62, 0x24, 0x67, 0x71, 0xdd, 0x6d, 0xf3, 0x20, 0x83, 0x8d, 0xca, 0x3e, 0x33, 0xc8, 0x75, 0x5a, 0x00, 0x05 ]
flag = 'CTF{the_3rd_time_is_the_charm}'

def enum(s, deco):
    current = FLAG[len(deco)]
    for f,n in zip(dirs, dirn):
        new = f(s) ^ current
        print(n + ':\t' + deco + chr(new) + ': ' + str(f(s)))

def solve():
    s = 5
    flag = 'C'
    choices = []
    while True:
        print('s: {}\nflag: {}'.format(s,flag))
        print('possibles:')
        enum(s, flag)
        choice = raw_input('> ')
        while (choice not in dirn + ['q']):
            choice = raw_input('again> ')
        choices.append(choice)
        f = None
        if choice == 'up':
            f = up
        elif choice == 'down':
            f = down
        elif choice == 'left':
            f = left
        elif choice == 'right':
            f = right
        elif choice == 'a':
            f = a
        elif choice == 'b':
            f = b
        else:
            print(s)
            print(flag)
            print(choices)
        s = f(s)
        flag += chr(s ^ FLAG[len(flag)])

solve()
