import discord
from discord.ext import commands
import os
import yaml
from pathlib import Path

with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.BaseLoader)

bot = commands.Bot(command_prefix=config['prefix'])

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print('Cog '+filename[:-3]+' loaded')
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='TEG'))
    print('Logged in as {}'.format(bot.user.name))

bot.run(config['token'])
