# dicord_music_bot
## 1.Quick start 


### 1.0 Download [Python 3.11](https://www.python.org/downloads/). (Or later version)

 - And then clone the repository and then run the following in terminal (virtual environment).
```
pip install -r requirements.txt
```
 - If your python version isn't 3.11 (later or older version), you may have error for this step. If anything is fine then no problems. :P

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
 - PS: If someone know how to sync global command instantly, please tell me xd.
----------


## 2.Commands (undone, update later)
format:

/command (mandatory argument)  [optional argument]

  

| command |description|note|
|---------|---|---|
| /help   |-show command list||
  
<br>

**Add songs from NetEase Cloud Music:**

| command                   | description                                                | note                                                                                |
|---------------------------|------------------------------------------------------------|-------------------------------------------------------------------------------------|
| /netease_search (keyword) | search the song and add it to the queue                    |
| /netease_user [username]  | set the user so that you can add it's playlist to the queue | The default user (provided in config.py) will be set if the username isn't provided |
| /netease_playlist [number]| add No. of the playlist to the queue                       | if no arg provided, the bot will display all user's playlists again                 |

<br>

**Add songs from Youtube:**

| command                    | description                        | note                                                  |
|----------------------------|------------------------------------|-------------------------------------------------------|
| /youtube_search (keywords) | search by the keyword from YouTube |                                                       |
| /url_search (url)          | add song by url                    | it support multiple websites (e.g. YouTube, BiliBili) |

<br>

**Control commands:**

| command                | description                                  | note                                                                                                                         |
|------------------------|----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| /play                  | to start playing the queue                   | If the bot was already join other channel in this server, you may user command ".join" to move it to your channel.           |
| /jump (number)         | jump to the target song                      |
| /skip                  | skip the current song and go to the next song |
| /pause                 | pause the music                              |
| /resume                | resume the music                             |
| /stop                  | stop playing music                           |
| /queue [number]        | show 20 songs of the queue                   | If no arg provided, the display will start at the current playing music, otherwised start at `number`                        |
| /delete (target) [end] | delete songs from the queue                  | Only `target` provided -> delete song at `target` position <br> Both of args provided -> delete songs from `target` to `end` |
| /clear                 | clear the queue                              |
| /play_mode (mode)      | change the playmode                          | 1. default: play the queue once only <br> 2. loop: loop the playlist <br> 3. random: shuffle the playlist                    |
| /save                  | unimplemented command                        |
| /load                  | unimplemented command                        |
