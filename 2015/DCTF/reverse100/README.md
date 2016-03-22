# Reverse 100

```
./r100
Enter the password: password
Incorrect password!
```
We just need to find the password for this one!

My first step was to break at main and run the program, but there's some anti-debugging and that just sticks us in
an infinite loop. Here's why:
```
   0x004007da:	call   0x400600 <ptrace@plt>
   0x004007df:	test   rax,rax
   0x004007e2:	jns    0x4007e6
   0x004007e4:	jmp    0x4007e4
```

if ptrace returns negative (we are debugging) it will jump to 0x4007e4 forever. So let's pretend it returns zero
```
b *0x4007df
commands
  set $rax=0
  continue
  end
```
now we can continue with gdb. Here is a section of code from main. We want the function at
0x4006fd to return 0 and it will print out 'Nice'
```
  0x0040083b  call 0x4006fd
  0x00400840  test eax, eax
  0x00400842  jne 0x400855
  0x00400844  mov edi, str.Nice
  0x00400849  call sym.imp.puts
```

here is the dissassembly of the important bits of that function from Radare2
```
|           0x0040070c  mov qword [rbp-local_4], str.Dufhbmf ; "Dufhbmf" @ 0x400914
|           0x00400714  mov qword [rbp - 0x18], str.pG_imos ;  "pG`imos" @ 0x40091c
|           0x0040071c  mov qword [rbp - 0x10], str.ewUglpt ;  "ewUglpt" @ 0x400924
|           0x00400724  mov dword [rbp-local_4_4], 0
|       ,=< 0x0040072b  jmp 0x40079b                 
|       |   0x0040072d  mov ecx, dword [rbp-local_4_4]
|       |   0x00400730  mov edx, 0x55555556
|       |   0x00400735  mov eax, ecx
|       |   0x00400737  imul edx
|       |   0x00400739  mov eax, ecx
|       |   0x0040073b  sar eax, 0x1f
|       |   0x0040073e  sub edx, eax
|       |   0x00400740  mov eax, edx
|       |   0x00400742  add eax, eax
|       |   0x00400744  add eax, edx
|       |   0x00400746  sub ecx, eax
|       |   0x00400748  mov edx, ecx
|       |   0x0040074a  movsxd rax, edx
|       |   0x0040074d  mov rsi, qword [rbp + rax*8 - 0x20]
|       |   0x00400752  mov ecx, dword [rbp-local_4_4]
|       |   0x00400755  mov edx, 0x55555556
|       |   0x0040075a  mov eax, ecx
|       |   0x0040075c  imul edx
|       |   0x0040075e  mov eax, ecx
|       |   0x00400760  sar eax, 0x1f
|       |   0x00400763  sub edx, eax
|       |   0x00400765  mov eax, edx
|       |   0x00400767  add eax, eax
|       |   0x00400769  cdqe
|       |   0x0040076b  add rax, rsi
|       |   0x0040076e  movzx eax, byte [rax]
|       |   0x00400771  movsx edx, al
|       |   0x00400774  mov eax, dword [rbp-local_4_4]
|       |   0x00400777  movsxd rcx, eax
|       |   0x0040077a  mov rax, qword [rbp-local_7]
|       |   0x0040077e  add rax, rcx
|       |   0x00400781  movzx eax, byte [rax]
|       |   0x00400784  movsx eax, al
|       |   0x00400787  sub edx, eax
|       |   0x00400789  mov eax, edx
|       |   0x0040078b  cmp eax, 1
|      ,==< 0x0040078e  je 0x400797                  
|      ||   0x00400790  mov eax, 1
|     ,===< 0x00400795  jmp 0x4007a6                 
|     |`--> 0x00400797  add dword [rbp-local_4_4], 1
|     | `-> 0x0040079b  cmp dword [rbp-local_4_4], 0xb 12
|     |     0x0040079f  jle 0x40072d - jumps to the loop
|     |     0x004007a1  mov eax, 0
|     `---> 0x004007a6  pop rbp
\           0x004007a7  ret
```

This loops through our input, does a subtraction and checks if it's equal to one. (lines 0x00400787 - 0x0040078e)
We want it to equal 1 each time through the loop. We can easily set a breakpoint here and force the
numbers to work, and we'll end with the complete string.

Stepping through GDB you can see it pulled the first char from the string 'Dufhbmf' which is a local
variable and subracts our char. So the first character is 'C'. This can be repeated for each character of
the flag, but it's much easier than that.

We can see there are three strings defined at the start of the function "Dufhbmf" "pG`imos" "ewUglpt"
The function just loops through each string, and pulls every other character to compare with ours.
```
D u f h b m f
p G ` i m o s
e w U g l p t

the order is:     D p e f ` U b m l f s t
and subtract one: C o d e _ T a l k e r s
```

and theres the flag, Code_Talkers
