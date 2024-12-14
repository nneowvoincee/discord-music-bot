from discord.ext import commands

dic = {}
with open('config.txt', 'r', encoding='utf-8') as f:
    args = f.readlines()
    for each in args:
        arg = (each.rstrip('\n').replace(' ', '')).split('=')    # arg = [arg_name,data]
        if len(arg) == 1:
            arg.append('')
        dic[arg[0]] = arg[1]    # arg_name:data

for i in ['token', 'default_user', 'default_playmode', 'search_VIP_in_ytb',
          'test_channel_id', 'testing']:
    if i not in dic.keys():
        raise KeyError(f'Missing "{i}" variable in config.txt')

if dic['default_playmode'] not in ['default', 'loop', 'random']:
    print('Unexpected value for default_playmode.')
    dic['default_playmode'] = 'default'

if dic['token'] == '':
    raise ValueError('Missing token in config.txt')

if int(dic['testing']) and not dic['test_channel_id']:  # in testing mode but test_channel_id is empty
    raise ValueError("You're in testing mode but the testing channel is missing. \n"
                     " Or you can set 'testing' to 0 in config.txt to disable testing mode")

token = dic['token']
default_user = dic['default_user']  # 默认网易云用户名
default_playmode = dic['default_playmode']    # default/loop/random

search_VIP_in_ytb = True    # If the songs in NetEase music is VIP-required, it will try to find the same song in YouTube (but search song by yld is time-consuming)
name_length_limit = 16

# for debugging
testing = bool(int(dic['testing']))
test_channel_id = int(dic['test_channel_id']) if testing else 0

command_help = '''
--------------
Add songs from NetEase Cloud Music:

/netease_search\t\t\t\t-keyword searching
/netease_user\t\t\t\t\t-Set user by name
/netease_playlist\t\t\t\t -display playlist/add playlist to the queue

--------------
Add songs from Youtube:

.youtube_search -keyword searching
.url_search

--------------
Control commands:

/play/jump/skip
/pause/resume/stop

/queue/delete/clear
/play_mode

/save/load  (Not Implemented)
--------------
'''

headers = {'X-Real-IP': '118.88.88.88',
           'cookie': "os=pc"}


ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ar 48000 -ac 2 -b:a 64k',
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