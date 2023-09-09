import os

import discord
from discord.ext.commands import AutoShardedBot, MinimalHelpCommand

from helpers import config

intents = discord.Intents.default()
intents.message_content = True


class checkai(AutoShardedBot):
    """the main bot class."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the bot instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(
            command_prefix=config.PREFIX,
            case_insensitive=True,
            help_command=HelpFormat(),
            intents=intents,
            owner_ids=config.OWNERS,
            *args,
            **kwargs,
        )

        self.launch_time = discord.utils.utcnow()

    async def setup_hook(self):
        """Perform setup operations for the bot."""
        await self.load_extension('jishaku')
        for file in os.listdir('cogs'):
            if not file.endswith('.py') or file.startswith('_'):
                continue

            name = file[:-3]
            await self.load_extension(f'cogs.{name}')

    async def on_message(self, msg: discord.Message):
        """
        Event handler for message events.

        Args:
            msg (discord.Message): The received message.
        """
        if not self.is_ready() or msg.author.bot or not msg.guild:
            return

        await self.process_commands(msg)

    async def process_commands(self, msg):
        """
        Process commands from a message.

        Args:
            msg: The received message.
        """
        ctx = await self.get_context(msg, cls=discord.ext.commands.Context)
        await self.invoke(ctx)


class HelpFormat(MinimalHelpCommand):
    """Custom help command format for the bot."""

    def __init__(self):
        """Initialize the HelpFormat instance."""
        super().__init__(command_attrs={'hidden': True})

    async def send_bot_help(self, mapping):
        """
        Send bot help information.

        Args:
            mapping: A mapping of cogs to their associated commands.
        """
        embed = self._create_embed(
            title='Help',
            description=f'Use `{config.PREFIX}help <command>` for more info on a command.',  # noqa: E501
        )
        await self._add_cog_fields(embed, mapping)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """
        Send help information for a specific command.

        Args:
            command: The command to get help for.
        """
        embed = self._create_embed(
            title=f'Help for {command.name}',
            description=command.help or 'No description',
        )
        self._add_aliases_field(embed, command.aliases)
        self._add_usage_field(embed, command)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        """
        Send help information for a command group.

        Args:
            group: The command group to get help for.
        """
        embed = self._create_embed(
            title=f'Help for {group.name}',
            description=group.help or 'No description',
        )
        self._add_aliases_field(embed, group.aliases)
        await self._add_subcommands_field(embed, group.commands)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        """
        Send help information for a cog.

        Args:
            cog: The cog to get help for.
        """
        embed = self._create_embed(
            title=f'Help for {cog.qualified_name}',
            description=cog.description or 'No description',
        )
        await self._add_cog_commands_field(embed, cog)
        await self.get_destination().send(embed=embed)

    @staticmethod
    def _create_embed(title, description):
        """
        Create an embed object.

        Args:
            title (str): The title of the embed.
            description (str): The description of the embed.

        Returns:
            discord.Embed: The created embed object.
        """
        return discord.Embed(
            title=title,
            description=description,
            color=discord.Color.dark_embed(),
        )

    @staticmethod
    def _add_aliases_field(embed, aliases):
        """
        Add aliases field to the embed.

        Args:
            embed (discord.Embed): The embed object to add the field to.
            aliases (List[str]): The list of command aliases.
        """
        if aliases:
            embed.add_field(
                name='Aliases',
                value=', '.join(f'`{a}`' for a in aliases),
                inline=False,
            )

    @staticmethod
    def _add_usage_field(embed, command):
        """
        Add usage field to the embed.

        Args:
            embed (discord.Embed): The embed object to add the field to.
            command (discord.ext.commands.Command): The command to get the usage for.
        """
        if command.usage:
            embed.add_field(
                name='Usage',
                value=f'`{config.PREFIX}{command.name} {command.usage}`',
                inline=False,
            )

    async def _add_subcommands_field(self, embed, commands):
        """
        Add subcommands field to the embed.

        Args:
            embed (discord.Embed): The embed object to add the field to.
            commands (List[discord.ext.commands.Command]): The list of subcommands.
        """
        filtered = await self.filter_commands(commands, sort=True)
        if filtered:
            embed.add_field(
                name='Subcommands',
                value=', '.join(f'`{c.name}`' for c in filtered),
                inline=False,
            )

    async def _add_cog_commands_field(self, embed, cog):
        """
        Add cog commands field to the embed.

        Args:
            embed (discord.Embed): The embed object to add the field to.
            cog (discord.ext.commands.Cog): The cog to get the commands for.
        """
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if filtered:
            embed.add_field(
                name='Commands',
                value=', '.join(f'`{c.name}`' for c in filtered),
                inline=False,
            )

    async def _add_cog_fields(self, embed, mapping):
        """
        Add cog fields to the embed.

        Args:
            embed (discord.Embed): The embed object to add the fields to.
            mapping: A mapping of cogs to their associated commands.
        """
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                embed.add_field(
                    name=cog.qualified_name,
                    value=', '.join(
                        f'`{c.name}`' for c in commands if not c.hidden
                    ),
                    inline=False,
                )
