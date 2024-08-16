﻿import discord
from discord.ext import commands

from MusicControls import MusicControls
import YTDLSource

# 음악 재생 클래스. 커맨드 포함.
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        
        channel = ctx.author.voice.channel
 
        if ctx.author.voice is None:
            return await ctx.send("음성 채널에 먼저 연결되어야 합니다.")
 
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
 
        await channel.connect()
 
   
    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
 
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
 
        await ctx.send(f'Now playing: {player.title}')
 
    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
 
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
 
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
 
    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
 
        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def pause(self, ctx):
        ''' 음악을 일시정지 할 수 있습니다. '''
 
        if ctx.voice_client.is_paused() or not ctx.voice_client.is_playing():
            await ctx.send("음악이 이미 일시 정지 중이거나 재생 중이지 않습니다.")
            
        ctx.voice_client.pause()
            
    @commands.command()
    async def resume(self, ctx):
        ''' 일시정지된 음악을 다시 재생할 수 있습니다. '''
 
        if ctx.voice_client.is_playing() or not ctx.voice_client.is_paused():
            await ctx.send("음악이 이미 재생 중이거나 재생할 음악이 존재하지 않습니다.")
            
        ctx.voice_client.resume()
 
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
            
    @commands.command()
    async def music_controls(self, ctx):
        """Displays music control buttons"""
        view = MusicControls()
        await ctx.send("Music Controls:", view=view)