import discord
from discord.ext import commands
import youtube_dl
import asyncio
from discord.utils import get
import config
import os

# словари
hello_words = ['hello', 'hi', 'привет', 'privet', 'ky', 'ку', 'q', 'qq', 'здарова',
               'здорова', 'здраствуй', 'здравствуйте']
goodbye_words = ['пока', 'bb', 'poka', 'bb all', 'всем пока', 'пока всем', 'bye', 'goodbye', 'bye bye', 'до скорого',
                 'до встречи', 'увидимся', 'услышимся']

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # привязать к ipv4, поскольку адреса ipv6 иногда вызывают проблемы
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # берем первый элемент плейлиста
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f'♂Billy Herrington go to the gym!♂')

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'♂Thank you sir♂')

    # @commands.command()
    # async def join(self, ctx, *, channel: discord.VoiceChannel):
    #     """Бот присоединяется к голосовому чату"""
    #
    #     if ctx.voice_client is not None:
    #         return await ctx.voice_client.move_to(channel)
    #
    #     await channel.connect()
    #     await ctx.send(f'♂ Billy Herrington go to the gym! ♂')

    @commands.command()
    async def play(self, ctx, *, query):
        """Вопроизведение локальных файлов"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send()

    @commands.command()
    async def yt(self, ctx, *, url):
        """Вопроизведение по url адресу"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Потоки с URL-адреса (такие же, как у yt, но без предварительной загрузки)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Изменяет громкость плеера"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Останавливает и отключает бота от голосового чата"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


prefix = "!"
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))


@bot.event
async def on_ready():
    print('{0} go to the gym ({0.id})'.format(bot.user))
    print('------')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Played with his dick'))


@bot.event
async def on_message(message):
    msg = message.content.lower()
    if 'ass' in message.content.lower():
        voice = get(bot.voice_clients, guild=message.guild)
        voice.play(discord.FFmpegPCMAudio("/Users/lebedevila/PycharmProjects/gachi_discordbot/sounds/Ass we can.mp3"))
        voice.is_playing()
    elif 'дела' in message.content.lower():
        await message.channel.send("♂️Ass we can♂️")
    elif 'fisting' in message.content.lower():
        voice = get(bot.voice_clients, guild=message.guild)
        voice.play(discord.FFmpegPCMAudio("/Users/lebedevila/PycharmProjects/gachi_discordbot/sounds/Our daddy told us not to be ashamed.mp3"))
        voice.is_playing()
    elif 'кабачок' in message.content.lower():
        voice = get(bot.voice_clients, guild=message.guild)
        voice.play(
            discord.FFmpegPCMAudio("/Users/lebedevila/PycharmProjects/gachi_discordbot/sounds/Fisting is 300 $.mp3"))
        voice.is_playing()
    elif msg in hello_words:
        await message.channel.send("♂️My fellow brothers! \n"
                                   "I, Billy Herrington, stand here today!♂️")
        voice = get(bot.voice_clients, guild=message.guild)
        voice.play(discord.FFmpegPCMAudio("/Users/lebedevila/PycharmProjects/gachi_discordbot/sounds/Im Billy.mp3"))
        voice.is_playing()
    elif msg in goodbye_words:
        await message.channel.send("♂️I want to see one more round!♂️")
        voice = get(bot.voice_clients, guild=message.guild)
        voice.play(discord.FFmpegPCMAudio("/Users/lebedevila/PycharmProjects/"
                                          "gachi_discordbot/sounds/i want to see 1 more round.mp3"))
        voice.is_playing()
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    pass

@bot.event
async def on_member_join(member):
    await member.send('Привет! Я Билли Хэрингтон, boss of this gym! Чтобы просмотреть команды напиши !help')

    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, добро пожаловать в ♂️GYM♂️')


@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, ♂️Oh fuck you letherman!♂️')


# отчистка сообщений
@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@bot.command()
async def инфо(ctx, arg=None):
    author = ctx.message.author
    if arg is None:
        await ctx.send(f'{author.mention} Введите:\n!инфо общая\n!инфо команды')
    elif arg == 'общая':
        await ctx.send(
            f'{author.mention} Я Билли Хэрингтон, boss of this gym! Могу интерактивно отвечать на сообщения, '
            f'воспроизводить музыку с YouTube, а также включать гачи ремиксы.')
    elif arg == 'команды':
        emb = discord.Embed(title='Навигация по командам')
        emb.add_field(name='{}join'.format(prefix),
                      value='Подключить бота к голосовому каналу')
        emb.add_field(name='{}leave'.format(prefix),
                      value='Отключить бота от голосового канала')
        emb.add_field(name='{}play + (путь к файлу)'.format(prefix),
                      value='Воспроизвести локальные файлы с компьютера')
        emb.add_field(name='{}yt + (URL видео)'.format(prefix),
                      value='Воспроизвести видео с YouTube с предварительной загрузкой')
        emb.add_field(name='{}stream + (URL видео)'.format(prefix),
                      value='Воспроизвести видео с YouTube')
        emb.add_field(name='{}volume + (значение от 1 до 200)'.format(prefix),
                      value='Регулирование громкости воспроизведения')
        emb.add_field(name='{}stop'.format(prefix),
                      value='Останавливает и отключает бота от голосового чата')
        emb.add_field(name='{}clear'.format(prefix),
                      value='Очистка чата')

        await ctx.send(embed=emb)
    else:
        await ctx.send(f'{author.mention} Такой команды нет')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        voice = get(bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("/Users/lebedevila/PycharmProjects/gachi_discordbot/sounds/fuck you....mp3"))
        voice.is_playing()
        await ctx.send(f'{ctx.author.name}, обязательно укажите число удаляемых сообщений')
    if isinstance(error, commands.CommandNotFound):
        voice = get(bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("/Users/lebedevila/PycharmProjects/gachi_discordbot/sounds/FUCK YOU.mp3"))
        voice.is_playing()
        await ctx.send(f'{ctx.author.name}, такая команда отсутсвует!')

bot.add_cog(Music(bot))
# token = open('token.txt', 'r').readline()
# bot.run(token)
bot.run(config.TOKEN)
