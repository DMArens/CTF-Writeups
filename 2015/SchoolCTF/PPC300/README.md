# PPC300
http://sibears.ru:10002/

this one is a website, with a lightning bolt button in the middle and a username/password field.
it keeps track of how many times you click the button in 10 seconds, and tells you that it's not much.

so we need to press it a lot. let's have javascript do that for us.

1. give the button an id "test"
2. i=0; while(i < 500) { $('#test').click(); i++; }
3. flag

Flag is we_need_one_more_world_to_save_it
