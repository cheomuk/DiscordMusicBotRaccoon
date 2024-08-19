import discord
from discord.ext import commands
from dico_token import ID

class MusicControls(discord.ui.View):
    def __init__(self, bot, music_cog):
        super().__init__(timeout=None)
        self.bot = bot
        self.music_cog = music_cog
        self.message = None

    async def update_ui(self, title: str = None):
        """UI를 현재 재생 중인 음악의 제목과 썸네일로 업데이트"""
        embed = discord.Embed(
            title=title if title else "현재 재생 중인 곡이 없습니다.",
            color=discord.Color.blue()
        )

        if self.message:
            await self.message.edit(embed=embed, view=self)
        else:
            channel = self.bot.get_channel(self.music_cog.channel_id)
            self.message = await channel.send(embed=embed, view=self)

    async def send_initial_ui(self, channel):
        """초기 UI 전송"""
        embed = discord.Embed(
            title="Ready to play music.",
            color=discord.Color.blue()
        )
        self.message = await channel.send(embed=embed, view=self)

    async def execute_command(self, interaction: discord.Interaction, command_name: str):
        command = self.bot.get_command(command_name)
        if command:
            ctx = await self.bot.get_context(interaction.message)
            ctx.interaction = interaction
            response_message = await ctx.invoke(command)
            if response_message:
                await response_message.delete(delay=5)  # 응답 메시지를 5초 후에 삭제
        else:
            await interaction.response.send_message(f"Command `{command_name}` not found.", ephemeral=True)

    @discord.ui.button(label="스킵", emoji="⏩", style=discord.ButtonStyle.secondary)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_command(interaction, "s")

    @discord.ui.button(label="일시 정지", emoji="⏸️", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_command(interaction, "ps")

    @discord.ui.button(label="재생", emoji="▶️", style=discord.ButtonStyle.secondary)
    async def resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_command(interaction, "rs")
        
    @discord.ui.button(label="반복 재생", emoji="🔁", style=discord.ButtonStyle.secondary)
    async def repeat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_command(interaction, "r")
        
    @discord.ui.button(label="이전 재생", emoji="⏮️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_command(interaction, "b")

    @discord.ui.button(label="셔플", emoji="🔀", style=discord.ButtonStyle.secondary)
    async def shuffle(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_command(interaction, "sh")
        
    @discord.ui.button(label="Playlist", emoji="📜", style=discord.ButtonStyle.secondary)
    async def playlist(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.execute_command(interaction, "pl")
        
    @discord.ui.button(label="Help", emoji="❓", style=discord.ButtonStyle.secondary)
    async def help_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execute_command(interaction, "h")