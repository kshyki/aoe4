from discord.ext import commands
import discord
import sqlite3
import asyncio
from classi.answers import EmbedMessage
import requests
DB_PATH = "players.db"
ranks = {"conqueror_3": "Третий конк <:conqueror_3:1440495533914587226>",
         "conqueror_2": "Второй конк <:conquer_2:1440497328850079745>",
         "conqueror_1": "Первый конк <:conquer_1:1440496879938048020>",
         "diamond_3": "Третий даймонд <:diamond_3:1440496528115634176>",
         "diamond_2": "Второй даймонд <:diamond_2:1440499629232881787>",
         "diamond_1": "Первый даймонд <:diamond_1:1440497840555294730>",
         "platinum_3": "Третья платина <:platinum_3:1440498000521859202>",
         "platinum_2": "Вторая платина <:platinum_2:1440497948659027988>",
         "platinum_1": "Первая платина <:platinum_1:1440497897702686771>",
         "gold_3": "Третье золото <:gold_3:1440499854173536307>",
         "gold_2": "Второе золото <:gold_2:1440499944804057271>",
         "gold_1": "Первое золото <:gold_1:1440499982498005054>",
         "silver_3": "Третье серебро",
         "silver_2": "Второе серебро",
         "silver_1": "Первое серебро",
         "bronze_3": "Третья бронза",
         "bronze_2": "Вторая бронза",
         "bronze_1": "Первая бронза",}
class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lock = asyncio.Lock()
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                user_id INTEGER PRIMARY KEY,
                nickname TEXT NOT NULL,
                profile_id TEXT NOT NULL,
                country TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()

    @commands.command()
    async def регистрируй(self, ctx, nickname: str, aoe_link: str, country: str):
        user_id = ctx.author.id
        async with self.lock:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
            exists = cursor.fetchone()
            

            if exists:
                conn.close()
                await ctx.send("Ты уже зарегистрирован.")
                return
            profile_id = aoe_link.split("/")[-1]
            cursor.execute("""
                INSERT INTO players (user_id, nickname, profile_id, country)
                VALUES (?, ?, ?, ?)
            """, (user_id, nickname, profile_id, country))

            conn.commit()
            conn.close()

        await EmbedMessage.send(ctx, f"**Ник:** {nickname}\n**AoEWorld:** {aoe_link}\n**Страна:** {country}", title="Регистрация успешна!🍺")

    @commands.command()
    async def мой_ммр(self, ctx):
        user_id = ctx.author.id
        async with self.lock:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
            exists = cursor.fetchone()
            user_id, nickname, profile_id, country = exists
            if not exists:
                await ctx.send("Я не знаю кто ты")
            else:
                user_info = requests.get(f"https://aoe4world.com/api/v0/players/{profile_id}").json()
                embed = discord.Embed(title=nickname, url = f"https://aoe4world.com/players/{profile_id}", color=0xFFFF00)
                embed.set_thumbnail(url=user_info["avatars"]["medium"])
                embed.add_field(name = "Соло ранкед:", value = f"{ranks[user_info["modes"]["rm_solo"]["rank_level"]]}\nРанг: {user_info["modes"]["rm_solo"]["rank"]}\nММры: {user_info["modes"]["rm_solo"]["rating"]} ")
                embed.add_field(name = "Тг ранкед:", value = f"{ranks[user_info["modes"]["rm_team"]["rank_level"]]}\nРанг: {user_info["modes"]["rm_team"]["rank"]}\nМмры:{user_info["modes"]["rm_team"]["rating"]} ")
                await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Register(bot))
