# Reverse 200
```
./r200
Enter the password: password!
Incorrect password!
```
Just like re100, we need to make the return value of ptrace 0 to debug it
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

It's creating a linked list, and each element contains the index and the index + 0x6d. Thaese numbers are all in ascii range, m n o p q r s t u v. Then we input 7 characters, and call 0x40074d. This function loops through each character of input, and for each character through the linked list.

It loops through the linked list until it find the current character of our input, then records the index of the list node and stores it in a variable, continuing to the next character. If the character is not in the linked list it stores a 0 instead.
```
         ; load the front of the linked list and loop
     ,=< 0x004007ad  jmp 0x40080d                       
.------> 0x004007af  mov rax, qword [rip + 0x2008ca] ; [0x601080:8]
|    |   0x004007b6  mov qword [rbp-list_node], rax 
|    |   0x004007ba  mov dword [rbp-node_index], 0
|   ,==< 0x004007c1  jmp 0x4007f6
||  ||   ; compare the input character to the current node
|.-----> 0x004007c3  mov rax, qword [rbp-list_node]
||  ||   0x004007c7  movzx edx, byte [rax + 4]
||  ||   0x004007cb  mov eax, dword [rbp-index]
||  ||   0x004007ce  movsxd rcx, eax
||  ||   0x004007d1  mov rax, qword [rbp-input] 
||  ||   0x004007d5  add rax, rcx
||  ||   0x004007d8  movzx eax, byte [rax]
||  ||   0x004007db  cmp dl, al
|| ,===< 0x004007dd  jne 0x4007ea
|| |||   ; if the characters match, store the index in a local variable
|| |||   0x004007df  mov rax, qword [rbp-list_node]
|| |||   0x004007e3  mov eax, dword [rax]
|| |||   0x004007e5  mov dword [rbp-node_index], eax
||,====< 0x004007e8  jmp 0x4007fd
||||     ; otherwise, get the next node
|||`---> 0x004007ea  mov rax, qword [rbp-list_node]
||| ||   0x004007ee  mov rax, qword [rax + 8]
||| ||   0x004007f2  mov qword [rbp-list_node], rax
||| ||   ; check if we have reached the last node
||| `--> 0x004007f6  cmp qword [rbp-list_node], 0
|`=====< 0x004007fb  jne 0x4007c3
| |  |   ; if we're at the end, store the saved index in another variable
| `----> 0x004007fd  mov eax, dword [rbp-index]
|    |   0x00400800  cdqe
|    |   0x00400802  mov edx, dword [rbp-node_index]
|    |   0x00400805  mov dword [rbp + rax*4 - 0x40], edx
|    |   0x00400809  add dword [rbp-index], 1
|    |   ; check if we've gone through 6 characters
|    `-> 0x0040080d  cmp dword [rbp-index], 5
`======< 0x00400811  jle 0x4007af
```
Then it loops through the array of indices that was created above, and compares each one to an array stored at rbp-0x20.
```
       0x00400813  mov dword [rbp-index], 0
   ,=< 0x0040081a  jmp 0x40083d
.----> 0x0040081c  mov eax, dword [rbp-index]
|  |   0x0040081f  cdqe
|  |   ; the array of indices we stored above
|  |   0x00400821  mov edx, dword [rbp + rax*4 - 0x40]
|  |   0x00400825  mov eax, dword [rbp-index]
|  |   0x00400828  cdqe
|  |   0x0040082a  mov eax, dword [rbp + rax*4 - 0x20]
|  |   0x0040082e  cmp edx, eax
| ,==< 0x00400830  je 0x400839
| ||   ; if they are equal continue, else return 1
| ||   0x00400832  mov eax, 1
|,===< 0x00400837  jmp 0x400848
||`--> 0x00400839  add dword [rbp-index], 1
|| `-> 0x0040083d  cmp dword [rbp-index], 5
`====< 0x00400841  jle 0x40081c
 |     0x00400843  mov eax, 0
 `---> 0x00400848  pop rbp
       0x00400849  ret
```

If we look up the indecise in the array at rbp-0x20 in the linked list we get
0x00000005 = r
0x00000002 = o
0x00000007 = t
0x00000002 = o
0x00000005 = r
0x00000006 = s

the flag is rotors.

