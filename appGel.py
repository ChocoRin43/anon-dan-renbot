import discord
import random
import aiohttp

api_gel = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={tags}&limit=100&json=1"

async def fetch_gelbooru_image(tags: str):
    """Mengambil data dari Gelbooru berdasarkan tag."""
    async with aiohttp.ClientSession() as session:
        async with session.get(api_gel.format(tags=tags)) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("post"):
                    getId = random.randint(0, 95)
                    return data["post"][getId]["file_url"]  # URL gambar atau video
                return None
            return None
        
class GelbooruView(discord.ui.View):
    def __init__(self, tags: str):
        super().__init__()
        self.tags = tags

    @discord.ui.button(label="Get New Image", style=discord.ButtonStyle.primary)
    async def get_new_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        image_url = await fetch_gelbooru_image(self.tags)
        if image_url:
            # Update pesan dengan gambar baru
            embed = discord.Embed(title="Gelbooru Result", description=f"Tag: `{self.tags}`")
            embed.set_image(url=image_url)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("Tidak ditemukan hasil untuk tag ini.", ephemeral=True)
