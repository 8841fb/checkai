import discord
from discord.ext import commands
import datetime
import requests
import prodia



intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, command_prefix, prodia_client):
        intents.message_content = True
        super().__init__(command_prefix, intents=intents)
        self.prodia_client = prodia_client

bot = commands.Bot(command_prefix='!', intents=intents)
key = "5ffd7bb9-8ff4-45d0-9e37-540879c7c37a"
prodia.Client(api_key=key)
start_time = None
client = prodia.Client(api_key=key)
bot = MyBot(command_prefix='!', prodia_client=client)

@bot.event
async def on_ready():
    global start_time
    print(f'Logged in as {bot.user.name}')
    server_id = 1104027127709438002  # Replace with your server ID
    channel_id = 1114861304897875968  # Replace with your channel ID

    server = bot.get_guild(server_id)
    channel = server.get_channel(channel_id)

    if start_time is None:
        start_time = datetime.datetime.now()


    uptime = datetime.datetime.now() - start_time
    uptime_message = f"Bot is now online! Uptime: {uptime}"
    await channel.send(uptime_message)

@bot.event
async def on_command_completion(ctx):
    server_id = 1104027127709438002  # Replace with your server ID
    channel_id = 1114861304897875968  # Replace with your channel ID

    if ctx.guild and ctx.guild.id == server_id:
        server = bot.get_guild(server_id)
        channel = server.get_channel(channel_id)
        author = ctx.author
        command = ctx.command
        message = ctx.message.content

        export_message = f"Command used by {author}: `{command}` - Message: {message}"
        await channel.send(export_message)


@bot.command()
async def generate(ctx, *, prompt):
    # Use prodia.arunv1 to generate AI art
    image = await prodia.arunv1(prompt=prompt)
    
    # Send the image to the Discord channel
    #<await ctx.send(image)>
    #or
    await ctx.send(embed=discord.Embed().set_image(url=image))

bot.run('MTExNDg1NDQzNzQ2MzI3MzYwMw.GS77b6.jdFdwFfzz2WnJdXkbhzxMHJPWyShPCCyHecrQ4')
