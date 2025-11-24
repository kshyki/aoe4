import discord
from discord.ext import commands
import config
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=config.PREFIX,
    intents=intents
)

async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")
    await load_cogs()

# Запускаем
bot.run(config.TOKEN)
