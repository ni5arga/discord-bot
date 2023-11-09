import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True  

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command("help")


for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        bot.load_extension(f'modules.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

token = os.environ['DISCORD_BOT_TOKEN']
bot.run(token)
