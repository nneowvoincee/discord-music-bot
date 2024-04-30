

pip install discord.py[voice]

pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
pip install pyncm_async

pip install pycryptodome

Command list:
1.Control command:
.play                       -bot will start playing the music in the queue
.pause                      -pause the music
.resume                     -resume the music
.stop                       -end playing music
.skip                       -jump to the next music immediately
.clear/cl                   -clear the playlist
.playmode [mode]            -default(play once)/ loop(play orderly forever)/ random
.delete [number1] [number2] -1.delete and skip the currently playing songs if no number provided
/del                         2.the target songs will be deleted from the playlist if the first number provided only
                             3.delete a range of songs (num1 - num2) if two numbers provided


以下所有网站可以用youtube_search指令url搜索（理论上
All the following websites are supported by 'youtube_search' command url search.
http://ytdl-org.github.io/youtube-dl/supportedsites.html