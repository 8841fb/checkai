import os

from discord.ext import commands
from jishaku.paginators import PaginatorInterface, WrappedPaginator


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, cog):
        """Load a cog."""
        try:
            await self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.reply(f'```py\n{e}```')
        else:
            await ctx.reply(f'Loaded {cog}.')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        """Unload a cog."""
        try:
            await self.bot.unload_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.reply(f'```py\n{e}```')
        else:
            await ctx.reply(f'Unloaded {cog}.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog):
        """Reload a cog."""
        try:
            await self.bot.reload_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.reply(f'```py\n{e}```')
        else:
            await ctx.reply(f'Reloaded {cog}.')

    @commands.command()
    @commands.is_owner()
    async def reloadall(self, ctx):
        """Reload all cogs."""
        try:
            for file in os.listdir('cogs'):
                if not file.endswith('.py') or file.startswith('_'):
                    continue

                name = file[:-3]
                await self.bot.reload_extension(f'cogs.{name}')
        except Exception as e:
            await ctx.reply(f'```py\n{e}```')
        else:
            await ctx.reply(f'Reloaded all cogs.')

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.reply('Shutting down...')
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot."""
        await ctx.reply('Restarting...')
        os.execv(sys.executable, ['python'] + sys.argv)


async def setup(bot):
    """Set up the cog."""
    await bot.add_cog(Owner(bot))
