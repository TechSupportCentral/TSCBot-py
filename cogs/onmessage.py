from discord.ext import commands
import discord
import yaml

class onmessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('swears.yaml', 'r') as swears_file:
        swearlist = yaml.load(swears_file, Loader=yaml.BaseLoader)
    global swears
    swears = swearlist['swears']
    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global channel_ids
    channel_ids = config['channel_ids']

    @commands.Cog.listener("on_message")
    async def swearfilter(self, message):
         swore = ""
         for swear in swears:
             if swear in message.content:
                 swore = swear
         if swore != "":
            await message.delete()
            dm = await message.author.create_dm()
            embed=discord.Embed(title="Swear", description="TEG is a PG Friendly server, you cannot swear here.")
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
            embed.add_field(name="Swear Detected:", value=swore, inline=False)
            dm_failed = False
            try:
                await dm.send(embed=embed)
            except:
                dm_failed = True

            embed=discord.Embed(title="Swear by " + str(message.author), color=0x00a0a0)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="User ID", value=message.author.id, inline=False)
            embed.add_field(name="In channel", value=message.channel.mention, inline=False)
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
            embed.add_field(name="Swear Detected:", value=swore, inline=False)
            if dm_failed == True:
                embed.set_footer(text="was not able to DM user")
            channel = self.bot.get_channel(int(channel_ids['filter_log']))
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(onmessage(bot))
