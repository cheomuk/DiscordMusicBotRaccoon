import discord
from discord.ext import commands
from YTDLSource import YTDLSource
import random


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist = []  # 플레이리스트를 저장할 리스트
        self.current_song_index = 0  # 현재 재생 중인 노래의 인덱스
        self.repeat = False  # 반복 재생 플래그
        self.playlist_message = None  # 플레이리스트 메시지를 저장할 변수
        self.bot_channel = None  # BotChannel 참조를 저장할 변수
        
    def set_bot_channel(self, bot_channel):
        self.bot_channel = bot_channel

    @commands.command(name='j')
    async def join(self, ctx):
        """ 채널에 입장합니다. """
        
        channel = ctx.author.voice.channel

        if ctx.author.voice is None:
            return await ctx.send("음성 채널에 먼저 연결되어야 합니다.", delete_after=5)

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        self.playlist.clear()
        await channel.connect()


    @commands.command(name='p')
    async def play(self, ctx, *, url):
        """ 유튜브 링크를 재생합니다. """
        
        # 봇이 음성 채널에 연결되어 있지 않으면 자동으로 연결
        if ctx.voice_client is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.send("봇이 음성 채널에 연결되어 있지 않으며, 당신도 음성 채널에 연결되어 있지 않습니다.", delete_after=5)
                return

        # 재생 목록 URL인지 확인 (이중 확인)
        if "playlist" in url or "list=" in url:
            await ctx.send("재생 목록 URL은 지원되지 않습니다. 개별 영상을 사용해주세요.", delete_after=10)
            return

        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                self.playlist.append(player)  # 플레이리스트에 추가

                # 플레이리스트에 추가된 곡이 하나밖에 없을 때만 새 곡을 재생
                if len(self.playlist) == 1:
                    await self.start_playing(ctx)
                else:
                    await ctx.send(f'Added to the playlist: {player.title}', delete_after=5)
            except Exception as e:
                await ctx.send(f"음악을 재생하는 데 실패했습니다: {str(e)}", delete_after=5)

    async def start_playing(self, ctx):
        """ 플레이 리스트에 있는 곡을 재생합니다. """
        if self.playlist:
            player = self.playlist[self.current_song_index]
            ctx.voice_client.play(player, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            
            if self.bot_channel:
                await self.bot_channel.update_ui(player.title)
            await ctx.send(f'Now playing: {player.title}', delete_after=5)
        else:
            if self.bot_channel:
                await self.bot_channel.update_ui("현재 재생 중인 곡이 없습니다.")


    async def play_next(self, ctx):
        """ 다음 곡 재생 """
        if self.repeat and ctx.voice_client and ctx.voice_client.is_playing():
            # 현재 곡 반복 재생
            current_player = ctx.voice_client.source
            ctx.voice_client.play(current_player, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            return
        
        # 현재 재생 중인 곡을 플레이리스트에서 제거
        if self.playlist:
            self.playlist.pop(self.current_song_index)

        # 다음 곡 재생 또는 플레이리스트 끝
        if self.current_song_index < len(self.playlist):
            await self.start_playing(ctx)
        else:
            self.current_song_index = 0  # 플레이리스트가 끝나면 처음으로 돌아감
            self.playlist.clear()  # 플레이리스트 초기화
            if self.bot_channel:
                await self.bot_channel.update_ui("현재 재생 중인 곡이 없습니다.")

    @commands.command(name='b')
    async def previous(self, ctx):
        """ 이전 곡으로 재생합니다 """
        if not await self.ensure_voice(ctx):
            return
        
        await self.play_previous(ctx)

    async def play_previous(self, ctx):
        if self.current_song_index > 0:
            self.current_song_index -= 1
            await self.start_playing(ctx)
        else:
            await ctx.send("이전 곡이 없습니다.", delete_after=5)

    @commands.command(name='r')
    async def repeat(self, ctx):
        """ 반복 재생 모드 """
        if not await self.ensure_voice(ctx):
            return
        
        if not self.playlist:
            await ctx.send("플레이리스트가 비어 있습니다. 반복 재생 모드를 활성화할 수 없습니다.", delete_after=5)
            return
        
        self.repeat = not self.repeat
        mode = "enabled" if self.repeat else "disabled"
        await ctx.send(f'Repeat mode is now {mode}.', delete_after=5)

    @commands.command(name='sh')
    async def shuffle(self, ctx):
        """ 셔플 기능을 제공합니다. """
        if not await self.ensure_voice(ctx):
            return
        
        if not self.playlist:
            return await ctx.send("플레이리스트가 비어 있습니다.", delete_after=5)

        random.shuffle(self.playlist)  # 플레이리스트 셔플
        self.current_song_index = 0  # 인덱스 초기화
        
        await ctx.send("플레이리스트가 셔플되었습니다.", delete_after=5)

    @commands.command(name='s')
    async def skip(self, ctx):
        """ 현재 곡을 스킵합니다. 마지막 곡이면 스킵하지 않습니다. """     
        if not await self.ensure_voice(ctx):
            return
        
        # 현재 곡이 마지막 곡인지 확인
        if self.current_song_index >= len(self.playlist) - 1:
            await ctx.send("현재 곡이 마지막 곡이므로 스킵할 수 없습니다.", delete_after=5)
            return
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("다음 곡으로 넘어갑니다.", delete_after=5)
        else:
            await ctx.send("현재 재생 중인 곡이 없습니다.", delete_after=5)

    @commands.command(name='v')
    async def volume(self, ctx, volume: int):
        """ 볼륨을 조절합니다. """
        if not await self.ensure_voice(ctx):
            return
        
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.", delete_after=5)

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%", delete_after=5)

    @commands.command(name='x')
    async def exit(self, ctx):
        """ 음성채팅방을 나갑니다. """
        if not await self.ensure_voice(ctx):
            return
        
        self.playlist.clear()  # 플레이리스트 초기화
        await ctx.voice_client.disconnect()
        await ctx.send("음성 채널에서 연결이 끊겼습니다.", delete_after=5)

    @commands.command(name='ps')
    async def pause(self, ctx):
        """ 음악을 일시정지 할 수 있습니다. """
        if not await self.ensure_voice(ctx):
            return
        
        if ctx.voice_client.is_paused() or not ctx.voice_client.is_playing():
            await ctx.send("음악이 이미 일시 정지 중이거나 재생 중이지 않습니다.", delete_after=5)
            return

        ctx.voice_client.pause()
        await ctx.send("음악이 일시 정지되었습니다.", delete_after=5)

    @commands.command(name='rs')
    async def resume(self, ctx):
        """ 일시정지된 음악을 다시 재생할 수 있습니다. """
        if not await self.ensure_voice(ctx):
            return
        
        if ctx.voice_client.is_playing() or not ctx.voice_client.is_paused():
            await ctx.send("음악이 이미 재생 중이거나 재생할 음악이 존재하지 않습니다.", delete_after=5)
            return

        ctx.voice_client.resume()
        await ctx.send("음악이 다시 재생되었습니다.", delete_after=5)
        
    @commands.command(name='pl')
    async def playlist(self, ctx):
        """ 플레이리스트 내역을 보여줍니다. """
        if not await self.ensure_voice(ctx):
            return
        
        if not self.playlist:
            self.playlist_message = await ctx.send("현재 플레이리스트가 비어 있습니다.", delete_after=5)
        else:
            playlist_titles = [f"{index + 1}. {song.title}" for index, song in enumerate(self.playlist)]
            playlist_message = "Now Playlist:\n" + "\n".join(playlist_titles)
            
            self.playlist_message = await ctx.send(playlist_message, delete_after=10)
            
    @commands.command(name='e')
    async def remove_song(self, ctx, index: int):
        """ 플레이리스트에서 특정 곡을 삭제합니다. """
        if index < 1 or index > len(self.playlist):
            await ctx.send("유효하지 않은 번호입니다. 올바른 번호를 입력해주세요.", delete_after=5)
            return
        
        # 플레이리스트에서 해당 곡을 삭제
        removed_song = self.playlist.pop(index - 1)

        await ctx.send(f"플레이리스트에서 '{removed_song.title}'이(가) 삭제되었습니다.", delete_after=5)

        # 현재 재생 중인 곡의 인덱스를 조정
        if index - 1 < self.current_song_index:
            self.current_song_index -= 1

        # 플레이리스트를 다시 보여줌
        await self.playlist(ctx)
        
    @commands.command(name='m')
    async def move_song(self, ctx, song_index: int, new_position: int):
        """플레이리스트에서 특정 곡을 원하는 위치로 이동시킵니다."""
        await self.move_song_by_index(ctx, song_index, new_position)

    async def move_song_by_index(self, ctx, song_index: int, new_position: int):
        """플레이리스트에서 특정 인덱스의 곡을 원하는 위치로 이동합니다."""
        if song_index < 1 or song_index > len(self.playlist):
            await ctx.send("유효하지 않은 곡 번호입니다. 올바른 번호를 입력해주세요.", delete_after=5)
            return

        if new_position < 1 or new_position > len(self.playlist):
            await ctx.send("유효하지 않은 위치입니다. 올바른 위치를 입력해주세요.", delete_after=5)
            return

        # 곡을 리스트에서 제거하고 새로운 위치에 삽입
        song = self.playlist.pop(song_index - 1)
        self.playlist.insert(new_position - 1, song)

        await ctx.send(f"'{song.title}'이(가) {new_position}번째 위치로 이동되었습니다.", delete_after=5)

        # 현재 재생 중인 곡의 인덱스를 조정
        if song_index - 1 == self.current_song_index:
            self.current_song_index = new_position - 1
        elif song_index - 1 < self.current_song_index <= new_position - 1:
            self.current_song_index -= 1
        elif new_position - 1 <= self.current_song_index < song_index - 1:
            self.current_song_index += 1
                
    @commands.command(name='h')
    async def help_command(self, ctx):
        """ 명령어 목록을 표시합니다. """
        help_text = """
        **명령어 목록:**
        > `>p <url>`: 유튜브 링크를 재생합니다.
        > `>j`: 봇을 음성 채널에 참여시킵니다.
        > `>b`: 이전 음악으로 돌아갑니다.
        > `>ps`: 음악을 일시정지합니다.
        > `>rs`: 음악 재생을 재개합니다.
        > `>s`: 현재 곡을 스킵합니다.
        > `>r`: 반복 재생 모드를 전환합니다.
        > `>e <Playlist 번호>`: Playlist 내 음악을 삭제합니다.
        > `>m <현재 Playlist 번호> <옮기고 싶은 순서 번호>`: 원하는 순번으로 이동시킵니다.
        > `>sh`: 플레이리스트를 셔플합니다.
        > `>pl`: 현재 플레이리스트를 보여줍니다.
        > `>v 0~100`: 볼륨을 조절합니다.
        > `>x`: 음성 채널에서 봇을 나가게 합니다.
        """
        await ctx.send(help_text, delete_after=30)

    @play.before_invoke
    async def play_ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                self.playlist.clear()
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.", delete_after=5)
                raise commands.CommandError("Author not connected to a voice channel.")
            
    async def ensure_voice(self, ctx):
        """ 봇이 음성 채널에 연결되어 있는지 확인합니다. """
        if ctx.voice_client is None:
            await ctx.send("봇이 음성 채널에 연결되어 있지 않습니다. 먼저 봇을 채널에 연결해주세요.", delete_after=5)
            return False
        return True
            
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        """ 모든 명령어가 실행된 후 메시지를 삭제합니다. """
        await self.delete_user_message(ctx)
        
    async def delete_user_message(self, ctx, delay: int = 5):
        """ 사용자 메시지를 일정 시간 후에 삭제합니다. """
        await ctx.message.delete(delay=delay)

            
            

        
        