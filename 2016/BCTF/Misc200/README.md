# Misc 200: hsab

Connecting to the server we have to give a proof of work, then we are dropped into a shell.
No other programs are loaded with it, checking /bin with 'cd /bin/; echo \*' we see
only bash and a server binary.

Checking /home there is a ctf/ directory and inside is flag.ray which probably contains the flag,
the only problem is reading. It would be pretty simple with a

```
while read line; do
	echo $line;
done < flag.ray
```

but it seems they blocked redirects, so < flag.ray won't work, so instead I went with history,
which will print out the entire HISTFILE. But history reloads the history at startup, so starting
a new bash after setting it will solve this. In the end I used:

```
HISTFILE=/home/ctf/flag.ray /bin/bash
history
```

and the flag is: BCTF{ipreferzshtoba}
