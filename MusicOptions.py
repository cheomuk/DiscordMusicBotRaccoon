import discord
from discord.ext import commands


import YTDLSource
import random


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist = []  # 플레이리스트를 저장할 리스트
        self.current_song_index = 0  # 현재 재생 중인 노래의 인덱스

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        
        channel = ctx.author.voice.channel

        if ctx.author.voice is None:
            return await ctx.send("음성 채널에 먼저 연결되어야 합니다.")

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        self.playlist.clear()
        await channel.connect()


    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            self.playlist.append(player)  # 플레이리스트에 추가

            if not ctx.voice_client.is_playing():
                ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
            await ctx.send(f'Now playing: {player.title}')

    def play_next(self, ctx):
        """ 다음 곡 재생 """
        
        self.current_song_index += 1
        
        if self.current_song_index < len(self.playlist):
            next_song = self.playlist[self.current_song_index]
            ctx.voice_client.play(next_song, after=lambda e: self.play_next(ctx))
            self.bot.loop.create_task(ctx.send(f'Now playing: {next_song.title}'))
        else:
            self.current_song_index = 0  # 플레이리스트가 끝나면 처음으로 돌아감
            self.playlist.clear()   # 플레이리스트 초기화

    @commands.command()
    async def shuffle(self, ctx):
        """ 셔플 기능을 제공합니다. """
        
        if not self.playlist:
            return await ctx.send("플레이리스트가 비어 있습니다.")

        random.shuffle(self.playlist)  # 플레이리스트 셔플
        self.current_song_index = 0  # 인덱스 초기화
        
        await ctx.send("플레이리스트가 셔플되었습니다.")

    @commands.command()
    async def skip(self, ctx):
        """ 다음 곡으로 넘어갑니다. """
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("다음 곡으로 넘어갑니다.")
        else:
            await ctx.send("현재 재생 중인 곡이 없습니다.")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def exit(self, ctx):
        """Exit and disconnects the bot from voice"""
        
        self.playlist.clear()  # 플레이리스트 초기화
        await ctx.voice_client.disconnect()

    @commands.command()
    async def pause(self, ctx):
        ''' 음악을 일시정지 할 수 있습니다. '''
        
        if ctx.voice_client.is_paused() or not ctx.voice_client.is_playing():
            await ctx.send("음악이 이미 일시 정지 중이거나 재생 중이지 않습니다.")
            return

        ctx.voice_client.pause()
        await ctx.send("음악이 일시 정지되었습니다.")

    @commands.command()
    async def resume(self, ctx):
        ''' 일시정지된 음악을 다시 재생할 수 있습니다. '''
        
        if ctx.voice_client.is_playing() or not ctx.voice_client.is_paused():
            await ctx.send("음악이 이미 재생 중이거나 재생할 음악이 존재하지 않습니다.")
            return

        ctx.voice_client.resume()
        await ctx.send("음악이 다시 재생되었습니다.")

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        
        