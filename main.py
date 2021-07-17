import discord
from discord.ext import commands
import os
import yaml
from pathlib import Path

with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.BaseLoader)

bot = commands.Bot(command_prefix=config['prefix'])

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')
        print('Cog '+filename[:-3]+' loaded')
    
bot.run(config['token'])
