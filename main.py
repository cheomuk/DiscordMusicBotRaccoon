import asyncio

import discord


from discord.ext import commands
from dico_token import Token
from MusicOptions import Music
 
intents = discord.Intents.default()
intents.message_content = True
 
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!!!"),
    description='Relatively simple music bot example',
    intents=intents,
)
 
 
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
 
 
async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(Token)
 
 
asyncio.run(main())