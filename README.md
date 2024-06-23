# dicord_music_bot
## 1.Quick start 

----------
### 1.0 Download [Python](https://www.python.org/downloads/). (> 3.11)

 - And then download and extract the code and then run the following in terminal (virtual environment).
```
pip install -r requirements.txt
```

### 1.1 Create you Application(bot) on [Discord Developer Portal](https://discord.com/developers/applications).
 - Many of YouTube video taught you that how to set up your bot, such as [this](https://www.youtube.com/watch?v=UYJDKSah-Ww) (2:16 - 6:30)

### 1.2 Complete config
 - Download the code and extract it, you will see a file named "config.txt" which should have five arguments:

| argument         | description                                                                                                                                                                                                                                                             |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| token            | Token of your application created in 1.1                                                                                                                                                                                                                                |
| default_user     | Use for the command "netease_user" for lazy people don't want to type the user name every time (can be empty)                                                                                                                                                           |
| default_playmode | the default mode of playing songs in the queue <br> (value: default / loop / random)                                                                                                                                                                                    |  
| test_channel_id  | the id of test channel (leave it empty if you don't need testing mode)                                                                                                                                                                                               |
| testing | enable testing mode (when you sync the commands, only your test channel's will be synced, but instantly. Otherwise sync global commands for all channel need one hour.) <br> Just for the people who want to modify the code, otherwise just keep this value to be 0. |

### 1.3 Run the bot
 - Run main.py, and then type `.sync` in discord channel to sync the slash command for the bot. (If nothing happen, you may run `.sync` again after about one hour. [Link](https://www.reddit.com/r/discordapp/comments/ukbu5h/1_hour_wait_on_global_slash_commands_gone/))

## 2.Commands (outdated, update later)
format:

/command (mandatory argument)  [optional argument]

  

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
