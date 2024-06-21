# dicord_music_bot
## 1.Quick start

## 2.Commands (outdated, update later)
format:

prefix-command (mandatory argument)  [optional argument]

  

|command|description|note|
|---|---|---|
|.help|-show command list||
  
<br>

**Add songs from NetEase Cloud Music:**
|command|abbr.|description|note|
|---|---|---|---|
|.search (song name)|.s|-search the song and add it to the queue|
|.user [user name]||-show user's playlists|The default user(config.py) will be set if the username isn't provided|
|.playlist [number]|.l| -add song of the playlist to the queue|if send command without number (only .playlist), the robot will show user's playlists again|

<br>

**Add songs from Youtube:**
(PS: It supports url from some of other platforms (Facebook, Bilibili .etc)

|command|abbr.|description|note|
|---|---|---|---|
|.youtube (keywords/url of the videos/songs)|.yts|-search the audio from YouTube/webite| the bot will search from YouTube if keywords are provided|

<br>

**Control commands:**

|command|abbr.|description|note|
|---|---|---|---|
|.play||-to start playing the queue|If the bot was already join other channel in this server, you may user command ".join" to move it to your channel.|
|.jump (number)|.j|-jump to the target song|
|.skip||-skip the current song and go to the next song|
|.pause||-pause the music|
|.resume||-resume the music|
|.stop||-stop playing music|
|.join||-let the bot join your channel|
|.clear|.cl|-clear the queue|
|.delete [number] [number]|.del|-delete songs from the queue| 0/1/2 arguments provided:<br>0. delete the current song<br>1. delete the target song<br>2. delete a range of songs|
|.play_mode (mode/number)|.pm|-change the playmode|1. default: play the queue once only <br> 2. loop: loop the playlist <br> 3. random: shuffle the playlist|
|.queue [number]||-show 50 songs of the queue|50 songs around the current song will be shown if no arument provided.|
|.disconnect||-let the bot leaves the channel|
|.save||unimplemented command|
|.load||unimplemented command|
