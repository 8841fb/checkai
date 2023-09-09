import discord

from discord.ext import commands

from helpers.generate import Prodia_Client


class Prodia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Prodia_Client()

    @commands.command(aliases=['generate'])
    async def prodia(self, ctx, *, prompt):
        """Generate an image with prodia."""
        image = await self.client.generate(prompt)
        embed = discord.Embed(color=discord.Color.dark_embed())
        embed.set_image(url=image)
        await ctx.reply(embed=embed)


async def setup(bot):
    """Set up the cog."""
    await bot.add_cog(Prodia(bot))
