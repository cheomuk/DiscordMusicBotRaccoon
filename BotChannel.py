import discord
from discord.ext import commands
from MusicControls import MusicControls
from MusicOptions import Music
from dico_token import ID

class BotChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = ID  # 메시지를 보낼 채널 ID 설정 필요
        self.music_cog = Music(bot)
        self.music_cog.set_bot_channel(self)  # MusicOptions에 BotChannel 설정
        self.view = MusicControls(bot, self.music_cog)
        self.initial_message = None

    async def send_initial_ui(self, channel):
        # 초기 UI 메시지 전송
        if self.initial_message is None:
            await self.view.update_ui()  # 초기 UI 설정
        else:
            await self.initial_message.edit(content="현재 재생 중인 노래가 없습니다.", view=self.view)

    async def update_ui(self, title):
        """ 음악이 시작될 때 UI를 업데이트합니다. """
        await self.view.update_ui(title)