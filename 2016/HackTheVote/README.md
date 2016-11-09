# Exploit 100: irs

We are given a linux x86 executable file
```
dan@localhost:100-irs$ file irs
irs: ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, BuildID[sha1]=00041d69ae706e1877c8a618dc092b33499c4d6d, stripped
```

Connecting to the server, or running the binary, we get a tax return filing system,
with an entry for Donald Trump. We are told the flag is Trump's password.

The system provides a few options:

```
Welcome to the IRS!
How may we serve you today?
1. File a tax return
2. Delete a tax return
3. Edit a tax return
4. View a tax return
5. Exit
```

To Create a return we must provide a name, password, income, and deductable.
Deleting, Editing, and Viewing the files require the name and password. From here
I used BinaryNinja to look for the vulnerability.

The vulnerability was easy to spot: there are no stack canaries, and the function
to edit a tax return contains a call to gets with a stack buffer.

![stack buffer overflow becuase of gets](hackthevote_irs_overflow.png)

Also, all password checks happen in main() before calls to other function handlers,
so we just need to overwrite the return address with the view function, and have it
print out Donald Trump's return (the only parameter is an index for which tax return).

About the returns, they are stored in an array on the stack, with a limit of
5 returns at a time, and each has the structure:
```
struct tax_return {
        char name[0x20];
        char pass[0x20];
        int income;
        int deductable;
}
```
![initial Donald Trump entry created in main](hackthevote_irs_namelist.png)

The only problem is leaking a stack address in order to find out where the tax returns
are stored in memory. It turns out they provide that exact address for us if we attempt
to create more tax returns than allowed:
```
printf("If this problem persists, contact us at this address: %p", tax_return_array);
```
![leaking stack addresses for us...](hackthevote_irs_addressleak.png)

1. leak the array address
2. call view(array address)
3. get flag

the solution is in [solve.py](solve.py) using pwntools

```
dan@localhost:100-irs$ ./solve.py
[+] Opening connection to irs.pwn.republican on port 4127: Done
[+] Recieving all data: Done (526B)
[*] Closed connection to irs.pwn.republican port 4127
Your changes have been recorded!
--------------------------------------------------------------------------------
| Name: Donald Trump                                                           |
| Income: 1316134911                                                           |
| Deductable: 1316134911                                                       |
| Password: flag{c4n_1_g3t_a_r3fund}                                           |
--------------------------------------------------------------------------------
```
