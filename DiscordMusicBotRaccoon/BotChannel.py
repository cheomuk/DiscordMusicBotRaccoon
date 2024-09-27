import discord
from discord.ext import commands

class BotChannel(commands.Cog):
    def __init__(self, bot, music_controls):
        self.bot = bot
        self.music_controls = music_controls

    async def update_ui(self, title: str = None):
        """음악 제목에 따라 UI 업데이트"""
        await self.music_controls.update_ui(title)

    async def send_initial_ui(self, channel):
        """봇 시작 시 초기 UI를 채널에 전송"""
        await self.music_controls.send_initial_ui(channel)

