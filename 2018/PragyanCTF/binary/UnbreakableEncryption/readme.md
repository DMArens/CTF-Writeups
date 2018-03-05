# Binary 350: Unbreakable Encryption
>Your friend, Liara, has encrypted all her life secrets, using the one of the best encryptions available in the world, the AES. She has challenged you that no matter what, you can never read her life secrets.
>
>The encryption service is running at :- 128.199.224.175:33000
>The binary file is named aes_enc.
>
>Her encrypted life secrets are as follows :-
>
>0000 - 40 87 68 1a b0 23 73 c4 61 44 b4 c0 21 f1 63 0b @.h..#s.aD..!.c.
>0010 - 73 e9 0d 38 e4 bd d8 33 41 64 2c 43 85 d4 54 0e s..8...3Ad,C..T.
>0020 - f5 bc 8c 02 db ee 0d e8 d6 29 81 3a 5f cb 63 bd .........).:_.c.

We are also given a binary `aes_enc_unbuf` and dummy aes files `key.aes` and `iv.aes`

## Disassembly With Radare2
The binary is statically compiled, but excluding the libraries, there isn't much to reverse.
`main` reads your input, prints it, and passes it to `encrypt` which loads the aes files, encrypts the
message, and dumps it to the screen. It then calls `decrypt` which decrypts and dumps the
plaintext to the screen.

There are two bugs in main:
```assembly
[0x08048d30]> s 0x08048d30
[0x08048d30]> pd 6
|           0x08048d30      lea eax, [local_8ch]
|           0x08048d36      push eax
|           0x08048d37      push 0x8182185                             ; "%s"
|           0x08048d3c      call sym.__isoc99_scanf
|           0x08048d41      add esp, 0x10
|           0x08048d44      mov byte [local_dh], 0
[0x08048d30]> ? 0x8c - 0xd
127 0x7f 0177 127 0000:007f 127 "\x7f" 01111111 127.0 127.000000f 127.000000
```

It's doing `scanf("%s")` into the local `local_8ch` and null terminates at `local_dh`.
Although it terminates after 127 characters, it is not checking the length of the input,
so we can overflow the buffer, though it will always have a `\x00` at the 128th position.

This alone is not exploitable, since there are stack canaries, and the `encrypt` and `decrypt`
functions stop on the null byte.

The second bug is a printf vulnerability:
```assembly
[0x08048d6c]> s 0x08048d6c
[0x08048d6c]> pd 3
|           0x08048d6c      lea eax, [local_8ch]
|           0x08048d72      push eax
|           0x08048d73      call sym._IO_printf
[0x08048d6c]>
```
It's calling `printf(local_8ch)` which is our input, and we can exploit this by using printf
format strings such as `%x`, `%p`, `%s`, and `%n`. Using the first 3 we can leak memory from
the stack, but we can't get anything useful. The stack canary is there, but at that point
we've already passed our opportunity for input.


The other option is `%n` which allows us to write the number of characters printed into an
integer pointer. For example:
```c
char *a = "abc";
int length;
printf("%s\n%n", a, &length);
```
would set `length` to 4 since we printed `abc\n`. We can use this to modify memory by printing
characters until we reach the value we want to write into memory, and then using `%n`. Since we
might want to insert large numbers, `%hhn` is similar takes a `char` pointer instead of `int`.

Now we need something useful to modify. My first though was to check the data section, which
is writeable and the numbers are consistent across executions:

```
[0x0822f060]> s section..data
[0x0822f060]> pxw 100
0x0822f060  0x00000000 0x00000000 0x00000000 0x00000000  ................
0x0822f070  0x00000000 0x00000000 0x00000000 0x00000000  ................
0x0822f080  0x6854200a 0x6e652065 0x70797263 0x20646574  . The encrypted 
0x0822f090  0x7373656d 0x20656761 0x20726f66 0x20656874  message for the 
0x0822f0a0  0x65766967 0x6c70206e 0x746e6961 0x20747865  given plaintext 
0x0822f0b0  0x3a207369 0x000a202d 0x00000001 0x00000001  is :- ..........
0x0822f0c0  0x0811e920                                    ...
[0x0822f060]>
```
We have a string that's printed out before our encrypted message

```assembly
[0x0822f060]> axt @ 0x0822f080
sym.encrypt 0x8048bf5 [data] push str._n_The_encrypted_message_for_the_given_plaintext_is_:___n
[0x0822f060]> s 0x8048bf5
[0x08048bf5]> pd 4
|           0x08048bf5      push str._n_The_encrypted_message_for_the_given_plaintext_is_:___n ; obj.ciphertext_msg ; 0x822f080 ; "\n The encrypted message for the given plaintext is :- \n"
|           0x08048bfa      call sym._IO_printf
|           0x08048bff      add esp, 0x10
|           0x08048c02      mov eax, dword obj._IO_stdout              ; obj.stdout ; [0x8230538:4]=0x8230280 obj._IO_2_1_stdout_
[0x08048bf5]> 
```
It is referenced in `encrypt` when it is passed to `printf`. If we modify this string, it would give us
another format string vulnerability. The difference here is that this call is in `encrypt` and it is after
the aes key and iv have been loaded onto the stack!

## The Exploit
So we have a possible exploit:
1. insert a format string which writes to the data section
2. use (1) to write another format string at `0x0822f080` which dumps stack info
3. use the leaked key and iv to decrypt the ciphertext

The only problem is the null termination in `main`. `printf` will stop at the null byte, so
our first format string cannot be longer than 127 characters.

Our initial format string will look something like this:
`\x80\xf0\x22\x08%033x%7$hhn`

There are 3 pieces to this example:
1. `\x80\xf0\x22\x08`: The little endian address we want to write to.
2. `%033x`: The format string to print a zero-padded (to 33 digits) hex number.
            This brings the total number of chars printed to 4 from (1) + 33,
            which is 37 or ascii `%`
3. `%7$hhn`: the format string to take the 7th stack parameter, and use it as
             a `char` pointer, which printf will write 37 to. The 7th parameter
             aligns on the stack to the begining of our input, where we have 
             written a pointer to the data section.

this ends up writing `%` to `0x0822f080`. As a proof of concept, I wrote a format string to also write
an `x` into 0x0822f081. Then the binary would print:
>????? The encrypted message for the given plaintext is :-

where the `?????` was a hex number from the stack.

The format string to build will be complicated, so it's best to write a script to do it. I used python
and pwntools. Initially the script was attempting to write a ton of `%p` into the string, but I was only
able to leak part of the IV before hitting the 127 byte limit. The second attempt was to write `%??$p` into
the string, where ?? points printf to leak 4 bytes further up the stack. Then increment this ?? and launch
the attack again, enough times to leak the key and IV.

The last piece is that writing `%??$p` byte by byte requires knowing how many bytes have been printed in order
to make sure `%n` writes the correct value. To do this, I sort the string, and the corresponding write address,
so that the number printed is incrementing to the correct ascii values.

The final script is [solve.py](./solve.py)
