from discord.ext import commands
import discord
import yaml

class listeners(commands.Cog):
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
    global role_ids
    role_ids = config['role_ids']

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        global invites
        invites = await guild.invites()

    @commands.Cog.listener()
    async def on_message(self, message):
        support_channels = [int(channel_ids['vc_chat'])]
        for channel in channel_ids:
            if channel.endswith("support"):
                support_channels.append(int(channel_ids[channel]))
        help_triggers = ["issue", "able to help", "get some help", "need help"]

        swore = ""
        for swear in swears:
            if swear in message.content:
                swore = swear

        if isinstance(message.channel, discord.channel.DMChannel):
            if message.author.bot:
                return
            embed = discord.Embed(title="DM", color=discord.Color.red())
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="Message Author", value=message.author, inline=True)
            embed.add_field(name="User ID", value=message.author.id, inline=True)
            if message.content:
                embed.add_field(name="Message:", value=message.content, inline=False)
            else:
                embed.add_field(name="Message:", value="Unable to detect message contents", inline=False)
            channel = self.bot.get_channel(int(channel_ids['bot_dm']))
            await channel.send(embed=embed)

        elif swore != "":
            await message.delete()
            if swore == "@everyone":
                dmbed=discord.Embed(title="@everyone ping", description="Please don't ping @everyone. If you need help, go to a support channel and ping @Support Team.")
                embed=discord.Embed(title="@everyone ping by " + str(message.author), color=0x00a0a0)
            if swore == "@here":
                dmbed=discord.Embed(title="@here ping", description="Please don't ping @here. If you need help, go to a support channel and ping @Support Team.")
                embed=discord.Embed(title="@here ping by " + str(message.author), color=0x00a0a0)
            elif swore == "discord.gg" or swore == "discord.com/invite":
                dmbed=discord.Embed(title="Invite Link", description="Please don't send invite links to other servers, it is against rule 6 of our server.")
                embed=discord.Embed(title="Invite Link sent by " + str(message.author), color=0x00a0a0)
            else:
                dmbed=discord.Embed(title="Swear", description="TSC is a PG Friendly server, you cannot swear here.")
                dmbed.add_field(name="Swear Detected:", value=swore, inline=False)
                embed=discord.Embed(title="Swear by " + str(message.author), color=0x00a0a0)
                embed.add_field(name="Swear Detected:", value=swore, inline=False)

            dm = await message.author.create_dm()
            dmbed.set_thumbnail(url=message.author.avatar_url)
            dmbed.add_field(name="Message Deleted:", value=message.content, inline=False)
            dm_failed = False
            try:
                await dm.send(embed=dmbed)
            except:
                dm_failed = True

            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
            embed.add_field(name="In channel", value=message.channel.mention, inline=False)
            embed.add_field(name="User ID", value=message.author.id, inline=False)
            if dm_failed == True:
                embed.set_footer(text="was not able to DM user")
            channel = self.bot.get_channel(int(channel_ids['filter_log']))
            await channel.send(embed=embed)

        elif any(trigger in message.content for trigger in help_triggers) and not message.channel.id in support_channels:
            channel = self.bot.get_channel(message.channel.id)
            await channel.send(f"If you're looking for help please go to a support channel like <#{channel_ids['general_support']}> and ping the <@&{role_ids['support_team']}>.", allowed_mentions=discord.AllowedMentions(roles=False))

        elif "reinstall windows" in message.content:
            channel = self.bot.get_channel(message.channel.id)
            await channel.send("This tutorial will lead you how to do a fresh windows installation: (All your data will be gone, back it up and use `!key` in case you need to back up your Product Key too, please save it somewhere safe and don't show us or anyone the key!)\nhttps://youtu.be/bwJ_E-I9WRs\nTo figure out which key you need to use to boot to a usb, run the command `!bootkeys`.")

        elif "virus" in message.content:
            if not message.author.bot:
                channel = self.bot.get_channel(message.channel.id)
                await channel.send("We suggest you to check for viruses and suspicious processes with Malwarebytes: https://malwarebytes.com/mwb-download/thankyou/")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(int(channel_ids['message_deleted']))
        if message.channel == channel:
            return
        embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="In channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Message Author", value=message.author, inline=True)
        embed.add_field(name="User ID", value=message.author.id, inline=True)
        if message.content:
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
        else:
            embed.add_field(name="Message Deleted:", value="Unable to detect message contents", inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        embed = discord.Embed(title="Message Edited", color=0x00a0a0)
        embed.set_thumbnail(url=before.author.avatar_url)
        embed.add_field(name="In channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Message Author", value=before.author, inline=True)
        embed.add_field(name="User ID", value=before.author.id, inline=True)
        if before.content:
            beforecontent = before.content
        else:
            beforecontent = "Unable to detect message contents"
        embed.add_field(name="Original Message:", value=beforecontent, inline=False)
        if after.content:
            aftercontent = after.content
        else:
            aftercontent = "Unable to detect message contents"
        embed.add_field(name="Edited Message:", value=aftercontent, inline=False)
        channel = self.bot.get_channel(int(channel_ids['message_edit']))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            embed = discord.Embed(title="Nickname changed/added", color=0x00a0a0)
            embed.set_author(name=before, icon_url=before.avatar_url)
            if before.nick is None:
                beforenick = before.name
            else:
                beforenick = before.nick
            embed.add_field(name="Old Nickname:", value=beforenick, inline=True)
            if after.nick is None:
                afternick = after.name
            else:
                afternick = after.nick
            embed.add_field(name="New Nickname:", value=afternick, inline=True)
            embed.add_field(name="User ID:", value=before.id, inline=False)
            channel = self.bot.get_channel(int(channel_ids['name_changed']))
            await channel.send(embed=embed)

        if len(before.roles) < len(after.roles):
            delta = [role for role in after.roles if role not in before.roles]
            embed = discord.Embed(title="Role Added", description=delta[0].mention, color=discord.Color.green())
            embed.set_author(name=before, icon_url=before.avatar_url)
            channel = self.bot.get_channel(int(channel_ids['role_changed']))
            await channel.send(embed=embed)
        if len(before.roles) > len(after.roles):
            delta = [role for role in before.roles if role not in after.roles]
            embed = discord.Embed(title="Role Removed", description=delta[0].mention, color=discord.Color.red())
            embed.set_author(name=before, icon_url=before.avatar_url)
            channel = self.bot.get_channel(int(channel_ids['role_changed']))
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title="Channel Created", color=discord.Color.green())
        embed.add_field(name="Channel", value=channel.mention, inline=True)
        embed.add_field(name="Channel Name", value=channel.name, inline=True)
        logchannel = self.bot.get_channel(int(channel_ids['channel_created']))
        await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title="Channel Deleted", description=f"Channel name: `{channel.name}`", color=discord.Color.red())
        logchannel = self.bot.get_channel(int(channel_ids['channel_deleted']))
        await logchannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = discord.Embed(title="Role Deleted", description=f"Role name: `{role.name}`", color=discord.Color.red())
        channel = self.bot.get_channel(int(channel_ids['role_deleted']))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global invites

        await member.add_roles(member.guild.get_role(int(role_ids['Mrole'])))

        embed1 = discord.Embed(title="Member Joined", description=f"{member} has joined Tech Support Central!", color=discord.Color.green())
        embed1.set_thumbnail(url=member.avatar_url)
        welcome = self.bot.get_channel(int(channel_ids['welcome']))
        await welcome.send(embed=embed1)

        embed2 = discord.Embed(title="Member Joined", description=member, color=discord.Color.green())
        embed2.set_thumbnail(url=member.avatar_url)
        embed2.add_field(name="User ID", value=member.id, inline=False)
        embed2.add_field(name="Account Created:", value=member.created_at.strftime("%-d %B %Y at %-H:%M"), inline=True)
        embed2.add_field(name="Joined Server:", value=member.joined_at.strftime("%-d %B %Y at %-H:%M"), inline=True)
        joined = self.bot.get_channel(int(channel_ids['joined']))
        await joined.send(embed=embed2)

        def findinvite(list, code):
            for invite in list:
                if invite.code == code:
                    return invite
        afterinvites = await member.guild.invites()
        for invite in invites:
            if invite.uses < findinvite(afterinvites, invite.code).uses:

                embed3 = discord.Embed(title=member, color=discord.Color.green())
                embed3.add_field(name="Invited by", value=invite.inviter, inline=False)
                embed3.add_field(name="Invite code", value=invite.code, inline=False)
                embed3.add_field(name="Invite uses", value=invite.uses, inline=False)
                inviteschannel = self.bot.get_channel(int(channel_ids['invites']))
                await inviteschannel.send(embed=embed3)

                invites = afterinvites
                return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Member Left", description=f"{member} has left Tech Support Central.", color=discord.Color.red())
        embed.set_thumbnail(url=member.avatar_url)
        channel = self.bot.get_channel(int(channel_ids['left']))
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(listeners(bot))
