from discord.ext import commands
import discord
import yaml
from asyncio import sleep
from datetime import datetime
import re
from main import get_database
mongodb = get_database()

async def seconds_to_fancytime(seconds, granularity):
    result = []
    intervals = (
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    if len(result) > 1:
        result[-1] = "and " + result[-1]
    if len(result) < 3:
        return ' '.join(result[:granularity])
    else:
        return ', '.join(result[:granularity])

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global channel_ids
    channel_ids = config['channel_ids']
    global role_ids
    role_ids = config['role_ids']

    @commands.command()
    async def alert(self, ctx, *, description=None):
        if description:
            alert = description
        else:
            alert = "A description was not provided."
        embed = discord.Embed(title="Moderator Alert", description=f"[Jump to message]({ctx.message.jump_url})\n{alert}", color=discord.Color.red())
        embed.add_field(name="Alert Author", value=ctx.message.author, inline=True)
        embed.add_field(name="User ID", value=ctx.message.author.id, inline=True)
        channel = self.bot.get_channel(int(channel_ids['modtalk']))
        await channel.send(f"<@&{role_ids['moderator']}> <@&{role_ids['trial_mod']}>", embed=embed)
        await ctx.send("The moderators have been alerted.")

    @commands.command()
    async def suggest(self, ctx, *, suggestion=None):
        if not suggestion:
            await ctx.send("Please provide a suggestion.")
            return
        embed = discord.Embed(description=f"**Suggestion:** {suggestion}", color=discord.Color.lighter_grey())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Status", value="Pending")
        channel = self.bot.get_channel(int(channel_ids['suggestions_list']))
        await channel.send(embed=embed)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def remindme(self, ctx, time=None, *, reminder=None):
        if not time:
            await ctx.send("Please specify the time you would like to be reminded in.")
            return
        if not reminder:
            reminder = "No description provided."
        gran = 0
        for char in time:
            gran += char.isalpha()
        if gran > 4:
            await ctx.send("The time you mentioned for me to remind you in is not in the correct format.\nIt should look something like `1d2h3m4s` (1 day, 2 hours, 3 minutes, and 4 seconds).")
            return
        cooltime = [int(a[ :-1]) if a else b for a,b in zip(re.search('(\d+d)?(\d+h)?(\d+m)?(\d+s)?', time).groups(), [0, 0, 0, 0])]
        seconds = cooltime[0]*86400 + cooltime[1]*3600 + cooltime[2]*60 + cooltime[3]
        fancytime = await seconds_to_fancytime(seconds, gran)

        await ctx.send(f"I will remind you in {fancytime}.")
        await sleep(seconds)
        embed = discord.Embed(title=f"Reminder from {fancytime} ago:", description=f"{reminder}\n\n[link to original message]({ctx.message.jump_url})", color=0x00a0a0)
        if ctx.message.author.dm_channel is None:
            dm = await ctx.message.author.create_dm()
        else:
            dm = ctx.message.author.dm_channel
        await dm.send(embed=embed)

    @commands.command()
    async def shorten(self, ctx, link=None):
        if not link:
            await ctx.send("Please specify a link to shorten.")
            return

        if re.search(r"https?:\/\/(www\.)?amazon\.[^\/]*", link) and re.search(r"\/dp\/B0[\dA-Z]{8}\/", link):
            amazon = re.search(r"amazon\.[^\/]*", link).group()
            dp = re.search(r"\/dp\/B0[0-9A-Z]{8}\/", link).group()
            await ctx.send("https://" + amazon + dp)

        elif re.search(r"https?:\/\/(www\.)?youtube\.com", link) and re.search(r"(\?|&)v=[\d\w-]{11}", link):
            v = re.search(r"(\?|&)v=[\d\w-]{11}", link).group()[3:]

            if re.search(r"(\?|&)t=\d+", link):
                t = "&" + re.search(r"(\?|&)t=\d+", link).group()[1:]
            else:
                t = ""

            await ctx.send("https://youtu.be/" + v + t)

    @commands.Cog.listener(name="on_message")
    async def matrix_moderation(self, message):
        if message.author.discriminator != "0000" or message.channel.id != int(channel_ids['modtalk']):
            return

        async def userinfo(self, message):
            guild = message.guild

            if len(message.content.split(" ")) >= 2:
                arg = message.content.split(" ")[1]
            else:
                await message.channel.send("You can't do a userinfo on yourself, since you're a Matrix user.")
                return

            if "<@" in arg:
                id = arg
                id = id.replace("<", "")
                id = id.replace(">", "")
                id = id.replace("@", "")
                id = id.replace("!", "")
                id = int(id)
            elif arg.isdigit():
                id = int(arg)
            else:
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            if guild.get_member(id) is None:
                await message.channel.send("User is not in the server.")
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
            await message.channel.send(embed=embed)

        async def warnings(self, message):
            guild = message.guild

            if len(message.content.split(" ")) >= 2:
                arg = message.content.split(" ")[1]
            else:
                await message.channel.send("Please mention a user to check the warnings of.")
                return

            if "<@" in arg:
                id = arg
                id = id.replace("<", "")
                id = id.replace(">", "")
                id = id.replace("@", "")
                id = id.replace("!", "")
                id = int(id)

            elif arg.isdigit():
                id = int(arg)

            else:
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            if guild.get_member(id) is None:
                description = ""
            else:
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
                await message.channel.send("This user has no warnings.")
                return
            await message.channel.send(embed=embed)

        async def warn(self, message):
            guild = message.guild

            args = message.content.split(" ")
            if len(args) < 2:
                await message.channel.send("Please mention a user to warn.")
                return
            user = args[1]
            if len(args) >= 3:
                reason = args[2:].join(" ")
            else:
                reason = "No reason provided."

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
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            if guild.get_member(id) is None:
                await message.channel.send("User is not in the server.")
                return
            member = guild.get_member(id)

            if member.bot:
                await message.channel.send("You cannot warn bots.")
                return

            channel = self.bot.get_channel(int(channel_ids['modlog']))
            warn_message = await channel.send(".")
            embed = discord.Embed(title="Warning", description=f"Use `!unwarn {warn_message.id} <reason>` to remove this warning. Note: This is not the user's ID, rather the ID of this message.", color=discord.Color.red())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User warned", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author.name} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await warn_message.edit(content="", embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "warn", "user": str(id), "moderator": f"{message.author.name} (matrix)", "reason": reason})

            dmbed = discord.Embed(title="You have been warned.", description=f"**Reason:** {reason}", color=discord.Color.red())
            if member.dm_channel is None:
                dm = await member.create_dm()
            else:
                dm = member.dm_channel
            try:
                await dm.send(embed=dmbed)
            except:
                await message.channel.send("The member was warned successfully, but a DM was unable to be sent.")
                return
            await message.add_reaction("✅")

        async def unwarn(self, message):
            guild = message.guild

            args = message.content.split(" ")
            if len(args) < 2:
                await message.channel.send("Please mention the ID of a warn message to remove.")
                return
            id = args[1]
            if len(args) >= 3:
                reason = args[2:].join(" ")
            else:
                reason = "No reason provided."

            if not id.isdigit():
                await message.channel.send("Warns have to be in the form of a Message ID.")
                return

            collection = mongodb['moderation']
            found = False
            for warn in collection.find():
                if warn.get('_id') == id:
                        found = True
                        user = warn.get('user')
                        og_reason = warn.get('reason')
            if found == False:
                await message.channel.send("The warn was not found.")
                return
            collection.delete_one({"_id": id})

            member = guild.get_member(int(user))
            embed = discord.Embed(title="Warning Removed", color=discord.Color.green())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User unwarned", value=member, inline=True)
            embed.add_field(name="User ID", value=user, inline=True)
            embed.add_field(name="Moderator", value=f"{message.author.name} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['modlog']))
            await channel.send(embed=embed)

            dmbed = discord.Embed(title="Your warning has been removed.", color=discord.Color.green())
            dmbed.add_field(name="Original reason for warn", value=og_reason, inline=False)
            dmbed.add_field(name="Reason for removal", value=reason, inline=False)
            if member.dm_channel is None:
                dm = await member.create_dm()
            else:
                dm = member.dm_channel
            try:
                await dm.send(embed=dmbed)
            except:
                await message.channel.send("The warn was removed successfully, but a DM was unable to be sent to the original warned user.")
                return
            await message.add_reaction("✅")

        async def kick(self, message):
            guild = message.guild

            args = message.content.split(" ")
            if len(args) < 2:
                await message.channel.send("Please mention a user to kick.")
                return
            user = args[1]
            if len(args) >= 3:
                reason = args[2:].join(" ")
            else:
                reason = "No reason provided."

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
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            if guild.get_member(id) is None:
                await message.channel.send("User is not in the server.")
                return
            member = guild.get_member(id)

            if member.bot:
                await message.channel.send("You cannot kick bots.")
                return

            embed = discord.Embed(title="Kick", color=discord.Color.red())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User kicked", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author.name} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['modlog']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "kick", "user": str(id), "moderator": f"{message.author.name} (matrix)", "reason": reason})

            dmbed = discord.Embed(title="You have been kicked.", description=f"**Reason:** {reason}", color=discord.Color.red())
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
                await message.add_reaction("✅")
            else:
                await message.channel.send("The member was kicked successfully, but a DM was unable to be sent.")
            await guild.kick(member, reason=reason)

        async def ban(self, message):
            guild = message.guild

            args = message.content.split(" ")
            if len(args) < 2:
                await message.channel.send("Please mention a user to ban.")
                return
            user = args[1]
            if len(args) >= 3:
                reason = args[2:].join(" ")
            else:
                reason = "No reason provided."

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
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            if guild.get_member(id) is None:
                member = await self.bot.fetch_user(id)
            else:
                member = guild.get_member(id)

            if not member:
                await message.channel.send("Not a valid discord user.")
                return

            if member.bot:
                await message.channel.send("You cannot ban bots.")
                return

            embed = discord.Embed(title="Ban", color=discord.Color.red())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User banned", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author.name} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['modlog']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "ban", "user": str(id), "moderator": f"{message.author.name} (matrix)", "reason": reason})

            dmbed = discord.Embed(title="You have been banned.", description=f"**Reason:** {reason}", color=discord.Color.red())
            dmbed.set_footer(text="You can appeal your ban at https://www.techsupportcentral.cf/appeal.php")
            if member.dm_channel is None:
                dm = await member.create_dm()
            else:
                dm = member.dm_channel
            dm_failed = False
            try:
                await dm.send(embed=dmbed)
            except:
                dm_failed = True

            await guild.ban(discord.Object(id=id), delete_message_days=0, reason=reason)
            if dm_failed == False:
                await message.add_reaction("✅")
            else:
                await message.channel.send("The member was banned successfully, but a DM was unable to be sent.")

        async def unban(self, message):
            guild = message.guild

            args = message.content.split(" ")
            if len(args) < 2:
                await message.channel.send("Please mention a user to unban.")
                return
            user = args[1]
            if len(args) >= 3:
                reason = args[2:].join(" ")
            else:
                reason = "No reason provided."

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
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            member = await self.bot.fetch_user(id)
            if not member:
                await message.channel.send("Not a valid discord user.")
                return

            embed = discord.Embed(title="Ban Removed", color=discord.Color.green())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User unbanned", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author.name} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['modlog']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "unban", "user": str(id), "moderator": f"{message.author.name} (matrix)", "reason": reason})

            await guild.unban(discord.Object(id=id), reason=reason)
            await message.add_reaction("✅")

        async def mute(self, message):
            guild = message.guild

            args = message.content.split(" ")
            if len(args) < 2:
                await message.channel.send("Please mention a user to mute.")
                return
            user = args[1]
            if len(args) >= 3:
                time = args[2]
            else:
                time = "12h"
            if len(args) >= 4:
                reason = args[3:].join(" ")
            else:
                reason = "No reason provided."

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
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            if guild.get_member(id) is None:
                await message.channel.send("User is not in the server.")
                return
            member = guild.get_member(id)

            if member.bot:
                await message.channel.send("You cannot mute bots.")
                return

            gran = 0
            for char in time:
                gran += char.isalpha()
            if gran > 4:
                await message.channel.send("Please mention the time to mute in a format like `1d2h3m4s` (1 day, 2 hours, 3 minutes, 4 seconds).")
                return
            cooltime = [int(a[ :-1]) if a else b for a,b in zip(re.search('(\d+d)?(\d+h)?(\d+m)?(\d+s)?', time).groups(), [0, 0, 0, 0])]
            seconds = cooltime[0]*86400 + cooltime[1]*3600 + cooltime[2]*60 + cooltime[3]
            fancytime = await seconds_to_fancytime(seconds, gran)

            muted_role = guild.get_role(int(role_ids['muted']))
            if muted_role in member.roles:
                await message.channel.send(f"{member} is already muted.")
                return

            embed = discord.Embed(title="Mute", color=discord.Color.red())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User muted", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author.name} (via matrix)", inline=False)
            embed.add_field(name="Time muted", value=fancytime, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['modlog']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "mute", "user": str(id), "moderator": f"{message.author.name} (matrix)", "time": str(seconds), "reason": reason})

            dmbed = discord.Embed(title=f"You have been muted for {fancytime}.", description=f"**Reason:** {reason}", color=discord.Color.red())
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
                await message.channel.send(f"{member} was muted for {fancytime}. A DM was unable to be sent.")
            else:
                await message.channel.send(f"{member} was muted for {fancytime}.")
                await message.add_reaction("✅")

            await member.add_roles(muted_role)
            await sleep(seconds)
            if not muted_role in member.roles:
                return

            dmbed2 = discord.Embed(title="You have been automatically unmuted.", color=discord.Color.green())
            dm2_failed = False
            try:
                await dm.send(embed=dmbed2)
            except:
                dm2_failed = True

            embed2 = discord.Embed(title="Mute Removed", color=discord.Color.green())
            embed2.set_thumbnail(url=member.avatar_url)
            embed2.add_field(name="User unmuted", value=member, inline=True)
            embed2.add_field(name="User ID", value=str(id), inline=True)
            embed2.add_field(name="Reason", value="Automatic unmute", inline=False)
            if dm2_failed == True:
                embed2.set_footer(text="was unable to DM user")
            await channel.send(embed=embed2)
            await member.remove_roles(muted_role)

        async def unmute(self, message):
            guild = message.guild

            args = message.content.split(" ")
            if len(args) < 2:
                await message.channel.send("Please mention a user to unmute.")
                return
            user = args[1]
            if len(args) >= 3:
                reason = args[2:].join(" ")
            else:
                reason = "No reason provided."

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
                await message.channel.send("Users have to be in the form of an ID or a mention.")
                return

            if guild.get_member(id) is None:
                await message.channel.send("User is not in the server.")
                return
            member = guild.get_member(id)

            muted_role = guild.get_role(int(role_ids['muted']))
            if not muted_role in member.roles:
                await message.channel.send(f"{member} is not muted.")
                return

            embed = discord.Embed(title="Mute Removed", color=discord.Color.green())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User unmuted", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author.name} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['modlog']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "unmute", "user": str(id), "moderator": f"{message.author.name} (matrix)", "reason": reason})

            dmbed = discord.Embed(title="You have been unmuted.", description=f"**Reason:** {reason}", color=discord.Color.green())
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
                await message.channel.send("The member was warned successfully, but a DM was unable to be sent.")
            else:
                await message.add_reaction("✅")
            await member.remove_roles(muted_role)

        if message.content.startswith("d!userinfo"):
            await userinfo(self, message)
        elif message.content.startswith("d!warnings"):
            await warnings(self, message)
        elif message.content.startswith("d!warn "):
            await warn(self, message)
        elif message.content.startswith("d!unwarn"):
            await unwarn(self, message)
        elif message.content.startswith("d!kick"):
            await kick(self, message)
        elif message.content.startswith("d!ban"):
            await ban(self, message)
        elif message.content.startswith("d!unban"):
            await unban(self, message)
        elif message.content.startswith("d!mute"):
            await mute(self, message)
        elif message.content.startswith("d!unmute"):
            await unmute(self, message)

def setup(bot):
    bot.add_cog(misc(bot))
