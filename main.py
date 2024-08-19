import asyncio
import discord

from BotChannel import BotChannel
from discord.ext import commands
from dico_token import Token
from dico_token import ID
from MusicOptions import Music
from MusicControls import MusicControls

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
    channel = bot.get_channel(ID)
    if channel:
        await channel.purge()
        bot_channel_cog = bot.get_cog('BotChannel')
        if bot_channel_cog:
            await bot_channel_cog.send_initial_ui(channel)

async def main():
    async with bot:
        music_cog = Music(bot)
        await bot.add_cog(music_cog)

        music_controls = MusicControls(bot, music_cog)
        await bot.add_cog(BotChannel(bot, music_controls))

        await bot.start(Token)

asyncio.run(main())



