import discord
import random
import aiohttp

api_gel = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={lquery}&limit=100&json=1"

async def fetch_gelbooru_image(lquery: str):
    """Mengambil data dari Gelbooru berdasarkan tag."""
    async with aiohttp.ClientSession() as session:
        async with session.get(api_gel.format(lquery=lquery)) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("post"):
                    count = await cnt()
                    getId = random.randint(0, count)
                    return data["post"][getId]["file_url"]  # URL gambar atau video
                return None
            return None

async def fetch_gelbooru_image_pv(lquery: str):
    """Mengambil data dari Gelbooru berdasarkan tag."""
    async with aiohttp.ClientSession() as session:
        async with session.get(api_gel.format(lquery=lquery)) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("post"):
                    count = await cnt()
                    getId = random.randint(0, count)
                    return data["post"][getId]["file_url"]  # URL gambar atau video
                return None
            return None

class GelbooruView(discord.ui.View):
    def __init__(self, lquery: str):
        super().__init__()
        self.lquery = lquery

    @discord.ui.button(label="Change", style=discord.ButtonStyle.success)
    async def get_new_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        image_url = await fetch_gelbooru_image(self.lquery)
        pv_url = await fetch_gelbooru_image_pv(self.lquery)
        urlext = check_url_file_type(image_url)
        if urlext == True:
            # Update pesan dengan gambar baru
            embed = discord.Embed(title="Gelbooru Result", description=f"Tag: `{self.lquery}`", color=discord.Color.blurple())
            embed.set_image(url=image_url)
            await interaction.response.edit_message(embed=embed, view=self)
        elif urlext == False:
            embed = discord.Embed(title="Gelbooru Result", description=f"Tag: `{self.lquery}`", color=discord.Color.blurple())
            embed.add_field(name="Video", value=pv_url)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message("Tidak ditemukan hasil untuk tag ini.", ephemeral=True)

# check count in gelbooru
async def cnt():
    async with aiohttp.ClientSession() as session:
        async with session.get(api_gel.format(lquery="")) as response:
            if response.status == 200:
                json_data = await response.json(content_type=None)
                count = json_data.get('@attributes', {}).get('count')
                if count is not None:
                    count = int(count)
                    count = min(count, 99)
                return count
            else:
                print(f"Request gagal dengan status: {response.status}")
                return None
            
def check_url_file_type(urlImage):
        photo_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
        video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
        
        for ext in photo_extensions:
            if urlImage.lower().endswith(ext):
                return True
        for ext in video_extensions:
            if urlImage.lower().endswith(ext):
                return False
        return "unknown"

