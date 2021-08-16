from discord.ext import commands
import discord
import yaml
from asyncio import sleep
from datetime import datetime
import re
from main import get_database
mongodb = get_database()

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global role_ids
    role_ids = config['role_ids']
    global channel_ids
    channel_ids = config['channel_ids']

    @commands.command()
    async def purge(self, ctx, arg=None):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        if not mod_role in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not arg:
            await ctx.send("Please mention a number of messages to purge.")
            return
        elif arg.isdigit():
            arg = int(arg)
        else:
            await ctx.send("Not a valid number of messages")
            return

        if arg > 100:
            await ctx.send("You can only delete 100 or fewer messages at once.")
            return

        await ctx.channel.purge(limit=arg)
        embed=discord.Embed(title=str(arg) + " Messages Deleted", color=0x00a0a0)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Deleted by", value=ctx.message.author, inline=True)
        embed.add_field(name="In channel", value=ctx.message.channel.mention, inline=True)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        await channel.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, arg=None):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        trial_mod_role = guild.get_role(int(role_ids['trial_mod']))
        if mod_role not in ctx.message.author.roles or trial_mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not arg:
            id = ctx.message.author.id

        elif "<@" in arg:
            id = arg
            id = id.replace("<", "")
            id = id.replace(">", "")
            id = id.replace("@", "")
            id = id.replace("!", "")
            id = int(id)

        elif arg.isdigit():
            id = int(arg)

        else:
            await ctx.send("Users have to be in the form of an ID or a mention.")
            return

        if guild.get_member(id) is None:
            await ctx.send("User is not in the server.")
            return

        member = guild.get_member(id)
        embed=discord.Embed(title=member, color=0x00a0a0)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User ID", value=id, inline=False)
        if member.name != member.display_name:
            embed.add_field(name="Nickname", value=member.display_name, inline=False)
        embed.add_field(name="Account Created:", value=member.created_at.strftime("%-d %B %Y at %-H:%M"), inline=True)
        embed.add_field(name="Joined Server:", value=member.joined_at.strftime("%-d %B %Y at %-H:%M"), inline=True)
        mention = []
        for role in member.roles:
            if role.name != "@everyone":
                mention.append(role.mention)
        roles = ", ".join(mention)
        embed.add_field(name="Roles", value=roles, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def warnings(self, ctx, arg=None):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        trial_mod_role = guild.get_role(int(role_ids['trial_mod']))
        if mod_role not in ctx.message.author.roles or trial_mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not arg:
            await ctx.send("Please mention a user to check the warnings of.")
            return

        elif "<@" in arg:
            id = arg
            id = id.replace("<", "")
            id = id.replace(">", "")
            id = id.replace("@", "")
            id = id.replace("!", "")
            id = int(id)

        elif arg.isdigit():
            id = int(arg)

        else:
            await ctx.send("Users have to be in the form of an ID or a mention.")
            return

        if guild.get_member(id) is not None:
            description = f"**User:** {guild.get_member(id)}\n"

        collection = mongodb['moderation']
        found = False
        number = 0
        for warning in collection.find():
            if warning.get('user') == str(id):
                found = True
                number = number + 1
                description = description + f"\n`{number}`:\n**Type:** {warning.get('type')}\n**Reason:** {warning.get('reason')}\n**Moderator:** {guild.get_member(int(warning.get('moderator')))}\n**Message ID:** {warning.get('_id')}\n"
        embed = discord.Embed(title="Warnings", description=description, color=0x00a0a0)
        if found == False:
            await ctx.send("This user has no warnings.")
            return
        await ctx.send(embed=embed)

    @commands.command()
    async def warn(self, ctx, user=None, *args):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        trial_mod_role = guild.get_role(int(role_ids['trial_mod']))
        if mod_role not in ctx.message.author.roles or trial_mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not user:
            await ctx.send("Please mention a user to warn.")
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
            await ctx.send("User is not in the server.")
            return
        member = guild.get_member(id)

        if not args:
            args = ['No', 'reason', 'provided.']

        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        message = await channel.send(".")
        embed = discord.Embed(title="Warning", description=f"Use `!unwarn {message.id} <reason>` to remove this warning.", color=discord.Color.red())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User warned", value=member, inline=True)
        embed.add_field(name="User ID", value=str(id), inline=True)
        embed.add_field(name="Moderator", value=ctx.message.author, inline=False)
        embed.add_field(name="Reason", value=' '.join(args), inline=False)
        await message.edit(content="", embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "warn", "user": str(id), "moderator": str(ctx.message.author.id), "reason": ' '.join(args)})

        dmbed = discord.Embed(title="You have been warned.", description=f"**Reason:** {' '.join(args)}", color=discord.Color.red())
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        try:
            await dm.send(embed=dmbed)
        except:
            await ctx.send("The member was warned successfully, but a DM was unable to be sent.")
            return
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def unwarn(self, ctx, id=None, *args):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        trial_mod_role = guild.get_role(int(role_ids['trial_mod']))
        if mod_role not in ctx.message.author.roles or trial_mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not id:
            await ctx.send("Please mention the ID of a warn message to remove.")
            return

        elif not id.isdigit():
            await ctx.send("Warns have to be in the form of a Message ID.")
            return

        collection = mongodb['moderation']
        found = False
        for warn in collection.find():
            if warn.get('_id') == id:
                found = True
                user = warn.get('user')
                reason = warn.get('reason')
        if found == False:
            await ctx.send("The warn was not found.")
            return
        collection.delete_one({"_id": id})

        if not args:
            args = ['No', 'reason', 'provided.']

        member = guild.get_member(int(user))
        embed = discord.Embed(title="Warning Removed", color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User unwarned", value=member, inline=True)
        embed.add_field(name="User ID", value=user, inline=True)
        embed.add_field(name="Moderator", value=ctx.message.author, inline=False)
        embed.add_field(name="Reason", value=' '.join(args), inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        await channel.send(embed=embed)

        dmbed = discord.Embed(title="Your warning has been removed.", color=discord.Color.green())
        dmbed.add_field(name="Original reason for warn", value=reason, inline=False)
        dmbed.add_field(name="Reason for removal", value=' '.join(args), inline=False)
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        try:
            await dm.send(embed=dmbed)
        except:
            await ctx.send("The warn was removed successfully, but a DM was unable to be sent to the original warned user.")
            return
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def kick(self, ctx, user=None, *args):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        if mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not user:
            await ctx.send("Please mention a user to kick.")
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
            await ctx.send("User is not in the server.")
            return
        member = guild.get_member(id)

        if not args:
            args = ['No', 'reason', 'provided.']

        embed = discord.Embed(title="Kick", color=discord.Color.red())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User kicked", value=member, inline=True)
        embed.add_field(name="User ID", value=str(id), inline=True)
        embed.add_field(name="Moderator", value=ctx.message.author, inline=False)
        embed.add_field(name="Reason", value=' '.join(args), inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "kick", "user": str(id), "moderator": str(ctx.message.author.id), "reason": ' '.join(args)})

        dmbed = discord.Embed(title="You have been kicked.", description=f"**Reason:** {' '.join(args)}", color=discord.Color.red())
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        dm_failed = False
        try:
            await dm.send(embed=dmbed)
        except:
            dm_failed = True

        if dm_failed == False:
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("The member was kicked successfully, but a DM was unable to be sent.")
        await guild.kick(member, reason=' '.join(args))

    @commands.command()
    async def ban(self, ctx, user=None, *args):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        if mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not user:
            await ctx.send("Please mention a user to ban.")
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

        member = await self.bot.fetch_user(id)
        if not member:
            await ctx.send("Not a valid discord user.")
            return

        if not args:
            args = ['No', 'reason', 'provided.']

        embed = discord.Embed(title="Ban", color=discord.Color.red())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User banned", value=member, inline=True)
        embed.add_field(name="User ID", value=str(id), inline=True)
        embed.add_field(name="Moderator", value=ctx.message.author, inline=False)
        embed.add_field(name="Reason", value=' '.join(args), inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "ban", "user": str(id), "moderator": str(ctx.message.author.id), "reason": ' '.join(args)})

        dmbed = discord.Embed(title="You have been banned.", description=f"**Reason:** {' '.join(args)}", color=discord.Color.red())
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        dm_failed = False
        try:
            await dm.send(embed=dmbed)
        except:
            dm_failed = True

        if dm_failed == False:
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("The member was banned successfully, but a DM was unable to be sent.")

        await guild.ban(discord.Object(id=id), reason=' '.join(args))

    @commands.command()
    async def unban(self, ctx, user=None, *args):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        if mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not user:
            await ctx.send("Please mention a user to unban.")
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

        member = await self.bot.fetch_user(id)
        if not member:
            await ctx.send("Not a valid discord user.")
            return

        if not args:
            args = ['No', 'reason', 'provided.']

        embed = discord.Embed(title="Ban Removed", color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User unbanned", value=member, inline=True)
        embed.add_field(name="User ID", value=str(id), inline=True)
        embed.add_field(name="Moderator", value=ctx.message.author, inline=False)
        embed.add_field(name="Reason", value=' '.join(args), inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "unban", "user": str(id), "moderator": str(ctx.message.author.id), "reason": ' '.join(args)})

        await guild.unban(discord.Object(id=id), reason=' '.join(args))
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def mute(self, ctx, user=None, time=None, *args):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        trial_mod_role = guild.get_role(int(role_ids['trial_mod']))
        if mod_role not in ctx.message.author.roles or trial_mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not user:
            await ctx.send("Please mention a user to mute.")
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
            await ctx.send("User is not in the server.")
            return
        member = guild.get_member(id)

        if not time:
            time = "12:00:00"
        elif not re.match(r"\d\d:\d\d:\d\d", time):
            await ctx.send("Please mention the time to mute in the form of `hh:mm:ss`.")
            return
        timeobject = datetime.strptime(time, '%H:%M:%S')
        seconds = timeobject.second + timeobject.minute*60 + timeobject.hour*3600
        fancytime = ""
        if timeobject.hour != 0:
            fancytime = f"{timeobject.hour} hours"
        if timeobject.minute != 0:
            if fancytime != "":
                fancytime = fancytime + ", "
            fancytime = fancytime + f"{timeobject.minute} minutes"
        if timeobject.second != 0:
            if fancytime != "":
                fancytime = fancytime + ", "
            fancytime = fancytime + f"{timeobject.second} seconds"

        if not args:
            args = ['No', 'reason', 'provided.']

        muted_role = guild.get_role(int(role_ids['muted']))
        if muted_role in member.roles:
            await ctx.send(f"{member} is already muted.")
            return

        embed = discord.Embed(title="Mute", color=discord.Color.red())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User muted", value=member, inline=True)
        embed.add_field(name="User ID", value=str(id), inline=True)
        embed.add_field(name="Moderator", value=ctx.message.author, inline=False)
        embed.add_field(name="Time muted", value=fancytime, inline=False)
        embed.add_field(name="Reason", value=' '.join(args), inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "mute", "user": str(id), "moderator": str(ctx.message.author.id), "time": time, "reason": ' '.join(args)})

        dmbed = discord.Embed(title=f"You have been muted for {fancytime}.", description=f"**Reason:** {' '.join(args)}", color=discord.Color.red())
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        dm_failed = False
        try:
            await dm.send(embed=dmbed)
        except:
            dm_failed = True

        if dm_failed == True:
            await ctx.send(f"{member} was muted for {fancytime}. A DM was unable to be sent.")
        else:
            await ctx.send(f"{member} was muted for {fancytime}.")

        await member.add_roles(muted_role)
        await sleep(seconds)
        if not muted_role in member.roles:
            return

        dmbed2 = discord.Embed(title="You have been automatically unmuted.", color=discord.Color.green())
        dm2_failed = False
        try:
            await dm.send(embed=dmbed2)
        except:
            dm_failed = True

        embed2 = discord.Embed(title="Mute Removed", color=discord.Color.green())
        embed2.set_thumbnail(url=member.avatar_url)
        embed2.add_field(name="User unmuted", value=member, inline=True)
        embed2.add_field(name="User ID", value=str(id), inline=True)
        embed2.add_field(name="Reason", value="Automatic unmute", inline=False)
        if dm2_failed == True:
            embed2.set_footer(text="was unable to DM user")
        await channel.send(embed=embed2)
        await member.remove_roles(muted_role)

    @commands.command()
    async def unmute(self, ctx, user=None, *args):
        guild = ctx.message.guild
        mod_role = guild.get_role(int(role_ids['moderator']))
        trial_mod_role = guild.get_role(int(role_ids['trial_mod']))
        if mod_role not in ctx.message.author.roles or trial_mod_role not in ctx.message.author.roles:
            await ctx.send("You do not have permission to run this command.")
            return

        if not user:
            await ctx.send("Please mention a user to unmute.")
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
            await ctx.send("User is not in the server.")
            return
        member = guild.get_member(id)

        if not args:
            args = ['No', 'reason', 'provided.']

        muted_role = guild.get_role(int(role_ids['muted']))
        if not muted_role in member.roles:
            await ctx.send(f"{member} is not muted.")
            return

        embed = discord.Embed(title="Mute Removed", color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="User unmuted", value=member, inline=True)
        embed.add_field(name="User ID", value=str(id), inline=True)
        embed.add_field(name="Moderator", value=ctx.message.author, inline=False)
        embed.add_field(name="Reason", value=' '.join(args), inline=False)
        channel = self.bot.get_channel(int(channel_ids['staff_logs']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "unmute", "user": str(id), "moderator": str(ctx.message.author.id), "reason": ' '.join(args)})

        dmbed = discord.Embed(title="You have been unmuted.", description=f"**Reason:** {' '.join(args)}", color=discord.Color.green())
        if member.dm_channel is None:
            dm = await member.create_dm()
        else:
            dm = member.dm_channel
        dm_failed = False
        try:
            await dm.send(embed=dmbed)
        except:
            dm_failed = True

        if dm_failed == True:
            await ctx.send("The member was warned successfully, but a DM was unable to be sent.")
        else:
            await ctx.message.add_reaction("✅")
        await member.remove_roles(muted_role)

def setup(bot):
    bot.add_cog(moderation(bot))
