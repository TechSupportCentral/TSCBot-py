from discord.ext import commands
import discord
import yaml
from asyncio import sleep
from datetime import datetime
import re
from main import get_database
mongodb = get_database()

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
    async def alert(self, ctx, *, description):
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
    async def suggest(self, ctx, *, suggestion):
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
    async def d(self, ctx):
        return

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

            channel = self.bot.get_channel(int(channel_ids['staff_logs']))
            warn_message = await channel.send(".")
            embed = discord.Embed(title="Warning", description=f"Use `!unwarn {warn_message.id} <reason>` to remove this warning.", color=discord.Color.red())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User warned", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await warn_message.edit(content="", embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "warn", "user": str(id), "moderator": f"{message.author} (matrix)", "reason": reason})

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
            embed.add_field(name="Moderator", value=f"{message.author} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['staff_logs']))
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
            embed.add_field(name="Moderator", value=f"{message.author} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['staff_logs']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "kick", "user": str(id), "moderator": f"{message.author} (matrix)", "reason": reason})

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
            embed.add_field(name="Moderator", value=f"{message.author} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['staff_logs']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "ban", "user": str(id), "moderator": f"{message.author} (matrix)", "reason": reason})

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
            embed.add_field(name="Moderator", value=f"{message.author} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['staff_logs']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "unban", "user": str(id), "moderator": f"{message.author} (matrix)", "reason": reason})

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
                time = "12:00:00"
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

            elif not re.match(r"\d\d:\d\d:\d\d", time):
                await message.channel.send("Please mention the time to mute in the form of `hh:mm:ss`.")
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

            muted_role = guild.get_role(int(role_ids['muted']))
            if muted_role in member.roles:
                await message.channel.send(f"{member} is already muted.")
                return

            embed = discord.Embed(title="Mute", color=discord.Color.red())
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="User muted", value=member, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Moderator", value=f"{message.author} (via matrix)", inline=False)
            embed.add_field(name="Time muted", value=fancytime, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['staff_logs']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "mute", "user": str(id), "moderator": f"{message.author} (matrix)", "time": time, "reason": reason})

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
            embed.add_field(name="Moderator", value=f"{message.author} (via matrix)", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            channel = self.bot.get_channel(int(channel_ids['staff_logs']))
            warn_message = await channel.send(embed=embed)

            collection = mongodb['moderation']
            collection.insert_one({"_id": str(warn_message.id), "type": "unmute", "user": str(id), "moderator": f"{message.author} (matrix)", "reason": reason})

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
