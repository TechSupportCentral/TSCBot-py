from discord.ext import commands
import discord
import yaml

class administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global role_ids
    role_ids = config['role_ids']
    global channel_ids
    channel_ids = config['channel_ids']

    @commands.command()
    async def sendmessage(self, ctx, *args):
        guild = ctx.message.guild
        owner_role = guild.get_role(int(role_ids['owner']))
        if not owner_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return
        elif not args:
            await ctx.send("Please specify a message to send.")
            return
        await ctx.message.delete()
        await ctx.send(' '.join(args))

    @commands.command()
    async def announce(self, ctx, *args):
        guild = ctx.message.guild
        owner_role = guild.get_role(int(role_ids['owner']))
        if not owner_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return
        elif not args:
            await ctx.send("Please specify the announcement message.")
            return
        await ctx.message.delete()
        embed=discord.Embed(title="Announcement", description=' '.join(args), color=0x00a0a0)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(administration(bot))
