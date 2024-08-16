import discord
from discord.ext import commands
from MusicOptions import Music

class MusicControls(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.music_cog = self.bot.get_cog("Music")  # Music 클래스 인스턴스 가져오기

    async def update_ui(self, title, thumbnail):
        self.title = title
        self.thumbnail = thumbnail
        # UI 업데이트 로직
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = False  # 버튼 활성화 예시

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.blurple)
    async def pause_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Pause 버튼 클릭 시 실행되는 코드
        await self.music_cog.pause(interaction)
        await interaction.response.send_message("음악이 일시 정지되었습니다.")

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.blurple)
    async def resume_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Resume 버튼 클릭 시 실행되는 코드
        await self.music_cog.resume(interaction)
        await interaction.response.send_message("음악이 재생되었습니다.")
        
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.green)
    async def skip_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Skip 버튼 클릭 시 실행되는 코드
        await self.music_cog.skip(interaction)
        await interaction.response.send_message("현재 곡이 건너뛰어졌습니다.")
        
    @discord.ui.button(label="Repeat", style=discord.ButtonStyle.primary)
    async def repeat_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Toggle repeat mode."""
        self.music_cog.repeat = not self.music_cog.repeat
        mode = "활성화" if self.music_cog.repeat else "비활성화"
        await interaction.response.send_message(f"반복 재생 모드가 {mode}되었습니다.")

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def exit_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # exit 버튼 클릭 시 실행되는 코드
        await self.music_cog.exit(interaction)
        await interaction.response.send_message("음악이 중지되고, 봇이 음성 채널에서 나갔습니다.")

    @discord.ui.button(label="Shuffle", style=discord.ButtonStyle.secondary)
    async def shuffle_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Shuffle 버튼 클릭 시 실행되는 코드
        await self.music_cog.shuffle(interaction)
        await interaction.response.send_message("플레이리스트가 셔플되었습니다.")

    @discord.ui.button(label="Show Playlist", style=discord.ButtonStyle.secondary)
    async def playlist_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Show Playlist 버튼 클릭 시 실행되는 코드
        playlist = self.music_cog.playlist  # 현재 플레이리스트 가져오기
        if not playlist:
            await interaction.response.send_message("현재 플레이리스트가 비어 있습니다.")
        else:
            playlist_titles = [song.title for song in playlist]
            await interaction.response.send_message("현재 플레이리스트:\n" + "\n".join(playlist_titles))
