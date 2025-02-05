import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

from config import command_help, ffmpeg_options, MusicBot, testing, test_channel_id


class Control(commands.Cog):
    def __init__(self, bot: MusicBot) -> None:
        self.bot = bot

    @app_commands.command(name='help', description='Display commands list.')
    async def command_help(self, interaction: discord.Interaction):
        await interaction.response.send_message(command_help)
        return

    @app_commands.command(description='Start playing songs.')
    async def play(self, interaction: discord.Interaction):
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        response = interaction.response

        if not queue:  # == 0
            await response.send_message('Queue is empty.')
            return

        # 加入频道
        if interaction.user.voice:
            vc = interaction.guild.voice_client
            if not vc:
                vc = await interaction.user.voice.channel.connect()

        else:
            await response.send_message('You are not in a channel')
            return

        if vc.is_playing():
            await response.send_message('I am playing song now')
            return

        if server_data['play_mode'] == 'default' and server_data['current_song'] >= (len(queue) - 1):
            server_data['current_song'] = -1

        await response.send_message('Start playing songs.')
        await self.play_next(vc=vc, text_channel=interaction.channel, server_data=server_data)
        return

    @app_commands.command(description='Jump to the target song.')
    async def jump(self, interaction: discord.Interaction, num: int):
        server_data = self.bot.servers_data[interaction.guild.id]
        response = interaction.response
        queue = server_data['queue']

        num -= 1  # user input 1 means index 0 of queue
        queue_length = len(queue)

        if not (0 <= num < queue_length):  # check if arg is out of range
            await response.send_message(f'播放列表里面只有{queue_length}首歌')
            return

        if not interaction.user.voice.channel:
            await response.send_message('You should join a channel first')
            return

        # connect to the channel if not
        vc = interaction.guild.voice_client
        if not vc:
            vc = await interaction.user.voice.channel.connect()

        if vc.is_playing() or vc.is_paused():
            server_data['playback_continue'] = False
            vc.stop()
            await asyncio.sleep(1)

        await response.send_message(f'Jump to: {queue[num]["title"]}')
        await self.play_next(vc=vc, text_channel=interaction.channel, server_data=server_data, next_song=num-1)

    @app_commands.command(description='Skip the current song.')
    async def skip(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        response = interaction.response

        if not vc:
            await response.send_message("I'm not in the channel")

        vc.stop()
        await response.send_message("Skip.")
        return

    @app_commands.command(description='Pause playing song.')
    async def pause(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        response = interaction.response

        if not vc:
            await response.send_message("I'm not in the channel")
            return

        vc.pause()
        await response.send_message("Pause.")
        return

    @app_commands.command(description='Resume playing song.')
    async def resume(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        response = interaction.response

        if not vc:
            await response.send_message("I'm not in the channel")
            return

        vc.resume()
        await response.send_message("Resume.")
        return

    @app_commands.command(description='Stop playing song.')
    async def stop(self, interaction: discord.Interaction):
        server_data = self.bot.servers_data[interaction.guild.id]
        vc = interaction.guild.voice_client
        response = interaction.response

        if not vc:
            await response.send_message("I'm not in the channel")
            return

        server_data['playback_continue'] = False
        vc.stop()
        await response.send_message('Terminate.')

        if server_data['current_song'] >= 0:
            server_data['current_song'] -= 1

        return

    @app_commands.command(description="Display up to 50 songs from the currently songs/ begin(optional parameter).")
    async def queue(self, interaction: discord.Interaction, begin: int = None):
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        current_song = server_data['current_song']

        if len(queue) == 0:
            await interaction.response.send_message('Queue is empty.')
            return

        total = 20
        prop = 0.3  # 显示前后歌曲数量的比例
        display = ''
        start = 0
        before = int(total * prop)

        if begin is None:
            if current_song > before:
                start = current_song - before
                display += '...\n'
            else:
                start = 0

        elif 0 < begin <= len(queue):
            if begin > 1:
                start = begin - 1
                display += '...\n'
            else:
                start = 0

        if start + total >= len(queue):     # 检测是否超出播放列表总量
            end = len(queue)
        else:
            end = start + total

        displaylist = []
        for begin in range(start, end):  # 歌曲前面的歌曲
            name = queue[begin]['title']

            if len(display) + len(name) > 1800:  # discord消息超过2000字会被转成.txt文字档,所以要分开发送
                displaylist.append(display)
                display = ''

            if begin == current_song:
                display += '\n'.join(['--------------',
                                      f'{begin + 1}. {queue[begin]["title"]}',
                                      '--------------\n'])
            else:
                display += f'{begin + 1}. {queue[begin]["title"]}\n'

        else:  # 结尾
            if begin < len(queue) - 1:
                display += '...'
            displaylist.append(display)

        await interaction.response.send_message(f'一共{len(queue)}首歌:\n')
        for each in displaylist:
            await interaction.channel.send(each)

        return

    @app_commands.command(description='One num given -> delete song/ Two num given -> delete songs between two numbers')
    async def delete(self, interaction: discord.Interaction, target: int, end: int = None):
        response = interaction.response
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        queue_length = len(queue)
        current_song = server_data['current_song']

        if target and not end:  # one arg is provided

            if 0 < target <= queue_length:
                song = queue.pop(target - 1)
                await response.send_message(f'已从播放列表中移除: {song["title"]}')

                if target - 1 <= current_song:
                    server_data['current_song'] -= 1

            else:
                await response.send_message(f'nothing is deleted (number is out of range)')

            return

        else:  # both of args are provided

            if target > end:
                target, end = end, target

            target = 0 if target < 0 else target
            end = queue_length if end > queue_length else end

            if target == end:
                await response.send_message('nothing is deleted')

            first_song = queue[target - 1]
            last_song = queue[end - 1]
            del queue[(target - 1):end]

            await response.send_message(
                f'成功移除{end - target + 1}首歌:\n{target}.{first_song["title"]}\n{"" if (target + 1 == end) else "..."}\n{end}.'
                f'{last_song["title"]}\n ')

            return

    @app_commands.command(description='Clear the queue.')
    async def clear(self, interaction: discord.Interaction):
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        response = interaction.response

        queue.clear()
        server_data['current_song'] = -1
        await response.send_message('Clear queue successfully')
        return

    @app_commands.command(description='Set/Check the play mode.')
    @app_commands.choices(mode=[
        app_commands.Choice(name="Check", value="check"),
        app_commands.Choice(name="Default", value="default"),
        app_commands.Choice(name="Loop", value="loop"),
        app_commands.Choice(name="Random", value="random")])
    async def mode(self, interaction: discord.Interaction, mode: app_commands.Choice[str] = None):
        server_data = self.bot.servers_data[interaction.guild.id]
        response = interaction.response
        mode = mode.value if mode else None

        match mode:
            case 'default':
                server_data['play_mode'] = 'default'
                await response.send_message("set play mode successfully: default")

            case 'loop':
                server_data['play_mode'] = 'loop'
                await response.send_message('set play mode successfully: loop')

            case 'random':
                server_data['play_mode'] = 'random'
                await response.send_message('set play mode successfully: random')

            case _:
                await response.send_message(f"Now: {server_data['play_mode']}")

    # (helper function) Be called in the 'play' command function
    async def play_next(self, vc: discord.VoiceClient, text_channel, server_data, next_song=None):

        if not server_data['playback_continue']:
            server_data['playback_continue'] = True
            return

        queue = server_data['queue']
        play_mode = server_data['play_mode']

        if len(vc.channel.members) <= 1:  # nobody in channel
            await vc.disconnect()
            await text_channel.send('bye~')
            return

        if next_song:
            server_data['current_song'] = next_song
        elif play_mode == 'default':
            server_data['current_song'] += 1

        elif play_mode == 'loop':
            server_data['current_song'] = (server_data['current_song'] + 1) % len(server_data['queue'])

        elif play_mode == 'random':
            server_data['current_song'] = random.randint(0, len(server_data['queue']) - 1)

        if server_data['play_mode'] == 'default' and server_data['current_song'] >= len(queue):
            server_data['current_song'] -= 1
            await text_channel.send('The queue has finished playing.')
            return

        # 播放音频
        current_song = server_data['current_song']  # number
        song = server_data['queue'][current_song]  # data

        loop = asyncio.get_running_loop()
        # source = await discord.FFmpegOpusAudio.from_probe(song['url'], **ffmpeg_options)
        source = discord.FFmpegOpusAudio(song['url'], **ffmpeg_options)
        vc.play(source,
                after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(vc=vc,
                                                                                text_channel=text_channel,
                                                                                server_data=server_data), loop))

        await text_channel.send(f'正在播放: {song["title"]}\n{song["duration"]}\t--{song["uploader"]}\n ')

        return

async def setup(bot: MusicBot) -> None:
        await bot.add_cog(Control(bot))
