# PPC200
this one gave us a directory with lots of directories and files. There's a file called start.txt:
```
start/uspom/yvawi/uihcw/jukrd/ndycl.txt
f
```

so it's the path to another file on one line, and a character on another..
we probably need to follow all of the files and get all of the characters, so I made a script to do that:
```
> cat script.sh 
#!/bin/bash
current='start.txt'
while [ 1 ]; do
        next=`sed '1q;d' $current`
        char=`sed '2q;d' $current`
        flag=$flag$char
        current=$next
        echo $flag
done
> ./script.sh 
f
fl
fla
flag
flag_
flag_1
flag_1s
flag_1s_
flag_1s_1
flag_1s_1t
flag_1s_1t_
flag_1s_1t_w
flag_1s_1t_w@
flag_1s_1t_w@s
flag_1s_1t_w@s_
flag_1s_1t_w@s_t
flag_1s_1t_w@s_t0
flag_1s_1t_w@s_t00
flag_1s_1t_w@s_t00_
flag_1s_1t_w@s_t00_e
flag_1s_1t_w@s_t00_ea
flag_1s_1t_w@s_t00_eas
flag_1s_1t_w@s_t00_easy
```
