
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, Button, View

from config import MusicBot
from utils import youtube_catch

class Youtube(commands.Cog):
    def __init__(self, bot: MusicBot) -> None:
        self.bot = bot

    @app_commands.command(description='Keyword searching in YouTube.')
    async def youtube_search(self, interaction: discord.Interaction, keyword: str):
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        ctx = interaction.followup

        await interaction.response.send_message('等我亿下......')


        songs_data = await youtube_catch.query_catch(keyword, ctx)

        await interaction.delete_original_response()

        if not songs_data:
            await ctx.send(f'查无结果: {keyword}')
            return

        select = Select(
            placeholder=keyword,
            options=[discord.SelectOption(label=songs_data[i]['title'],
                                          value=str(i),
                                          description=f"{songs_data[i]['duration']} --{songs_data[i]['channel']}")
                     for i in range(len(songs_data))]
            # label = song name, value = n-th selection, description = duration --author
        )

        button = Button(
            style=discord.ButtonStyle.red,
            label='Cancel'
        )

        async def join_list(interaction):
            value = int(select.values[0])
            song_data = {'platform': 'ytb',
                         'title': songs_data[value]['title'],
                         'uploader': songs_data[value]['channel'],
                         'duration': songs_data[value]['duration'],
                         'url': songs_data[value]['url']}

            queue.append(song_data)
            await msg_selectlist.delete()
            # 发送成功信息
            message = f"成功添加歌曲:\n\t{song_data['title']}\n\t{song_data['duration']}   --{song_data['uploader']}\n"
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

    @app_commands.command(description='Url of YouTube video.')
    async def url_search(self, interaction: discord.Interaction, url: str):
        server_data = self.bot.servers_data[interaction.guild.id]
        queue = server_data['queue']
        ctx = interaction.followup

        await interaction.response.send_message('等我亿下......')

        result = await youtube_catch.url_catch(url)

        await interaction.delete_original_response()

        match result:  # check if error
            case 'Invalid url':
                await ctx.send('Invalid url')
                return
            case 'Extract fail':
                await ctx.send('Cannot extract information from this URL (￣ ‘i ￣;)')
                return
            case 'Unsupported URL':
                await ctx.send('Unsupported url')
                return
            case 'Other error':
                await ctx.send('???')
                return

        queue.append(result)

        await ctx.send(f'''成功添加歌曲:\n\t{result['title']}\n\t{result['duration']}   --{result['uploader']}\n
        ''')
        return

async def setup(bot: MusicBot) -> None:
    await bot.add_cog(Youtube(bot))