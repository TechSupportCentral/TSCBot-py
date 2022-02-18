import discord
from discord.ext import commands
import os
import yaml
import pymongo

with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.BaseLoader)

def get_database():
    client = pymongo.MongoClient(config['mongo_uri'])
    db = client[config['mongo_db']]
    return db

if __name__ == "__main__":
    mongodb = get_database()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents, help_command=None)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print('Cog '+filename[:-3]+' loaded')
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='TSC'))
    print('Logged in as {}'.format(bot.user.name))

bot.run(config['token'])
