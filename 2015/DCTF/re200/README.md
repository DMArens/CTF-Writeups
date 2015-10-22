# Reverse 200

```
./r200
Enter the password: password!
Incorrect password!
```
Just like re100, we need to make the return value of ptrace 0
```
   0x00400878:	call   0x400600 <ptrace@plt>
   0x0040087d:	test   rax,rax
   0x00400880:	jns    0x4007e6
   0x00400882:	jmp    0x4007e4
b *0x40087d
commands
  set $rax=0
  continue
  end
```

the first thing in main is a loop that calls malloc 10 times:
```
.--> 0x004008ad  mov edi, 0x10
||   0x004008b2  call sym.imp.malloc
||   0x004008b7  mov qword [rbp-malloced], rax 
||
||   0x004008bb  mov rax, qword [rbp-malloced]
||   0x004008bf  mov edx, dword [rbp-count]
||   0x004008c2  mov dword [rax], edx 
||
||   0x004008c4  mov rax, qword [rbp-malloced]
||   0x004008c8  mov eax, dword [rax]
||   0x004008ca  add eax, 0x6d
||   0x004008cd  mov edx, eax 
||   0x004008cf  mov rax, qword [rbp-malloced]
||   0x004008d3  mov byte [rax + 4], dl
||
||   0x004008d6  mov rdx, qword [rip + 0x2007a3] ; [0x601080:8]=0x6e756275322d342e
||   0x004008dd  mov rax, qword [rbp-malloced]
||   0x004008e1  mov qword [rax + 8], rdx 
||
||   0x004008e5  mov rax, qword [rbp-malloced]
||   0x004008e9  mov qword [rip + 0x200790], rax ; [0x601080:8]=0x6e756275322d342e
||
||   0x004008f0  add dword [rbp-count], 1
|`-> 0x004008f4  cmp dword [rbp-count], 0xa
`==< 0x004008f8  jle 0x4008ad 
```
I split the code into 6 pieces:
1. malloc 16 bytes, store the pointer in rbp-malloced
2. move the count into the first dword
3. move the count + 0x6d into the following byte
4. move a qword from a variable into the end of malloced
5. store the address of malloced into that variable
6. increment, check if 10, continue

It's creating a linked list, and each element contains the index and the index + 0x6d

then it asks for 7 characters of input:
```
0x00400914   mov esi, 7
0x00400919   mov rdi, rax
0x0040091c   call sym.imp.fgets 
```

then we call 0x40074d
... I'll finish this soon
