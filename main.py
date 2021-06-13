import discord
from discord.ext import commands
import os
from json import load
from pathlib import Path

with Path("config.json").open() as f:
    config = load(f)

bot = commands.Bot(command_prefix=config['prefix'])

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')
        print('Cog '+filename[:-3]+' loaded')
    
bot.run(config['token'])
