import discord
import yaml
import logging
import random

with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.BaseLoader)

client = discord.Client()
prefix = config['prefix']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix+'ping'):
        await message.channel.send('Pong!')

    if message.content.startswith(prefix+'help'):
        with open('commands.yaml', 'r') as commands_file:
            commands = yaml.load(commands_file, Loader=yaml.BaseLoader)

        embedVar = discord.Embed(title="Command List", color=0x00a0a0)
        for command in commands:
            embedVar.add_field(name=command, value=commands[command], inline=False)
        await message.channel.send(embed=embedVar)

client.run(config['token'])
