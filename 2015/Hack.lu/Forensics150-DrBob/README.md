# Dr. Bob - Forensic 150 - by lama
There are elections at the moment for the representative of the students and the winner will be announced 
tomorrow by the head of elections Dr. Bob. The local schoolyard gang is gambling on the winner and you could 
really use that extra cash. Luckily, you are able to hack into the mainframe of the school and get a copy of 
the virtual machine that is used by Dr. Bob to store the results. The desired information is in the file 
/home/bob/flag.txt, easy as that.

[download](https://school.fluxfingers.net/static/chals/dr_bob_e22538fa166acecc68fa17ac148dcbe2.tar.gz)

[mega.nz mirror](https://mega.nz/#!qoUDxYrB!W-C6vZxiulkaZ9ONWbyohCpAOfRbLtvHIgIICvjeZWk)

# Solution
The given file is a VirtualBox vm, with a saved state at the login screen. We need to retrieve the flag 
from /home/bob/flag.txt. I rebooted the vm to try and reset the password manually or get a shell, but the
drive is encrypted. So instead, we need to:

1. Get the key from memory
2. Decrypt the drive
3. Win

I booted finnix in the vm to do the rest:

## Getting The Key
dump memory
```
vboxmanage debugvm "Safe" dumpvmcore --filename dump.elf
```

find the key
```
./aeskeyfind dump.elf
1fab015c1e3df9eac8728f65d3d16646
Keyfind progress: 100%
```

## Getting The Flag
we want to decrypt /dev/vg/home, so get some info about it
```
cryptsetup luksDump /dev/vg/home
blockdev --getsz /dev/vg/home
```

then decrypt it using that info
```
dmsetup create luksthing --table "0 5865472 crypt aes-ecb-essiv:sha1 1fab015c1e3df9eac8728f65d3d16646 0 /dev/vg/home 0"
```

now read it for the flag
```
strings /dev/mapper/luksthing | less
```

and we have a flag
