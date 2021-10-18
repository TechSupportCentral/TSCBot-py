from discord.ext import commands
import discord
import yaml
#from emoji import emoji_count
from main import get_database
mongodb = get_database()

class administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global channel_ids
    channel_ids = config['channel_ids']

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sendmessage(self, ctx, *, message):
        if not message:
            await ctx.send("Please specify a message to send.")
            return
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, *, message):
        if not message:
            await ctx.send("Please specify the announcement message.")
            return
        await ctx.message.delete()
        embed=discord.Embed(title="Announcement", description=message, color=0x00a0a0)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, user=None, *, message):
        if not user:
            await ctx.send("Please specify a user to DM.")
            return
        elif not message:
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
        dmbed = discord.Embed(title="Message from the owners of TSC", description=message, color=0x00a0a0)
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
        embed.add_field(name="Sent by", value=ctx.message.author, inline=False)
        embed.add_field(name="Message:", value=message, inline=False)
        channel = self.bot.get_channel(int(channel_ids['bot_dm']))
        await channel.send(embed=embed)

    @commands.command(name="accept-suggestion")
    @commands.has_permissions(administrator=True)
    async def accept_suggestion(self, ctx, id=None, *, reason):
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

        if not reason:
            reason = "No reason provided."

        message = await channel.fetch_message(id)
        embed = discord.Embed(description=message.embeds[0].description, color=discord.Color.green())
        embed.set_author(name=message.embeds[0].author.name, icon_url=message.embeds[0].author.icon_url)
        embed.add_field(name="Status: Accepted", value=reason)
        await message.edit(embed=embed)

        dmbed = discord.Embed(title="Your suggestion was accepted by the owners.", description=message.embeds[0].description, color=discord.Color.green())
        dmbed.add_field(name="Reason:", value=reason)

        member = ctx.message.guild.get_member_named(message.embeds[0].author.name)
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
    @commands.has_permissions(administrator=True)
    async def decline_suggestion(self, ctx, id=None, *, reason):
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

        if not reason:
            reason = "No reason provided."

        message = await channel.fetch_message(id)
        embed = discord.Embed(description=message.embeds[0].description, color=discord.Color.red())
        embed.set_author(name=message.embeds[0].author.name, icon_url=message.embeds[0].author.icon_url)
        embed.add_field(name="Status: Declined", value=reason)
        await message.edit(embed=embed)

        dmbed = discord.Embed(title="Your suggestion was declined by the owners.", description=message.embeds[0].description, color=discord.Color.red())
        dmbed.add_field(name="Reason:", value=reason)

        member = ctx.message.guild.get_member_named(message.embeds[0].author.name)
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

    @commands.command(name="add-swear")
    @commands.has_permissions(administrator=True)
    async def add_swear(self, ctx, arg=None):
        if not arg:
            await ctx.send("Please provide the name of the new swear.")
            return

        collection = mongodb['swears']
        for swear in collection.find():
            if swear.get('swear') == arg:
                await ctx.send(f"The swear `{arg}` already exists.")
                return
        collection.insert_one({"swear": arg})
        await ctx.send(f"Swear `{arg}` successfully added.")
        await ctx.send("reload swears")

    @commands.command(name="remove-swear")
    @commands.has_permissions(administrator=True)
    async def remove_swear(self, ctx, arg=None):
        if not arg:
            await ctx.send("Please provide the name of the swear to remove.")
            return

        collection = mongodb['swears']
        found = False
        for swear in collection.find():
            if swear.get('swear') == arg:
                found = True
        if found == False:
            await ctx.send(f"The swear `{arg}` was not found.")
            return
        collection.delete_one({"swear": arg})
        await ctx.send(f"Swear `{arg}` successfully removed.")
        await ctx.send("reload swears")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def swearlist(self, ctx):
        collection = mongodb['swears']
        description = ""
        for swear in collection.find():
            description = description + f"\n{swear.get('swear')}"
        embed = discord.Embed(title="Swearlist", description=description, color=0x00a0a0)
        await ctx.send(embed=embed)

#    @commands.command(name="add-reaction-role")
#    async def add_reaction_role(self, ctx, role=None, reaction=None, *, message):
#        if not role:
#            await ctx.send("Please provide the ID of the role to add.")
#            return
#        if not reaction:
#            await ctx.send("Please provide the emoji to use as a reaction.")
#            return
#        if not message:
#            await ctx.send("Please provide the contents of the reaction role message.")
#            return
#
#        if not ctx.message.guild.get_role(int(role)):
#            await ctx.send("Not a valid role.")
#            return
#
#        if emoji_count(reaction) != 1:
#            await ctx.send("Not a valid emoji.")
#            return
#
#        channel = self.bot.get_channel(int(channel_ids['reaction_roles']))
#        message = await channel.send(message)
#        await message.add_reaction(reaction)
#
#        collection = mongodb['reaction-roles']
#        collection.insert_one({"_id": str(message.id), "role": role, "emoji": reaction})
#
#        await ctx.message.add_reaction("✅")
#        await ctx.send("reload reaction roles")

    @commands.command()
    async def softban(self, ctx, user=None):
        guild = ctx.message.guild
        if not user:
            await ctx.send("Please mention a user to softban.")
            return

        elif "<@" in user:
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

        if guild.get_member(id) is None:
            member = await self.bot.fetch_user(id)
        else:
            member = guild.get_member(id)

        if not member:
            await ctx.send("Not a valid discord user.")
            return

        await guild.ban(discord.Object(id=id), delete_message_days=7, reason="softban")
        await ctx.message.add_reaction("✅")
        await guild.unban(discord.Object(id=id), reason="softban")

def setup(bot):
    bot.add_cog(administration(bot))
