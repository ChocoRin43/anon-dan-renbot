import discord
from discord.ext import commands
import aiohttp
import random

DISCORD_BOT_TOKEN = "" #masukan bot token mu

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

# Prefix untuk bot
bot = commands.Bot(command_prefix="+", intents=intents)

# Icon untuk bot (digunakan pada embed)
botIcon = discord.File("./rin.jpeg", filename="rin.jpeg")

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

# Command untuk mendapatkan gambar dari waifu.pics
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
    
    if image_type not in ["waifu", "trap", "neko", "shinobu", "megumin", "bully", "cuddle", "hug", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe", "blowjob"]:
        await ctx.send("Tipe gambar tidak valid! Cek daftar tipe di waifu.pics.")
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
                await ctx.send(embed=embed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
            else:
                await ctx.send("Terjadi kesalahan saat mengambil gambar.")
@bot.command()
async def nekos(ctx, kategori: str ="catgirl;"):
    """
    Mengambil gambar dari API nekos.cat.
    :param kategori: Kategori gambar (default: catgirl).
    catgirl, foxgirl, wolf-girl, animal-ears, tail, tail-with-ribbon, tail-from-under-skirt
    cute, cuteness-is-justice, blue-archive, girl, young-girl, maid, maid-uniform, vtuber, w-sitting, lying-down, hands-forming-a-heart, wink, valentine, headphones
    thigh-high-socks, knee-high-socks, white-tights, black-tights, heterochromia, uniform, sailor-uniform, hoodie, ribbon, white-hair, blue-hair, long-hair, blonde, blue-eyes, purple-eyes
    swimwear, swimsuit, bikini, sea, swim-ring
    """
    
    if kategori not in ["catgirl", "foxgirl", "wolf-girl", "animal-ears", "tail", "tail-with-ribbon", "tail-from-under-skirtcute", "cuteness-is-justice", "blue-archive", "girl", "young-girl", "maid", "maid-uniform", "vtuber", "w-sitting", "lying-down", "hands-forming-a-heart", "wink", "valentine", "headphonesthigh-high-socks", "knee-high-socks", "white-tights", "black-tights", "heterochromia", "uniform", "sailor-uniform", "hoodie", "ribbon", "white-hair", "blue-hair", "long-hair", "blonde", "blue-eyes", "purple-eyes", "swimwear", "swimsuit", "bikini", "sea", "swim-ring"]:
        await ctx.send("Tipe gambar tidak valid! Cek daftar tipe di nekos")
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
                    bed.set_footer(text="Rin Bot | Disediakan oleh nekosia.cat", icon_url="attachment://rin.jpeg")
                    bed.set_image(url=image_url)
                    await ctx.send(embed=bed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                else:
                    await ctx.send("Tidak dapat menemukan gambar untuk kategori ini.")
            else:
                await ctx.send("Terjadi kesalahan saat menghubungi API.")
                await ctx.send(f"Pesan Kesalahan{url}")

@bot.command()
async def gif(ctx, kategori: str ="baka;"):
    """
    Mengambil gambar dari API nekos.best.
    :param kategori: Kategori gif (default: baka).
    baka, bite, blush, bored, cry, cuddle, dance, facepalm, feed, handhold, handshake, happy, highfive, 
    hug, kick,kiss, laugh, lurk, nod, nom, nope, pat, peck, poke, pout, punch, shoot, shrug, slap, sleep, 
    smile, smug, stare, think, thumbsup, tickle, wave, wink, yawn, yeet
    """
    
    if kategori not in ["baka", "cry", "bite", "blush", "bored", "cuddle", "dance", "facepalm", "feed", "handhold", "handshake", "happy", "highfive", "hug", "kick", "kiss", "laugh", "lurk", "nod", "nom", "nope", "pat", "peck", "poke", "pout", "punch", "shoot", "shrug", "slap", "sleep", "smile", "smug", "stare", "think", "thumbsup", "tickle", "wave", "wink", "yawn", "yeet"]:
        await ctx.send("Tipe gif tidak valid! Cek daftar tipe di nekos.best")
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
                    await ctx.send(embed=bed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                else:
                    await ctx.send("Tidak dapat menemukan gambar untuk kategori ini.")
            else:
                await ctx.send("Terjadi kesalahan saat menghubungi API.")
                await ctx.send(f"Pesan Kesalahan{url}")

@bot.command()
async def anime(ctx, query: str):
    """
    Mencari informasi anime dari API Jikan.
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
                    await ctx.send(embed=embed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                else:
                    await ctx.send("Anime tidak ditemukan.")
            else:
                await ctx.send("Gagal mengambil data dari API.")

@bot.command()
async def chara(ctx, query: str):
    """
    Mencari informasi karakter anime dari gelbooru.
    :param query: Query pencarian karakter.
    """
    url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={query}&limit=5&json=1&api_key=3acf790b11d7e62273294e4fa7cca9e9eadd0c8105bcf65cb1721090cd353328&user_id=1612991"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                # Pastikan data tidak kosong
                if data:
                    randomwaifu = random.randint(0, 4)
                    chara = data["post"][randomwaifu]
                    imgChara = chara["file_url"]
                    name = query
                    url = chara["source"]
                    embed = discord.Embed(title=name, color=discord.Color.fuchsia())
                    embed.set_image(url=imgChara)
                    embed.add_field(name="Source", value=f"[Click here]({url})")
                    embed.set_footer(text="Rin Bot | Disediakan oleh Gelbooru", icon_url="attachment://rin.jpeg")
                    await ctx.send(embed=embed, file=discord.File("rin.jpeg", filename="rin.jpeg"))
                else:
                    await ctx.send ("Tidak ada hasil yang ditemukan untuk tag tersebut.")
            else:
                await ctx.send("Gagal mengambil data dari API.")
                raise Exception(f"Error {response.status}: Failed to fetch data")

@bot.command()
async def talita(ctx):
    await ctx.send("Talita punya nya Rehan")

@bot.command()
async def membercount(ctx):
    """
    Menampilkan jumlah member di server.
    """
    member_count = ctx.guild.member_count
    await ctx.send(f"Jumlah anggota di server ini: {member_count}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """
    Kick seorang anggota dari server.
    :param member: Anggota yang akan di-kick.
    :param reason: Alasan kick (opsional).
    """
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} telah di-kick dari server. Alasan: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """
    Ban seorang anggota dari server.
    :param member: Anggota yang akan di-ban.
    :param reason: Alasan ban (opsional).
    """
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} telah di-ban dari server. Alasan: {reason}')

bot.run(DISCORD_BOT_TOKEN)
