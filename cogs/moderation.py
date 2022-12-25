from discord.ext import commands
import discord
import yaml
from asyncio import sleep
from time import time
from calendar import timegm
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
            result.append(str(value) + " " + name)
    if len(result) > 1:
        result[-1] = "and " + result[-1]
    if len(result) < 3:
        return ' '.join(result[:granularity])
    else:
        return ', '.join(result[:granularity])

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global role_ids
    role_ids = config['role_ids']
    global channel_ids
    channel_ids = config['channel_ids']

    @commands.Cog.listener()
    async def on_ready(self):
        async def resume_mute(self, mute):
            id = int(mute['user'])
            end = int(mute['start']) + int(mute['time'])
            now = time()
            fancytime = await seconds_to_fancytime(int(mute['time']), 4)

            if self.bot.guilds[0].get_member(id) is None:
                return
            user = self.bot.guilds[0].get_member(id)
            muted_role = self.bot.guilds[0].get_role(int(role_ids['muted']))
            channel = self.bot.get_channel(int(channel_ids['modlog']))

            print(f"Resuming mute of {fancytime} for {user}")
            await sleep(end - now)
            if not muted_role in user.roles:
                return

            dmbed = discord.Embed(title="You have been automatically unmuted.", color=discord.Color.green())
            dm_failed = False
            try:
                await user.send(embed=dmbed)
            except:
                dm_failed = True

            embed = discord.Embed(title="Mute Removed", color=discord.Color.green())
            embed.set_thumbnail(url=user.display_avatar)
            embed.add_field(name="User unmuted", value=user, inline=True)
            embed.add_field(name="User ID", value=str(id), inline=True)
            embed.add_field(name="Reason", value="Automatic unmute", inline=False)
            if dm_failed:
                embed.set_footer(text="was unable to DM user")
            await channel.send(embed=embed)
            await user.remove_roles(muted_role)

        collection = mongodb['moderation']
        for mute in collection.find({"type": "mute"}):
            end = int(mute['start']) + int(mute['time'])
            now = time()
            if end > now:
                await resume_mute(self, mute)

    @discord.app_commands.command(description="Delete a certain number of messages")
    @discord.app_commands.guild_only()
    @discord.app_commands.describe(
        messages="Number of messages to delete",
        reason="Reason for deleting the messages"
    )
    async def purge(self, interaction: discord.Interaction, messages: int, reason: str = "No reason provided."):
        if messages > 100:
            await interaction.response.send_message("You can only delete 100 or fewer messages at once.", ephemeral=True)
            return

        embed=discord.Embed(title=f"{messages} Messages Deleted", color=discord.Color.red())
        embed.set_thumbnail(url=interaction.user.display_avatar)
        embed.add_field(name="Deleted by", value=interaction.user, inline=True)
        embed.add_field(name="In channel", value=interaction.channel.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Successfully deleted {messages} messages.", ephemeral=True)
        await interaction.channel.purge(limit=messages)

    @discord.app_commands.command(description="Obtain various info about a certain user")
    @discord.app_commands.guild_only()
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member):
        embed=discord.Embed(title=user, color=0x00a0a0)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User ID", value=user.id, inline=False)
        if user.name != user.display_name:
            embed.add_field(name="Nickname", value=user.display_name, inline=False)

        created = timegm(user.created_at.timetuple())
        joined = timegm(user.joined_at.timetuple())
        created_delta = round(time() - created)
        joined_delta = round(time() - joined)
        if created_delta < 604800:
            created_fancy = await seconds_to_fancytime(created_delta, 2)
        else:
            created_fancy = await seconds_to_fancytime(created_delta, 1)
        if joined_delta < 604800:
            joined_fancy = await seconds_to_fancytime(joined_delta, 2)
        else:
            joined_fancy = await seconds_to_fancytime(joined_delta, 1)
        embed.add_field(name="Account Created:", value=f"<t:{created}> ({created_fancy} ago)", inline=True)
        embed.add_field(name="Joined Server:", value=f"<t:{joined}> ({joined_fancy} ago)", inline=True)
        if joined - created < 604800:
            embed.add_field(name="Difference between creation and join:", value=await seconds_to_fancytime(joined - created, 2), inline=False)

        mentions = []
        for role in user.roles:
            if role.name != "@everyone":
                mentions.append(role.mention)
        roles = ", ".join(mentions)
        embed.add_field(name="Roles", value=roles, inline=False)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(description="Check a user's punishments")
    @discord.app_commands.guild_only()
    async def warnings(self, interaction: discord.Interaction, user: discord.User):
        description = f"**User:** {user}\n"
        collection = mongodb['moderation']
        found = False
        number = 0
        for warning in collection.find():
            if warning['user'] == str(user.id):
                found = True
                number += 1
                description = description + f"\n`{number}`:\n**Type:** {warning['type']}\n**Reason:** {warning['reason']}\n**Moderator:** {interaction.guild.get_member(int(warning['moderator']))}\n**Message ID:** {warning['_id']}\n"
        if not found:
            await interaction.response.send_message("This user has no warnings.")
            return
        embed = discord.Embed(title="Warnings", description=description, color=0x00a0a0)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(description="Give a user a warning")
    @discord.app_commands.guild_only()
    async def warn(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        if user.top_role.position > interaction.user.top_role.position:
            await interaction.response.send_message(f"{user} is higher than you in the role hierarchy, cannot warn.", ephemeral=True)
            return
        if user.bot:
            await interaction.response.send_message("You cannot warn bots.", ephemeral=True)
            return

        channel = self.bot.get_channel(int(channel_ids['modlog']))
        message = await channel.send(".")
        embed = discord.Embed(title="Warning", description=f"Use `/unwarn {message.id} <reason>` to remove this warning. Note: This is not the user's ID, rather the ID of this message.", color=discord.Color.red())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User warned", value=user, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Moderator", value=interaction.user, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await message.edit(content="", embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "warn", "user": str(user.id), "moderator": str(interaction.user.id), "reason": reason})

        dmbed = discord.Embed(title="You have been warned.", description="**Reason:** " + reason, color=discord.Color.red())
        try:
            await user.send(embed=dmbed)
        except:
            await interaction.response.send_message("The user was warned successfully, but a DM was unable to be sent.")
            return
        await interaction.response.send_message("The user was warned successfully.")

    @discord.app_commands.command(description="Remove a specific warning")
    @discord.app_commands.guild_only()
    @discord.app_commands.describe(
        id="ID of the warning to remove",
        reason="Reason to remove the warning"
    )
    async def unwarn(self, interaction: discord.Interaction, id: str, reason: str):
        if not id.isdigit():
            await interaction.response.send_message("Warnings have to be in the form of a Message ID.", ephemeral=True)
            return

        collection = mongodb['moderation']
        found = False
        for warn in collection.find():
            if warn['_id'] == id:
                found = True
                user = warn['user']
                og_reason = warn['reason']
        if not found:
            await interaction.response.send_message("The warn was not found.", ephemeral=True)
            return
        collection.delete_one({"_id": id})

        member = interaction.guild.get_member(int(user))
        embed = discord.Embed(title="Warning Removed", color=discord.Color.green())
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="User unwarned", value=member, inline=True)
        embed.add_field(name="User ID", value=user, inline=True)
        embed.add_field(name="Moderator", value=interaction.user, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        await channel.send(embed=embed)

        dmbed = discord.Embed(title="Your warning has been removed.", color=discord.Color.green())
        dmbed.add_field(name="Original reason for warn", value=og_reason, inline=False)
        dmbed.add_field(name="Reason for removal", value=reason, inline=False)
        try:
            await member.send(embed=dmbed)
        except:
            await interaction.response.send_message("The warn was removed successfully, but a DM was unable to be sent to the original warned user.")
            return
        await interaction.response.send_message("The warning was removed successfully.")

    @discord.app_commands.command(description="Update the reason for a warning")
    @discord.app_commands.guild_only()
    @discord.app_commands.describe(
        id="ID of the warning to update",
        reason="New reason for the warning"
    )
    async def reason(self, interaction: discord.Interaction, id: str, reason: str):
        if not id.isdigit():
            await interaction.response.send_message("Warnings have to be in the form of a Message ID.", ephemeral=True)
            return

        collection = mongodb['moderation']
        found = False
        for warn in collection.find():
            if warn['_id'] == id:
                found = True
                user = warn['user']
                moderator = warn['moderator']
                og_reason = warn['reason']
        if not found:
            await interaction.response.send_message("The warning was not found.", ephemeral=True)
            return
        if interaction.user.id != int(moderator) and interaction.guild.get_role(int(role_ids['owner'])) not in interaction.user.roles:
            await interaction.response.send_message("This is not your warning to change.", ephemeral=True)
            return

        collection.update_one({"_id": id}, {"$set": {"reason": reason}})
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        message = await channel.fetch_message(int(id))
        og_embed = message.embeds[0]
        embed = discord.Embed(title=og_embed.title, description=og_embed.description, color=og_embed.color)
        embed.set_thumbnail(url=og_embed.thumbnail.url)
        for field in og_embed.fields:
            if field.name == "Reason":
                embed.add_field(name="Reason", value=reason, inline=field.inline)
            else:
                embed.add_field(name=field.name, value=field.value, inline=field.inline)
        embed.set_footer(text=og_embed.footer.text)
        await message.edit(embed=embed)

        member = interaction.guild.get_member(int(user))
        if member is None:
            await interaction.response.send_message("The reason was updated successfully, but the user is no longer in the server and thus could not be notified.")
            return
        dmbed = discord.Embed(title="Your warning has been updated.", color=0x00a0a0)
        dmbed.add_field(name="Original reason", value=og_reason, inline=False)
        dmbed.add_field(name="New reason", value=reason, inline=False)
        try:
            await member.send(embed=dmbed)
        except:
            await interaction.response.send_message("The reason was updated successfully, but a DM was unable to be sent to the warned user.")
            return
        await interaction.response.send_message("The reason was updated successfully.")

    @discord.app_commands.command(description="Kick a user from the server")
    @discord.app_commands.guild_only()
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided."):
        if user.top_role.position >= interaction.user.top_role.position:
            await interaction.response.send_message(f"{user} is higher than or equal to you in the role hierarchy, cannot kick.", ephemeral=True)
            return
        if user.bot and interaction.guild.get_role(int(role_ids['owner'])) not in interaction.user.roles:
            await interaction.response.send_message("You do not have permission to kick bots.", ephemeral=True)
            return

        embed = discord.Embed(title="Kick", color=discord.Color.red())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User kicked", value=user, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Moderator", value=interaction.user, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "kick", "user": str(user.id), "moderator": str(interaction.user.id), "reason": reason})

        dmbed = discord.Embed(title="You have been kicked.", description=f"**Reason:** " + reason, color=discord.Color.red())
        dm_failed = False
        try:
            await user.send(embed=dmbed)
        except:
            dm_failed = True

        await interaction.guild.kick(user, reason=reason)
        if dm_failed:
            await interaction.response.send_message("The user was kicked successfully, but a DM was unable to be sent.")
        else:
            await interaction.response.send_message("The user was kicked successfully.")

    @discord.app_commands.command(description="Ban a user from the server")
    @discord.app_commands.guild_only()
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided."):
        if interaction.guild.get_member(user.id) is not None:
            if user.top_role.position >= interaction.user.top_role.position:
                await interaction.response.send_message(f"{user} is higher than or equal to you in the role hierarchy, cannot ban.", ephemeral=True)
                return
            if user.bot and interaction.guild.get_role(int(role_ids['owner'])) not in interaction.user.roles:
                await interaction.response.send_message("You do not have permission to ban bots.", ephemeral=True)
                return

            dmbed = discord.Embed(title="You have been banned.", description=f"**Reason:** " + reason, color=discord.Color.red())
            dmbed.set_footer(text="You can appeal your ban at https://www.techsupportcentral.cf/appeal.php")

            try:
                await user.send(embed=dmbed)
            except:
                pass

        embed = discord.Embed(title="Ban", color=discord.Color.red())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User banned", value=user, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Moderator", value=interaction.user, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "ban", "user": str(user.id), "moderator": str(interaction.user.id), "reason": reason})

        await interaction.guild.ban(discord.Object(id=user.id), delete_message_days=0, reason=reason)
        await interaction.response.send_message("The user was banned successfully.")

    @discord.app_commands.command(description="Unban a user from the server")
    @discord.app_commands.guild_only()
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = "No reason provided."):
        embed = discord.Embed(title="Ban Removed", color=discord.Color.green())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User unbanned", value=user, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Moderator", value=interaction.user, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        message = await channel.send(embed=embed)

        mod_collection = mongodb['moderation']
        mod_collection.insert_one({"_id": str(message.id), "type": "unban", "user": str(user.id), "moderator": str(interaction.user.id), "reason": reason})
        app_collection = mongodb['applications']
        app_collection.update_one({"id": str(user.id), "type": "appeal"}, {"$set": {"accepted": "yes"}})

        await interaction.guild.unban(discord.Object(id=user.id), reason=reason)
        await interaction.response.send_message("The user was unbanned successfully.")

    @discord.app_commands.command(description="Stop a user from sending messages or joining VCs")
    @discord.app_commands.guild_only()
    @discord.app_commands.rename(mutetime="time")
    @discord.app_commands.describe(
        user="User to mute",
        mutetime="Time to mute user for.\nSyntax is `1d2h3m4s` (example of 1 day, 2 hours, 3 minutes, and 4 seconds).",
        reason="Reason for muting user"
    )
    async def mute(self, interaction: discord.Interaction, user: discord.Member, mutetime: str = "12h", reason: str = "No reason provided."):
        if user.top_role.position >= interaction.user.top_role.position:
            await interaction.response.send_message(f"{user} is higher than or equal to you in the role hierarchy, cannot mute.", ephemeral=True)
            return
        if user.bot:
            await interaction.response.send_message("You cannot mute bots.", ephemeral=True)
            return

        gran = 0
        for char in mutetime:
            gran += char.isalpha()
        if gran > 4:
            await interaction.response.send_message("Please mention the time to mute in a format like `1d2h3m4s` (1 day, 2 hours, 3 minutes, 4 seconds).", ephemeral=True)
            return
        cooltime = [int(a[ :-1]) if a else b for a,b in zip(re.search('(\d+d)?(\d+h)?(\d+m)?(\d+s)?', mutetime).groups(), [0, 0, 0, 0])]
        seconds = cooltime[0]*86400 + cooltime[1]*3600 + cooltime[2]*60 + cooltime[3]
        fancytime = await seconds_to_fancytime(seconds, gran)

        muted_role = interaction.guild.get_role(int(role_ids['muted']))
        if muted_role in user.roles:
            await interaction.response.send_message(f"{user} is already muted.", ephemeral=True)
            return

        embed = discord.Embed(title="Mute", color=discord.Color.red())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User muted", value=user, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Moderator", value=interaction.user, inline=False)
        embed.add_field(name="Time muted", value=fancytime, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "mute", "user": str(user.id), "moderator": str(interaction.user.id), "start": str(round(time())), "time": str(seconds), "reason": reason})

        dmbed = discord.Embed(title=f"You have been muted for {fancytime}.", description="**Reason:** " + reason, color=discord.Color.red())
        dm_failed = False
        try:
            await user.send(embed=dmbed)
        except:
            dm_failed = True

        if dm_failed:
            await interaction.response.send_message(f"{user} was muted for {fancytime}. A DM was unable to be sent.")
        else:
            await interaction.response.send_message(f"{user} was muted for {fancytime}.")

        await user.add_roles(muted_role)
        await sleep(seconds)
        if not muted_role in user.roles:
            return

        dmbed2 = discord.Embed(title="You have been automatically unmuted.", color=discord.Color.green())
        dm2_failed = False
        try:
            await user.send(embed=dmbed2)
        except:
            dm2_failed = True

        embed2 = discord.Embed(title="Mute Removed", color=discord.Color.green())
        embed2.set_thumbnail(url=user.display_avatar)
        embed2.add_field(name="User unmuted", value=user, inline=True)
        embed2.add_field(name="User ID", value=user.id, inline=True)
        embed2.add_field(name="Reason", value="Automatic unmute", inline=False)
        if dm2_failed:
            embed2.set_footer(text="was unable to DM user")
        await channel.send(embed=embed2)
        await user.remove_roles(muted_role)

    @discord.app_commands.command(description="Remove a user's mute")
    @discord.app_commands.guild_only()
    async def unmute(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided."):
        muted_role = interaction.guild.get_role(int(role_ids['muted']))
        if not muted_role in user.roles:
            await interaction.response.send_message(f"{user} is not muted.", ephemeral=True)
            return

        embed = discord.Embed(title="Mute Removed", color=discord.Color.green())
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="User unmuted", value=user, inline=True)
        embed.add_field(name="User ID", value=user.id, inline=True)
        embed.add_field(name="Moderator", value=interaction.user, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        message = await channel.send(embed=embed)

        collection = mongodb['moderation']
        collection.insert_one({"_id": str(message.id), "type": "unmute", "user": str(user.id), "moderator": str(interaction.user.id), "reason": reason})

        dmbed = discord.Embed(title="You have been unmuted.", description=f"**Reason:** " + reason, color=discord.Color.green())
        dm_failed = False
        try:
            await user.send(embed=dmbed)
        except:
            dm_failed = True

        await user.remove_roles(muted_role)
        if dm_failed:
            await interaction.response.send_message("The user was unmuted successfully, but a DM was unable to be sent.")
        else:
            await interaction.response.send_message("The user was unmuted successfully.")

async def setup(bot):
    await bot.add_cog(moderation(bot))
