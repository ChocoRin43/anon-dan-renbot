import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import os
from discord.ext import commands
import aiohttp
import random
import datetime
import traceback
import sys

api_gel = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={tags}&limit=100&json=1"

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

# Prefix untuk bot
bot = commands.Bot(command_prefix="+", intents=intents)

# Icon untuk bot (digunakan pada embed)
botIcon = discord.File("./rin.jpeg", filename="rin.jpeg")

# Fungsi untuk menulis log error
def write_log(error_message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("log.txt", "a") as log_file:
        log_file.write(f"{timestamp} {error_message}\n")

def global_error_handler(exctype, value, tb):
    error_message = f"Error global:\n{exctype.__name__}: {value}\n{''.join(traceback.format_tb(tb))}"
    write_log(error_message)

sys.excepthook = global_error_handler

@bot.event
async def on_command_error(ctx, error):
    error_message = f"Command '{ctx.command}' menyebabkan error:\n{error}\n{traceback.format_exc()}"
    write_log(error_message)
    await ctx.send("Tag yang kamu masukkan mungkin tidak valid")

@bot.event
async def on_ready():
    await bot.tree.sync()
    activity = discord.Game(name="+help | Rin Bot")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(f"Bot telah masuk sebagai {bot.user}")

@bot.tree.command(name="ping", description="Untuk melihat status ready pada bot")
async def ping(interaction: discord.Interaction):
    """
    Untuk Melihat Ping Delay Dari Bot
    """
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! 🏓 Latency: {latency} ms")

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

@bot.command()
async def gel(ctx, *, tags: str = "anime"):
    """Command untuk mengambil gambar Gelbooru berdasarkan tag."""
    view = GelbooruView(tags)
    image_url = await fetch_gelbooru_image(tags)
    if image_url:
        embed = discord.Embed(title="Gelbooru Result", description=f"Tag: `{tags}`")
        embed.set_image(url=image_url)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("Tidak ditemukan hasil untuk tag tersebut.")


@bot.tree.command(name="waifu", description="Untuk mengambil gambar dari waifu.pics")
@app_commands.choices(
    category=[
        discord.app_commands.Choice(name="SFW", value="sfw"),
        discord.app_commands.Choice(name="NSFW", value="nsfw")
    ]
)
async def waifu(interaction: discord.Interaction, category: str, image_type: str):
    """
    Perintah untuk mengambil gambar waifu dari waifu.pics
    Args:
        category (str): Kategori gambar ('sfw' atau 'nsfw')
        image_type (str): Tipe gambar ('waifu', 'neko', "shinobu", "megumin", "bully", "cuddle", "hug", "kiss")
    """

    if category not in ["sfw", "nsfw"]:
        await interaction.response.send_message("Kategori harus 'sfw' atau 'nsfw'!")
        return
    
    if image_type not in ["waifu", "trap", "neko", "shinobu", "megumin", "bully", "cuddle", "hug", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe", "blowjob"]:
        await interaction.response.send_message("Tipe gambar tidak valid! Cek daftar tipe di waifu.pics.")
        return

    url = f"https://api.waifu.pics/{category}/{image_type}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get("url")
                embed = discord.Embed(title=f"{category.upper()} {image_type.capitalize()}", color=discord.Color.fuchsia())
                embed.set_footer(text="Rin Bot | Disediakan oleh waifu.pics", icon_url="attachment://rin.jpeg")
                embed.set_image(url=image_url)
                await interaction.response.send_message(embed=embed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
            else:
                await interaction.response.send_message("Terjadi kesalahan saat mengambil gambar.")
@bot.tree.command(name="neko", description="Untuk mengambil gambar dari nekos.cat")
async def nekos(interaction: discord.Interaction, kategori: str):
    """
    Mengambil gambar dari API nekos.cat.
    :param kategori: Kategori gambar (default: catgirl).
    catgirl, foxgirl, wolf-girl, animal-ears, tail, tail-with-ribbon, tail-from-under-skirt
    cute, cuteness-is-justice, blue-archive, girl, young-girl, maid, maid-uniform, vtuber, w-sitting, lying-down, hands-forming-a-heart, wink, valentine, headphones
    thigh-high-socks, knee-high-socks, white-tights, black-tights, heterochromia, uniform, sailor-uniform, hoodie, ribbon, white-hair, blue-hair, long-hair, blonde, blue-eyes, purple-eyes
    swimwear, swimsuit, bikini, sea, swim-ring
    """
    
    if kategori not in ["catgirl", "foxgirl", "wolf-girl", "animal-ears", "tail", "tail-with-ribbon", "tail-from-under-skirtcute", "cuteness-is-justice", "blue-archive", "girl", "young-girl", "maid", "maid-uniform", "vtuber", "w-sitting", "lying-down", "hands-forming-a-heart", "wink", "valentine", "headphonesthigh-high-socks", "knee-high-socks", "white-tights", "black-tights", "heterochromia", "uniform", "sailor-uniform", "hoodie", "ribbon", "white-hair", "blue-hair", "long-hair", "blonde", "blue-eyes", "purple-eyes", "swimwear", "swimsuit", "bikini", "sea", "swim-ring"]:
        await interaction.response.send_message("Tipe gambar tidak valid! Cek daftar tipe di nekos")
        return

    url = f"https://api.nekosia.cat/api/v1/images/{kategori}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get("image", {}).get("original", {}).get("url")
                cat = data.get("category", {})
                ctgory = cat.replace("-", " ")
                if image_url:
                    bed = discord.Embed(title=f"Kategori: {ctgory}", color=discord.Color.fuchsia())
                    bed.set_footer(text="Rin Bot | Disediakan oleh nekosia.cat", icon_url="attachment://rin.jpeg")
                    bed.set_image(url=image_url)
                    await interaction.response.send_message(embed=bed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                else:
                    await interaction.response.send_message("Tidak dapat menemukan gambar untuk kategori ini.")
            else:
                await interaction.response.send_message("Terjadi kesalahan saat menghubungi API.")
                await interaction.response.send_message(f"Pesan Kesalahan{url}")

@bot.tree.command()
async def gif(interaction: discord.Interaction, kategori: str ="baka;"):
    """
    Mengambil gambar dari API nekos.best.
    :param kategori: Kategori gif (default: baka).
    baka, bite, blush, bored, cry, cuddle, dance, facepalm, feed, handhold, handshake, happy, highfive, 
    hug, kick,kiss, laugh, lurk, nod, nom, nope, pat, peck, poke, pout, punch, shoot, shrug, slap, sleep, 
    smile, smug, stare, think, thumbsup, tickle, wave, wink, yawn, yeet
    """
    
    if kategori not in ["baka", "cry", "bite", "blush", "bored", "cuddle", "dance", "facepalm", "feed", "handhold", "handshake", "happy", "highfive", "hug", "kick", "kiss", "laugh", "lurk", "nod", "nom", "nope", "pat", "peck", "poke", "pout", "punch", "shoot", "shrug", "slap", "sleep", "smile", "smug", "stare", "think", "thumbsup", "tickle", "wave", "wink", "yawn", "yeet"]:
        await interaction.response.send_message("Tipe gif tidak valid! Cek daftar tipe di nekos.best")
        return

    url = f"https://nekos.best/api/v2/{kategori}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                animeName = data["results"][0]["anime_name"]
                image_url = data["results"][0]["url"]
                if image_url:
                    bed = discord.Embed(title=f"Anime: {animeName}", color=discord.Color.fuchsia(),)
                    bed.set_footer(text="Rin Bot | Disediakan oleh nekos.cat", icon_url="attachment://rin.jpeg")
                    bed.set_image(url=image_url)
                    await interaction.response.send_message(embed=bed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                else:
                    await interaction.response.send_message("Tidak dapat menemukan gambar untuk kategori ini.")
            else:
                await interaction.response.send_message("Terjadi kesalahan saat menghubungi API.")
                await interaction.response.send_message(f"Pesan Kesalahan{url}")

@bot.tree.command(name="anime", description="Untuk mencari informasi anime dari myanimelist")
async def anime(interaction: discord.Interaction, query: str):
    """
    Mencari informasi anime dari myanimelist.
    :param query: Query pencarian anime.
    """
    api_url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                if data["data"]:
                    anime = data["data"][0]
                    imgAnime = anime["images"]["jpg"]["large_image_url"]
                    title = anime["title"]
                    synopsis = anime["synopsis"]
                    url = anime["url"]
                    embed = discord.Embed(title=title, description=synopsis, color=discord.Color.fuchsia())
                    embed.set_image(url=imgAnime)
                    embed.add_field(name="More Info", value=f"[Click here]({url})")
                    embed.set_footer(text="Rin Bot | Disediakan oleh Jikan API", icon_url="attachment://rin.jpeg")
                    await interaction.response.send_message(embed=embed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                else:
                    await interaction.response.send_message("Anime tidak ditemukan.")
            else:
                await interaction.response.send_message("Gagal mengambil data dari API.")

@bot.tree.command(name="chara", description="Untuk mencari gambar karakter anime dari gelbooru")
async def chara(interaction: discord.Interaction, query: str):
    """
    Mencari informasi karakter anime dari gelbooru.
    :param query: Query pencarian karakter.
    Untuk tagnya bisa dispasi atau bisa lihat di gelbooru sendiri
    """    
    async def cnt():
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

    lquery = query.lower()

    prvnt_tag = ["loli", "shota", "shotacon", "lolicon"]
    is_prvnt = any(qr in query.lower() for qr in prvnt_tag)

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

    urlg = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={lquery}&limit=100&json=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(urlg) as response:
            if response.status == 200 and is_prvnt:
                await interaction.response.send_message("Dikarenakan discord memiliki peraturan yang sangat ketat, kami tidak toleransi dengan tag tersebut", delete_after=5)
                try:
                    await interaction.delete()
                except discord.Forbidden:
                    await interaction.response.send_message("Bot tidak memiliki izin untuk menghapus pesan.")
                except discord.HTTPException as e:
                    await interaction.response.send_message(f"Terjadi error: {e}")
            elif response.status == 200 and isinstance(interaction.channel, discord.TextChannel) and interaction.channel.is_nsfw():
                data = await response.json()
                if data:
                    count = await cnt()
                    randomwaifu = random.randint(0, count)
                    chara = data["post"][randomwaifu]
                    imgChara = chara["file_url"]
                    pvImg = chara["preview_url"]
                    name = query.replace("+", " ").replace("_", " ")
                    sc = chara["source"]
                    photoext = check_url_file_type(imgChara)
                    if photoext == True:
                        embed = discord.Embed(title=name, color=discord.Color.fuchsia())
                        embed.set_image(url=imgChara)
                        embed.add_field(name="Source", value=f"[Click here]({sc})")
                        embed.set_footer(text="Rin Bot | Disediakan oleh Gelbooru", icon_url="attachment://rin.jpeg")
                        await interaction.response.send_message(embed=embed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                    elif photoext == False:
                        embed = discord.Embed(title=name, description="File tersebut video, jika ingin menonton silahkan pergi ke sumbernya", color=discord.Color.fuchsia())
                        embed.set_image(url=pvImg)
                        embed.add_field(name="Source", value=f"[Click here]({sc})")
                        embed.set_footer(text="Rin Bot | Disediakan oleh Gelbooru", icon_url="attachment://rin.jpeg")
                        await interaction.response.send_message(embed=embed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                    else:
                        await interaction.response.send_message("Tidak dapat menemukan gambar untuk tag tersebut.")
            elif response.status == 200:
                await interaction.response.send_message("Dikarenakan discord memiliki peraturan yang sangat ketat, kami tidak toleransi dengan tag tersebut", delete_after=5)
            else:
                await interaction.response.send_message("Sepertinya ada yang salah")
                raise Exception(f"Error {response.status}: Failed to fetch data")

@bot.tree.command(name="talita", description="Cobain aja")
async def talita(interaction: discord.Interaction):
    await interaction.response.send_message("Talita punya nya Rehan")

@bot.tree.command(name="dadu", description="Untuk mengkocok dadu")
async def dadu(interaction: discord.Interaction):
    """
    Mengkocok dadu 1 sampai 6.
    """
    dadu = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 Angka dadu: {dadu} 🎲")

@bot.tree.command(name= "membercount", description="Untuk melihat jumlah member di server")
async def membercount(interaction: discord.Interaction):
    """
    Menampilkan jumlah member di server.
    """
    member_count = interaction.guild.member_count
    await interaction.response.send_message(f"Jumlah anggota di server ini: {member_count}")

@bot.tree.command(name="kick", description="Untuk mengeluarkan anggota dari server")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
    """
    Kick seorang anggota dari server.
    :param member: Anggota yang akan di-kick.
    :param reason: Alasan kick (opsional).
    """
    await interaction.response.send_message(f'{member.mention} telah di-kick dari server. Alasan: {reason}')
    await member.kick(reason=reason)

@bot.tree.command(name="ban", description="Untuk mem-ban anggota dari server")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
    """
    Ban seorang anggota dari server.
    :param member: Anggota yang akan di-ban.
    :param reason: Alasan ban (opsional).
    """
    await interaction.response.send_message(f'{member.mention} telah di-ban dari server. Alasan: {reason}')
    await member.ban(reason=reason)

bot.run(DISCORD_BOT_TOKEN)
