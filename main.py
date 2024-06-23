# This Python file uses the following encoding: utf-8
import pyncm_async
import discord

import config


prefix = '.'
intent = discord.Intents.default()
intent.message_content = True
intent.voice_states = True
bot = config.MusicBot(command_prefix=prefix, intents=intent)


bot.remove_command('help')   # 删除默认的help指令
extension_list = ["commands.control", "commands.netease", "commands.youtube"]



@bot.event
async def on_ready():

    for extension in extension_list:
        await bot.load_extension(extension)

    for guild in bot.guilds:
        await register(guild)

    #for i in command_list:
    #    print(i, end=" | ")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="/help"))
    print(f'{bot.user.name} starts working.')
    print(bot.servers_data)


@bot.event
async def on_guild_join(guild):
    await register(guild)
    return


@bot.event
async def on_guild_remove(guild):
    bot.servers_data[guild.id]['user']['session'].aclose()
    del bot.servers_data[guild.id]
    return


async def register(guild):
    def get_new_session():
        session = pyncm_async.CreateNewSession()
        session.headers.update(config.headers)
        return session

    print(f"Join {guild.name}.")
    bot.servers_data.update({guild.id: {'queue': [],   # 播放列表
                                    'current_song': -1,    # 当前歌曲序号
                                    'playback_continue': True,
                                    'play_mode': config.default_playmode,
                                    'user': {'user_name': '', 'id': '', 'playlists': [],
                                             'session': get_new_session()}}
                         })
    return


# leave the voice channel if no one in the voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    vc = member.guild.voice_client

    if vc and not vc.is_playing() and len(vc.channel.members) == 1:
        await vc.disconnect()
    return


# the bot will response to other bot's message if these lines are added
#@bot.event
#async def on_message(message):
#    ctx = await client.get_context(message)
#    await client.invoke(ctx)


@bot.command()
async def join(ctx):

    if not ctx.author.voice:
        await ctx.send('You should join a channel first')
        return

    channel = ctx.author.voice.channel  # target channel

    if ctx.voice_client:
        vc = ctx.voice_client   # bot

        if vc.channel == ctx.author.voice.channel:
            await ctx.send('I am already join the channel')
        else:
            await vc.move_to(channel)
    else:
        await channel.connect()

    return

@bot.command()
async def sync(ctx):
    fmt = await bot.tree.sync()
    await ctx.send(f'{len(fmt)} commands synced.')

@bot.command()
async def test(ctx):
    if config.testing == True:
        print()
        print(ctx.guild.id, ':')
        print(bot.servers_data[ctx.guild.id])

@bot.command()
async def vc(ctx):
    print(ctx.voice_client)

#print(config.token)
if __name__ == '__main__':
    bot.run(config.token)




