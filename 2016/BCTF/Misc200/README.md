# Misc 200: hsab

Connecting to the server we give a proof of work, and then we are dropped into a shell.
No other programs are loaded with it, checking /bin with
```
cd /bin
echo \*
```
we see only bash and a server binary. Checking /home there is a ctf/ directory and inside is flag.ray
which probably contains the flag, the only problem is reading it. A simple solution would be:
```
while read line; do
	echo $line;
done < flag.ray
```
but it seems they blocked redirects, so 'done < flag.ray' won't work. Instead, I went with history
which will print out the contents of HISTFILE from your environment. History loads HISTFILE at startup, 
so starting a new bash after setting it will solve this. In the end I used:
```
HISTFILE=/home/ctf/flag.ray /bin/bash
history
```
and the flag is: BCTF{ipreferzshtoba}
