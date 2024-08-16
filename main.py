import asyncio

import discord

from BotChannel import BotChannel
from discord.ext import commands
from dico_token import Token
from MusicOptions import Music
 
intents = discord.Intents.default()
intents.message_content = True
 
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(">"),
    description='Relatively simple music bot example',
    intents=intents,
)
 
 
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    # 봇이 준비되었을 때 특정 채널에 UI를 전송
    channel = bot.get_channel(1273905184841400351)  # 채널 ID 입력
    if channel:
        my_bot = BotChannel(bot)  # BotChannel 인스턴스 생성
        await my_bot.send_initial_ui(channel)  # 초기 UI 전송
 
 
async def main():
    async with bot:
        await bot.add_cog(BotChannel(bot))
        await bot.start(Token)
 
 
asyncio.run(main())