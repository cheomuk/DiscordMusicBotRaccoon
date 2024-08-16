import discord
from discord.ext import commands

class MusicControls(discord.ui.View):
    @discord.ui.button(label="Play", style=discord.ButtonStyle.green)
    async def play_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Play 버튼 클릭 시 실행되는 코드
        await interaction.response.send_message("Play button clicked.")

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.blurple)
    async def pause_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Pause 버튼 클릭 시 실행되는 코드
        await interaction.response.send_message("Pause button clicked.")

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.blurple)
    async def resume_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Resume 버튼 클릭 시 실행되는 코드
        await interaction.response.send_message("Resume button clicked.")

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Stop 버튼 클릭 시 실행되는 코드
        await interaction.response.send_message("Stop button clicked.")

    @discord.ui.button(label="Shuffle", style=discord.ButtonStyle.secondary)
    async def shuffle_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Shuffle 버튼 클릭 시 실행되는 코드
        await interaction.response.send_message("Shuffle button clicked.")

    @discord.ui.button(label="Show Playlist", style=discord.ButtonStyle.secondary)
    async def playlist_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Show Playlist 버튼 클릭 시 실행되는 코드
        await interaction.response.send_message("Showing playlist.")