import discord
from discord.ext import commands
from discord.ext.commands import errors

from helpers import config


class Events(commands.Cog):
    """Event listeners for handling command errors, command usage, and bot readiness."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, err: commands.CommandError
    ):
        """Event listener for handling command errors."""
        if isinstance(
            err, (errors.MissingRequiredArgument, errors.BadArgument)
        ):
            helper = (
                str(ctx.invoked_subcommand)
                if ctx.invoked_subcommand
                else str(ctx.command)
            )
            await ctx.send_help(helper)
        elif isinstance(err, errors.CommandInvokeError):
            await ctx.send(
                f'An error occurred while processing the command: `{err}`'  # noqa: E501
            )
            # print full traceback to console
            raise err.original
        elif isinstance(err, errors.CheckFailure):
            pass
        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send(f'You are already using this command.')
        elif isinstance(err, errors.CommandOnCooldown):
            # if user has role 1234 or 5678, bypass cooldown
            await ctx.send(
                f'This command is on cooldown. Try again in {err.retry_after:.2f}s.'  # noqa: E501
            )
        elif isinstance(err, errors.CommandNotFound):
            await ctx.send(
                f'Command not found. Use `{config.PREFIX}help` for a list of commands.'  # noqa: E501
            )

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        """Event listener that activates when a command is used."""
        embed = discord.Embed(
            color=discord.Color.dark_blue(),
            description=f'**{ctx.author}** (`{ctx.author.id}`) used command `{ctx.message.content}` in channel {ctx.channel.mention} (`{ctx.channel.id}`) in guild **{ctx.guild}** (`{ctx.guild.id}`)',  # noqa: E501
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.set_footer(text=f'User ID: {ctx.author.id}')
        await self.bot.get_channel(1114861304897875968).send(embed=embed)
        print(f'Command used: {ctx.author} | {ctx.message.content}')

    @commands.Cog.listener()
    async def on_ready(self):
        """Event listener that activates when the bot is ready."""
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'{config.PREFIX}help | {len(self.bot.guilds)} servers',
            ),
            status=discord.Status.idle,
        )

        print(f'Ready: {self.bot.user} | {self.bot.user.id}')


async def setup(bot):
    await bot.add_cog(Events(bot))
