# Reverse 300: Realism
Did you know that x86 is really old? I found a really old Master Boot Record that I thought was quite interesting! At least, I think it's really old...

```
qemu-system-i386 -drive format=raw,file=main.bin
```

## Setup
We are given main.bin, and x86 boot sector. Running it in qemu we get a prompt for a flag with 20 blank spaced.
When 20 characters are type it displays a 'wrong flag' message, and we can see the 'correct flag' string in the
binary.

### Static Analysis
I used radare2 for disassembly
```
r2 -a x86 -b 16 main.bin
```

### Dynaic Analysis
We need a combination of qemu and gdb to debug the boot sector. Startup qemu and use
`-s -S` to start emulation with paused execution, and to enable debuging on port 1234
```
qemu-system-i386 -s -S -drive format=raw,file=main.bin
```

then attach with gdb
```
gdb
target remote localhost:1234
set architecture i8086
b *0x7c8e
c
```
## Reversing
Most of the code implements the flashing text colors and user input, and I will skip over those.
If you want learn how input/output is handled in real mode, read about the following instructions
```
int 0x10 ; AH = 0x13
int 0x16 ; AH = 0
int 0x16 ; AH = 1
```

It stores our input in a buffer at address 0x1234 and keeps a count of how many characters we input.
When it hits 20 it breaks the input loop and checks if the flag is valid with a simple algorithm:

First, it checks if our input starts with "flag"
```
0000:006f      cmp dword [0x1234], 0x67616c66 ; "flag"                                                            
0000:0078      jne 0x14d
```

Then it shuffles our input with `pshufw mm0, mm0, 0x1e` This essential rearranges input
so that 0xaaaabbbbccccdddd becomes 0xccccddddbbbbaaaa.
```
0000:0086      pshufw mm0, mm0, 0x1e
```

### Flag Check Algorithm
Then it moves the other 16 bytes of input into the xmm0 register, and loads
16 bytes starting at address 0x7c00 (offset 0 in the binary) into xmm5. It then
loops through our input 8 times running this check:
```
0000:008e      movaps xmm2, xmm0                
0000:0091      andps xmm2, xmmword [si + 0x7d90]                                                                                                       
0000:0096      psadbw mm5, mm2                                                                                                                         
0000:009a      movaps xmmword [0x1268], xmm5               
0000:009f      mov di, word [0x1268]                       
0000:00a3      shl edi, 0x10                                                                                                                           
0000:00a7      mov di, word [0x1270]                       
0000:00ab      mov dx, si                                                                                                                              
0000:00ad      dec dx                                                                                                                                  
0000:00ae      add dx, dx                                                                                                                              
0000:00b0      add dx, dx                                                                                                                              
0000:00b2      cmp edi, dword [edx + 0x7da8]               
0000:00ba      jne 0x14d  
```

first it loads xmm0 (our input) into the temp variable xmm2, then ANDs it with [si + 0x7d90] where si is
the index counting down from 8. 0x7d90 is an array of bytes equal to 0xFF and one 0x00 such that as it
loops, the AND operation is blanking out two characters of our input. Like this:
```
tmp = input
tmp[i] = 0
tmp[i+8] = 0
```

Then it hits the psadbw instruction, which calculates the sum of absolute differences between two
registers, in this case mm5 and mm2. It works like this:
```
mm5 = 00 03 00 00 00 01 02 00 | 00 00 00 02 02 00 00 00
mm2 = 01 01 00 00 00 01 04 03 | 00 04 00 00 00 01 00 00
dif = 01 02 00 00 00 00 02 03 | 00 04 00 02 02 01 00 00
sum =                      08 | 09
final mm5 = 0x0000000000000008 0000000000000009
```

At 0x00b2 it compares this calcuation with an array in memory. So we have a simple
algorithm, a starting condition for mm5, and the end results of each. I just wrote a simple
python script to solve this using Z3

This is the python script I wrote to solve it with z3:
[solution script](realistic.py)

flag{4r3alz_m0d3_y0}
