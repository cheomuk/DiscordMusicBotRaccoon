import asyncio

import discord

from BotChannel import BotChannel
from discord.ext import commands
from dico_token import Token
from dico_token import ID
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
    channel = bot.get_channel(ID)  # 채널 ID 입력
    if channel:
        await channel.purge()
        bot_channel_cog = bot.get_cog('BotChannel')  # 이미 등록된 Cog에서 가져오기
        if bot_channel_cog:
            await bot_channel_cog.send_initial_ui(channel)  # 초기 UI 전송
 
 
async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(BotChannel(bot))
        await bot.start(Token)
 
 
asyncio.run(main())