import discord
from discord.ext import commands
import aiohttp

# Masukkan token bot Anda
DISCORD_BOT_TOKEN = "Masukan bot token mu"

intents = discord.Intents.default()
intents.message_content = True  # Aktifkan intent untuk membaca isi pesan
intents.members = True

# Prefix untuk bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot telah masuk sebagai {bot.user}")

@bot.command()
async def ping(ctx):
    """
    Untuk Melihat Ping Delay Dari Bot
    """
    latency = round(bot.latency * 1000)  # Latensi dalam milidetik
    await ctx.send(f"Pong! 🏓 Latency: {latency} ms")

# Command untuk mendapatkan gambar waifu
@bot.command()
async def waifu(ctx, category: str = "sfw", image_type: str = "waifu"):
    """
    Perintah untuk mengambil gambar waifu dari waifu.pics
    Args:
        category (str): Kategori gambar ('sfw' atau 'nsfw')
        image_type (str): Tipe gambar ('waifu', 'neko', dll.)
    """
    # Validasi input
    if category not in ["sfw", "nsfw"]:
        await ctx.send("Kategori harus 'sfw' atau 'nsfw'!")
        return
    
    if image_type not in ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "hug", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe"]:
        await ctx.send("Tipe gambar tidak valid! Cek daftar tipe di waifu.pics.")
        return

    url = f"https://api.waifu.pics/{category}/{image_type}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get("url")
                embed = discord.Embed(title=f"{category.upper()} {image_type.capitalize()}", color=discord.Color.fuchsia())
                embed.set_image(url=image_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Terjadi kesalahan saat mengambil gambar.")
@bot.command()
async def nekos(ctx, kategori: str = "waifu"):
    """
    Mengambil gambar dari API nekos.cat.
    :param kategori: Kategori gambar (default: waifu).
    """
    valid_kategori = ["waifu", "neko", "kitsune", "shinobu", "megumin", "maid", "cat", "catgirl", "blue-archive", "young-girl", "uniform", "sailor-uniform"]
    if kategori not in valid_kategori:
        await ctx.send(f"Kategori tidak valid. Coba salah satu dari: {', '.join(valid_kategori)}")
        return

    url = f"https://api.nekosia.cat/api/v1/images/{kategori}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data.get("image", {}).get("original", {}).get("url")
                cat = data.get("category", {})
                if image_url:
                    bed = discord.Embed(title=f"Kategori: {cat}", color=discord.Color.fuchsia())
                    bed.set_image(url=image_url)
                    await ctx.send(embed=bed)
                else:
                    await ctx.send("Tidak dapat menemukan gambar untuk kategori ini.")
            else:
                await ctx.send("Terjadi kesalahan saat menghubungi API.")

@bot.command()
async def talitha(ctx):
    await ctx.send("Talitha punya nya Rehan")

# Command untuk melihat jumlah member
@bot.command()
async def membercount(ctx):
    """
    Menampilkan jumlah member di server.
    """
    member_count = ctx.guild.member_count  # Mendapatkan jumlah member
    await ctx.send(f"Jumlah anggota di server ini: {member_count}")

# Command untuk kick user
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason=None):
    """
    Kick anggota dari server.
    """
    try:
        await user.kick(reason=reason)
        await ctx.send(f"{user} telah di-kick dari server. Alasan: {reason if reason else 'Tidak ada alasan diberikan.'}")
    except discord.Forbidden:
        await ctx.send("Bot tidak memiliki izin untuk kick user ini.")
    except discord.HTTPException:
        await ctx.send("Terjadi kesalahan saat mencoba kick user.")

# Command untuk ban user
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason=None):
    """
    Ban anggota dari server.
    """
    try:
        await user.ban(reason=reason)
        await ctx.send(f"{user} telah di-ban dari server. Alasan: {reason if reason else 'Tidak ada alasan diberikan.'}")
    except discord.Forbidden:
        await ctx.send("Bot tidak memiliki izin untuk ban user ini.")
    except discord.HTTPException:
        await ctx.send("Terjadi kesalahan saat mencoba ban user.")

# Error handler untuk memberikan pesan yang jelas jika user tidak memiliki izin
@ban.error
@kick.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Anda tidak memiliki izin untuk melakukan tindakan ini.")

# Menjalankan bot
bot.run(DISCORD_BOT_TOKEN)
