from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "привет" in message.content.lower():
            await message.channel.send("Привет!")

async def setup(bot):
    await bot.add_cog(Basic(bot))
