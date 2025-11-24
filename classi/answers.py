import discord

class EmbedMessage:
    @staticmethod
    async def send(ctx, text: str, *, title: str = "", color: int = 0xFFFF00):
        embed = discord.Embed(
            title=title,
            description=text,
            color=color
        )
        await ctx.send(embed=embed)
