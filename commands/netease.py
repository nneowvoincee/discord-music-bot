import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, Button, View

from config import MusicBot, default_user, name_length_limit
from utils import netease_music_catch


class Netease(commands.Cog):
    def __init__(self, bot: MusicBot) -> None:
        self.bot = bot

    @app_commands.command(name='netease_search')
    async def search(self, interaction: discord.Interaction, search_word: str):
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        session = server_data['user']['session']
        ctx = interaction.followup

        await interaction.response.send_message('等我亿下......')

        info = await netease_music_catch.song_catch(search_word, session)
        await interaction.delete_original_response()

        if not info:
            await ctx.send('查无此歌: ' + search_word)

        # 创建选择列表
        select = Select(
            placeholder=search_word,
            options=[discord.SelectOption(label=info[i]['title'],
                                          value=str(i),
                                          description=f"{info[i]['duration']}  ——{info[i]['uploader'] if len(info[i]['uploader']) < 15 else info[i]['uploader'][:15] + '...'}")
                     for i in range(len(info))]
            # label=歌名, value=第几选项, description=时长/歌手
        )

        # 创建取消按钮
        button = Button(
            style=discord.ButtonStyle.red,
            label='Cancel'
        )

        # 将歌加入播放列表
        async def join_list(interaction):
            value = int(select.values[0])
            song_data = info[value]
            queue.append(song_data)
            await msg_selectlist.delete()

            # 发送成功信息
            message = f"成功添加歌曲:\n\t{song_data['title']}\n\t{song_data['duration']}   --{song_data['uploader']}"
            await ctx.send(message)

        # cancel message
        async def cancel(interaction):
            await msg_selectlist.delete()

        select.callback = join_list
        button.callback = cancel
        view = View()
        view.add_item(select)
        view.add_item(button)

        msg_selectlist = await ctx.send(view=view)
        return

    @app_commands.command(name='netease_user')
    async def user(self, interaction: discord.Interaction, search_word: str = default_user):
        server_data = self.bot.servers_data[interaction.guild.id]
        session = server_data['user']['session']
        ctx = interaction.followup

        await interaction.response.send_message('等我亿下')

        user_data = await netease_music_catch.user_catch(search_word, session)
        if not user_data:
            await ctx.send(f'No user found: {search_word}')

        server_data['user']['user_name'] = user_data['nickname']
        server_data['user']['id'] = user_data['id']
        server_data['user']['playlists'] = user_data['playlists']

        # 返回成功信息
        embed = discord.Embed(title='Set user successfully', description=user_data['signature'])
        embed.set_thumbnail(url=user_data['avatarUrl'])
        await interaction.delete_original_response()
        await ctx.send(embed=embed)
        await asyncio.sleep(1)

        # 发送用户拥有的歌单
        display = '搜索到以下歌单:\n(输入数字序号来添加歌曲,如: /netease_playlist 1)\n'
        displaylist = []
        count = 0
        for each in server_data['user']['playlists']:
            if len(display) + len(each['name']) > 2000:  # 防止discord消息超过2000字会被转成文字档
                displaylist.append(display)
                display = ''

            if len(each['name']) <= name_length_limit:
                playlist_name = each['name']
            else:
                playlist_name = each['name'][:name_length_limit] + '...'

            count += 1
            display += f'{count}. {playlist_name}\n'

        displaylist.append(display)
        for each in displaylist:
            await ctx.send(each)

    @app_commands.command(name='netease_playlist')
    async def playlist(self, interaction: discord.Interaction, num: int = None):
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        session = server_data['user']['session']
        ctx = interaction.followup

        if server_data['user']['id']:
            playlists = server_data['user']['playlists']
        else:
            await interaction.response.send_message('目标用户未设置, 请使用指令 /netease_user')
            return

        if num is None:  # 显示该用户拥有的歌单

            await interaction.response.send_message('搜索到以下歌单:\n(输入数字序号来添加歌曲,如: .playlist 1)\n')
            display = ''
            displaylist = []
            count = 0
            for each in playlists:
                if len(display) + len(each['name']) > 2000:  # 多于2000字分开发送，否则超过2000字会被转成文字档
                    displaylist.append(display)
                    display = ''

                if len(each['name']) <= name_length_limit:
                    playlist_name = each['name']
                else:
                    playlist_name = each['name'][:name_length_limit] + '...'    # 歌单名字过长则后半部分被省略号替代

                count += 1
                display += f'{count}. {playlist_name}\n'

            displaylist.append(display)
            for each in displaylist:
                await ctx.send(each)

        else:
            await interaction.response.send_message('等我亿下...')
            if 0 < num <= len(playlists):
                tracks = await netease_music_catch.playlists_catch(playlists[num - 1]['id'], session)
                await interaction.delete_original_response()
                # print(songs_data['playlist'])
                if tracks:
                    queue.extend(tracks)
                    await ctx.send(f"已将{len(tracks)}首歌曲添加到播放列表中")
                    return
                else:
                    await ctx.send("歌单中没有歌曲")
                    return
            else:
                await ctx.send(f'the user only have {len(playlists)} playlists.')
                return


async def setup(bot: MusicBot) -> None:
    await bot.add_cog(Netease(bot))