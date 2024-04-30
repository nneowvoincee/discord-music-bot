from discord.ext import commands

dic = {}
with open('config.txt', 'r', encoding='utf-8') as f:
    args = f.readlines()
    for each in args:
        arg = (each.rstrip('\n').replace(' ', '')).split('=')    # arg = [arg_name,data]
        if len(arg) == 1:
            arg.append('')
        dic[arg[0]] = arg[1]    # arg_name:data

for i in ['token', 'default_user', 'default_playmode']:
    if i not in dic.keys():
        raise KeyError(f'Missing "{i}" variable in config.txt')

if dic['default_playmode'] == '':
    dic['default_playmode'] = 'default'

if dic['token'] == '':
    raise ValueError('Missing token in config.txt')

token = dic['token']
default_user = dic['default_user']  # 默认网易云用户名
default_playmode = dic['default_playmode']    # default/loop/random
search_VIP_in_ytb = bool(int(dic['search_VIP_in_ytb']))

name_length_limit = 16

command_help = '''
(mandatory argument)  [optional argument]

.help\t\t\t\t\t\t\t\t\t\t\t -show command list
--------------
Add songs from NetEase Cloud Music:

.search/s (song name)\t\t\t-search the song and add it to the queue
.user [user name]\t\t\t\t\t -show user's playlists
\t\t\t\t\t\t\t\t\t\t\t\t\t\t(The default user will be set if the username isn't provided)
.playlist/l [number]\t\t\t\t -add song of the playlist to the queue, 
\t\t\t\t\t\t\t\t\t\t\t\t\t\t if send command without number (only .playlist), 
\t\t\t\t\t\t\t\t\t\t\t\t\t\t the robot will show the list of the playlists again

--------------
Add songs from Youtube: (PS: It supports url from some of other platforms (Facebook, Bilibili .etc)

.youtube/yts (keywords/url of the videos/songs)

--------------
Control commands:

.play\t\t\t\t\t\t\t\t\t\t\t\t  -to start playing the queue
.jump (number)\t\t\t\t\t\t\t  -jump to the target song
.skip
.pause
.resume
.stop

.join\t\t\t\t\t\t\t\t\t\t\t\t\t\t  -move bot to your current channel
.clear/cl\t\t\t\t\t\t\t\t\t\t\t\t  -clear the queue
.delete/del [number] [number]\t   -delete songs from the queue
.play_mode/pm (mode/number)\t-default(play the queue once only)/loop/random
.queue [number] \t\t\t\t\t\t\t\t -show 50 songs of the queue

.disconnect -leave the channel
.save
.load

'''

headers = {'X-Real-IP': '118.88.88.88',
           'cookie': "os=pc"}


ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
    'method': 'fallback',
    'executable': r'./tools/ffmpeg/bin/ffmpeg.exe'
}


ytdl_options = {
    'quiet': True,
    'noplaylist': True,
    'format': 'bestaudio/best'
}

class MusicBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.servers_data = dict()  # 每个server拥有独立的 播放列表/模式..etc
        super().__init__(*args, **kwargs)