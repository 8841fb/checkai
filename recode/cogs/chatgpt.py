import discord
from discord.ext import commands

from helpers.chatbot import OpenAI


class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI()

    @commands.command()
    async def ask(self, ctx, *, prompt):
        """Generate a message with chatgpt."""
        message = await self.client.generate(prompt)
        embed = discord.Embed(
            color=discord.Color.dark_embed(), description=f'{message}'
        )
        embed.set_author(name=f'{prompt}', icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)


async def setup(bot):
    """Set up the cog."""
    await bot.add_cog(ChatGPT(bot))
