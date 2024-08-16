import discord
from discord.ext import commands, tasks
from MusicControls import MusicControls

class BotChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = 1273905184841400351  # 메시지를 보낼 채널 ID
        self.view = MusicControls(bot)  # MusicControls 인스턴스 생성
        self.initial_message = None  # 초기 메시지를 저장할 변수

    async def send_initial_ui(self, channel):
        # 초기 UI 메시지 전송
        self.initial_message = await channel.send("현재 재생 중인 노래가 없습니다.", view=self.view)

    async def update_ui(self, title, thumbnail):
        # UI 업데이트 메서드
        if self.initial_message:
            embed = discord.Embed(title=title)
            embed.set_thumbnail(url=thumbnail)
            await self.initial_message.edit(embed=embed, view=self.view)

    async def reset_ui(self):
        # UI 초기화 메서드
        if self.initial_message:
            await self.initial_message.edit(content="현재 재생 중인 노래가 없습니다.", embed=None, view=self.view)

    @commands.command()
    async def play(self, ctx, song):
        # 음악 재생 로직
        await self.send_initial_ui(ctx.channel)  # 최초 UI 전송
        self.view.update_ui(title=song['title'], thumbnail=song['thumbnail'])  # UI 업데이트

    @commands.command()
    async def stop(self, ctx):
        # 음악 정지 로직
        await self.reset_ui()  # UI 초기화