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
        try:
            await dm.send(embed=dmbed)
        except:
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

    @commands.command(name="accept-suggestion")
    async def accept_suggestion(self, ctx, id=None, *args):
        guild = ctx.message.guild
        owner_role = guild.get_role(int(role_ids['owner']))
        if not owner_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not id:
            await ctx.send("Feed me some arguments please")
            return
        elif not id.isdigit():
            await ctx.send("Please mention what suggestion you'd like to accept via the message ID.")
            return
        channel = self.bot.get_channel(int(channel_ids['suggestions_list']))
        try:
            await channel.fetch_message(id)
        except:
            await ctx.send("Not a valid message ID.")
            return

        if not args:
            args = ['No', 'reason', 'provided.']

        message = await channel.fetch_message(id)
        embed = discord.Embed(description=message.embeds[0].description, color=discord.Color.green())
        embed.set_author(name=message.embeds[0].author.name, icon_url=message.embeds[0].author.icon_url)
        embed.add_field(name="Status: Accepted", value=' '.join(args))
        await message.edit(embed=embed)

        dmbed = discord.Embed(title="Your suggestion was accepted by the owner.", description=message.embeds[0].description, color=discord.Color.green())
        dmbed.add_field(name="Reason:", value=' '.join(args))

        member = guild.get_member_named(message.embeds[0].author.name)
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        try:
            await dm.send(embed=dmbed)
        except:
            await ctx.send("The suggestion was accepted successfully but the the user was unable to be DMed.")
            return

        await ctx.message.add_reaction("✅")

    @commands.command(name="decline-suggestion")
    async def decline_suggestion(self, ctx, id=None, *args):
        guild = ctx.message.guild
        owner_role = guild.get_role(int(role_ids['owner']))
        if not owner_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not id:
            await ctx.send("Feed me some arguments please")
            return
        elif not id.isdigit():
            await ctx.send("Please mention what suggestion you'd like to decline via the message ID.")
            return
        channel = self.bot.get_channel(int(channel_ids['suggestions_list']))
        try:
            await channel.fetch_message(id)
        except:
            await ctx.send("Not a valid message ID.")
            return

        if not args:
            args = ['No', 'reason', 'provided.']

        message = await channel.fetch_message(id)
        embed = discord.Embed(description=message.embeds[0].description, color=discord.Color.red())
        embed.set_author(name=message.embeds[0].author.name, icon_url=message.embeds[0].author.icon_url)
        embed.add_field(name="Status: Declined", value=' '.join(args))
        await message.edit(embed=embed)

        dmbed = discord.Embed(title="Your suggestion was declined by the owner.", description=message.embeds[0].description, color=discord.Color.red())
        dmbed.add_field(name="Reason:", value=' '.join(args))

        member = guild.get_member_named(message.embeds[0].author.name)
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        try:
            await dm.send(embed=dmbed)
        except:
            await ctx.send("The suggestion was declined successfully but the the user was unable to be DMed.")
            return

        await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(administration(bot))
