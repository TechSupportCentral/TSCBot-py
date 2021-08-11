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

    @commands.command()
    async def dm(self, ctx, user=None, *args):
        guild = ctx.message.guild
        owner_role = guild.get_role(int(role_ids['owner']))
        if not owner_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return
        elif not user:
            await ctx.send("Please specify a user to DM.")
            return
        elif not args:
            await ctx.send("Please specify a DM to send.")
            return

        if "<@" in user:
            id = user
            id = id.replace("<", "")
            id = id.replace(">", "")
            id = id.replace("@", "")
            id = id.replace("!", "")
            id = int(id)
        elif user.isdigit():
            id = int(user)
        else:
            await ctx.send("Users have to be in the form of an ID or a mention.")
            return
        guild = ctx.message.guild
        if guild.get_member(id) is None:
            await ctx.send("User is not in the server.")
            return
        member = guild.get_member(id)

        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        dmbed = discord.Embed(title="Message from the owner of TSC", description=' '.join(args), color=0x00a0a0)
        dm_failed = False
        try:
            await dm.send(embed=dmbed)
        except:
            dm_failed = True

        if dm_failed == True:
            await ctx.send("Failed to DM the user")
            return
        await ctx.message.add_reaction("✅")
        embed = discord.Embed(title="DM Sent", color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Sent to", value=member, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Message:", value=' '.join(args), inline=False)
        channel = self.bot.get_channel(int(channel_ids['bot_dm']))
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(administration(bot))
