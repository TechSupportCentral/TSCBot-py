from discord.ext import commands
import discord
import yaml
from asyncio import sleep
from time import time
from calendar import timegm
from pypartpicker import Scraper, get_list_links
from main import get_database
mongodb = get_database()

class listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    global bumptimer
    bumptimer = False

    global swears
    swears = []
    swearcol = mongodb['swears']
    for swear in swearcol.find():
        swears.append(swear['swear'])

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global pcpp_cookie
    pcpp_cookie = config['pcpp_cookie']
    global channel_ids
    channel_ids = config['channel_ids']
    global support_channel_names
    support_channel_names = config['support_channels']
    global public_channel_names
    public_channel_names = config['public_channels']
    global role_ids
    role_ids = config['role_ids']
    global message_ids
    message_ids = config['message_ids']

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        global invites
        invites = await guild.invites()
        print('Remember to set the bump timer.')

    @commands.Cog.listener()
    async def on_message(self, message):
        global bumptimer
        global swears
        help_triggers = ["issue", "able to help", "get some help", "need help"]
        owner_role = self.bot.guilds[0].get_role(int(role_ids['owner']))

        support_channels = []
        for channel in support_channel_names:
            support_channels.append(int(channel_ids[channel]))
        public_channels = []
        for channel in public_channel_names:
            public_channels.append(int(channel_ids[channel]))

        swore = ""
        for swear in swears:
            if swear in message.content.lower():
                swore = swear

        if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
            embed = discord.Embed(title="DM Received", color=discord.Color.red())
            embed.set_thumbnail(url=message.author.display_avatar)
            embed.add_field(name="Message Author", value=message.author.name, inline=True)
            embed.add_field(name="User ID", value=message.author.id, inline=True)
            if message.content:
                embed.add_field(name="Message:", value=message.content, inline=False)
                if len(message.attachments) >= 1:
                    value = ""
                    for file in message.attachments:
                        value += file.url + "\n"
                    embed.add_field(name="Attachments:", value=value, inline=False)
            elif len(message.attachments) >= 1:
                if "image" in message.attachments[0].content_type:
                    if len(message.attachments) == 1:
                        if message.attachments[0].description is None:
                            value = ""
                        else:
                            value = message.attachments[0].description
                        embed.add_field(name="Image:", value=value, inline=False)
                        embed.set_image(url=message.attachments[0].url)
                    else:
                        value = ""
                        for image in message.attachments:
                            value += image.url + "\n"
                        embed.add_field(name="Images:", value=value, inline=False)
                else:
                    value = ""
                    for file in message.attachments:
                        value += file.url + "\n"
                    embed.add_field(name="Files:", value=value, inline=False)
            elif len(message.stickers) >= 1:
                if len(message.stickers) == 1:
                    embed.add_field(name="Sticker:", value=message.stickers[0].name, inline=False)
                    embed.set_image(url=message.stickers[0].url)
                else:
                    value = ""
                    for sticker in message.stickers:
                        value += sticker.url + "\n"
                    embed.add_field(name="Stickers:", value=value, inline=False)
            else:
                embed.add_field(name="Message:", value="Unable to detect message contents", inline=False)
            channel = self.bot.get_channel(int(channel_ids['bot_dm']))
            await channel.send(embed=embed)
        elif swore != "" and message.channel.id in public_channels and not owner_role in message.author.roles and not isinstance(message.channel, discord.Thread):
            await message.delete()

            if swore == "@everyone":
                dmbed=discord.Embed(title="@everyone ping", description="Please don't ping @everyone. If you need help, go to a support channel and ping @Support Team.", color=discord.Color.red())
                embed=discord.Embed(title="@everyone ping by " + str(message.author), description=f"[Jump to message]({message.jump_url})", color=discord.Color.red())
            elif swore == "@here":
                dmbed=discord.Embed(title="@here ping", description="Please don't ping @here. If you need help, go to a support channel and ping @Support Team.", color=discord.Color.red())
                embed=discord.Embed(title="@here ping by " + str(message.author), description=f"[Jump to message]({message.jump_url})", color=discord.Color.red())
            elif swore == "discord.gg" or swore == "discord.com/invite":
                dmbed=discord.Embed(title="Invite Link", description="Please don't send invite links; it is against rule 6 of our server.", color=discord.Color.red())
                embed=discord.Embed(title="Invite Link sent by " + str(message.author), description=f"[Jump to message]({message.jump_url})", color=discord.Color.red())
            else:
                dmbed=discord.Embed(title="Swear", description="This is a PG Friendly server, you cannot swear here.", color=discord.Color.red())
                dmbed.add_field(name="Swear Detected:", value=swore, inline=False)
                embed=discord.Embed(title="Swear by " + str(message.author.name), description=f"[Jump to message]({message.jump_url})", color=discord.Color.red())
                embed.add_field(name="Swear Detected:", value=swore, inline=False)

            dmbed.set_thumbnail(url=message.author.display_avatar)
            dmbed.add_field(name="Message Deleted:", value=message.content, inline=False)
            dm_failed = False
            try:
                await message.author.send(embed=dmbed)
            except:
                dm_failed = True

            embed.set_thumbnail(url=message.author.display_avatar)
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
            embed.add_field(name="In channel", value=message.channel.mention, inline=False)
            embed.add_field(name="User ID", value=message.author.id, inline=False)
            if dm_failed:
                embed.set_footer(text="was not able to DM user")
            channel = self.bot.get_channel(int(channel_ids['filter_log']))
            await channel.send(embed=embed)

        elif any(trigger in message.content.lower() for trigger in help_triggers) and message.channel.id in public_channels and message.channel.id not in support_channels:
            channel = self.bot.get_channel(message.channel.id)
            notice = await channel.send(f"If you're looking for help please go to a support channel like <#{channel_ids['general_support']}> and ping the <@&{role_ids['support_team']}>.", allowed_mentions=discord.AllowedMentions(roles=False))
            await sleep(10)
            await notice.delete()

        elif " virus" in message.content.lower() and message.channel.id in public_channels and "malwarebytes" not in message.content.lower() and not message.author.bot:
            channel = self.bot.get_channel(message.channel.id)
            notice = await channel.send("We suggest you to check for viruses and suspicious processes with Malwarebytes: https://malwarebytes.com/mwb-download")
            await sleep(10)
            await notice.delete()

        elif message.author.id == 302050872383242240:
            if ":thumbsup:" in message.embeds[0].description:
                embed = discord.Embed(title="Thank you for bumping the server!", description="Vote for Tech Support Central on top.gg at https://top.gg/servers/824042976371277884", color=0x00a0a0)
                await message.channel.send(embed=embed)
                if not bumptimer:
                    bumptimer = True
                    await sleep(7200)
                    bumptimer = False
                    await message.channel.send(f"Time to bump the server!\n<@&{role_ids['bump_reminders']}>, could someone please run `/bump`?")

        elif message.content.startswith("set bump"):
            if bumptimer:
                await message.channel.send("The bump timer is already set.")
            else:
                await message.delete()
                if "now" not in message.content:
                    response = await message.channel.send("Bump timer set. Bump Reminders will ping in 2 hours.")
                    await sleep(2)
                    await response.delete()

                    bumptimer = True
                    await sleep(7198)
                    bumptimer = False
                await message.channel.send(f"Time to bump the server!\n<@&{role_ids['bump_reminders']}>, could someone please run `/bump`?")

        elif "reload swears" in message.content:
            if message.author.bot or owner_role in message.author.roles:
                await message.delete()
                swears = []
                swearcol = mongodb['swears']
                for swear in swearcol.find():
                    swears.append(swear['swear'])
            else:
                response = await message.channel.send("I'm sorry Dave, I'm afraid I can't do that.")
                await sleep(2)
                await message.delete()
                await response.delete()

        elif len(get_list_links(message.content)) >= 1:
            pcpp = Scraper(headers={"cookie": pcpp_cookie, "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"})

            for link in get_list_links(message.content):
                list = pcpp.fetch_list(link)

                description = ""
                for part in list.parts:
                    description += f"**{part.type}:** {part.name} **({part.price})**\n"
                description += f"\n**Estimated Wattage:** {list.wattage}\n**Price:** {list.total}"

                embed = discord.Embed(title="PCPartPicker List", url=link, description=description, color=0x00a0a0)
                await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(int(channel_ids['message_deleted']))
        if message.content.startswith("reload") or message.author.bot or message.guild.get_role(int(role_ids['owner'])) in message.author.roles:
            return
        embed = discord.Embed(title="Message Deleted", description=f"[Jump to message]({message.jump_url})", color=discord.Color.red())
        embed.set_thumbnail(url=message.author.display_avatar)
        embed.add_field(name="In channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Message Author", value=message.author.name, inline=True)
        embed.add_field(name="User ID", value=message.author.id, inline=True)
        if message.content:
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
        else:
            embed.add_field(name="Message Deleted:", value="Unable to detect message contents", inline=False)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content or before.author.bot or before.guild.get_role(int(role_ids['owner'])) in before.author.roles:
            return
        embed = discord.Embed(title="Message Edited", description=f"[Jump to message]({before.jump_url})", color=0x00a0a0)
        embed.set_thumbnail(url=before.author.display_avatar)
        embed.add_field(name="In channel", value=before.channel.mention, inline=False)
        embed.add_field(name="Message Author", value=before.author.name, inline=True)
        embed.add_field(name="User ID", value=before.author.id, inline=True)
        if before.content:
            embed.add_field(name="Original Message:", value=before.content, inline=False)
        else:
            embed.add_field(name="Original Message:", value="Unable to detect message contents", inline=False)
        if after.content:
            embed.add_field(name="Edited Message:", value=after.content, inline=False)
        else:
            embed.add_field(name="Edited Message:", value="Unable to detect message contents", inline=False)
        channel = self.bot.get_channel(int(channel_ids['message_edit']))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            embed = discord.Embed(title="Nickname changed/added", color=0x00a0a0)
            embed.set_author(name=before.name, icon_url=before.display_avatar)
            embed.add_field(name="Old Nickname:", value=before.nick, inline=True)
            embed.add_field(name="New Nickname:", value=after.nick, inline=True)
            embed.add_field(name="User ID:", value=before.id, inline=False)
            channel = self.bot.get_channel(int(channel_ids['name_changed']))
            await channel.send(embed=embed)

        if len(before.roles) < len(after.roles):
            delta = [role for role in after.roles if role not in before.roles]
            role = delta[0]
            guild = role.guild

            if role.id == int(role_ids['support_team']):
                aembed = discord.Embed(title="New Support Team Member", description=f"Welcome {before.mention} to the Support Team!", color=role.color)
                aembed.set_author(name=before.global_name)
                aembed.set_thumbnail(url=before.display_avatar)
                achannel = self.bot.get_channel(int(channel_ids['new_staff']))
                await achannel.send(embed=aembed)
            if role.id == int(role_ids['trial_mod']) or role.id == int(role_ids['moderator']):
                aembed = discord.Embed(title=f"New {role.name}", description=f"Welcome {before.mention} to the Moderation Team!", color=role.color)
                aembed.set_author(name=before.global_name)
                aembed.set_thumbnail(url=before.display_avatar)
                achannel = self.bot.get_channel(int(channel_ids['new_staff']))
                await achannel.send(embed=aembed)
            embed = discord.Embed(title="Role Added", description=role.mention, color=discord.Color.green())
            embed.set_author(name=before.name, icon_url=before.display_avatar)
            channel = self.bot.get_channel(int(channel_ids['role_changed']))
            await channel.send(embed=embed)
        elif len(before.roles) > len(after.roles):
            delta = [role for role in before.roles if role not in after.roles]
            embed = discord.Embed(title="Role Removed", description=delta[0].mention, color=discord.Color.red())
            embed.set_author(name=before.name, icon_url=before.display_avatar)
            channel = self.bot.get_channel(int(channel_ids['role_changed']))
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global invites

        await member.add_roles(member.guild.get_role(int(role_ids['og'])))

        embed1 = discord.Embed(title="Member Joined", description=f"{member.global_name} has joined Tech Support Central!", color=discord.Color.green())
        embed1.set_thumbnail(url=member.display_avatar)
        channel1 = self.bot.get_channel(int(channel_ids['welcome']))
        await channel1.send(embed=embed1)

        def findinvite(list, code):
            for invite in list:
                if invite.code == code:
                    return invite
        afterinvites = await member.guild.invites()
        invite_used = None
        for invite in afterinvites:
            if invite.uses > findinvite(invites, invite.code).uses:
                invite_used = invite
                invites = afterinvites

        embed2 = discord.Embed(title="Member Joined", description=member.name, color=discord.Color.green())
        embed2.set_thumbnail(url=member.display_avatar)
        embed2.add_field(name="User ID", value=member.id, inline=False)
        embed2.add_field(name="Account Created:", value=f"<t:{timegm(member.created_at.timetuple())}>", inline=False)
        if invite_used is not None:
                embed2.add_field(name="Invite code", value=invite_used.code, inline=False)
                if invite_used.code == "2vwUBmhM8U":
                    embed2.add_field(name="Invite maker", value="top.gg", inline=True)
                else:
                    embed2.add_field(name="Invite maker", value=invite_used.inviter, inline=True)
                embed2.add_field(name="Invite uses", value=invite_used.uses, inline=True)
        channel2 = self.bot.get_channel(int(channel_ids['member_changed']))
        await channel2.send(embed=embed2)

        collection = mongodb['moderation']
        found = False
        for mute in collection.find({"type": "mute"}):
            end = int(mute['start']) + int(mute['time'])
            now = time()
            if int(mute['user']) == member.id and end > now:
                found = True
        if found:
            muted_role = member.guild.get_role(int(role_ids['muted']))
            await member.add_roles(muted_role)

            if member.dm_channel is None:
                dm = await member.create_dm()
            else:
                dm = member.dm_channel
            await dm.send("Nice try; you cannot escape a mute by leaving and rejoining the server.")

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        global invites
        invites = await invite.guild.invites()

        if invite.inviter == None:
            return
        embed = discord.Embed(title="Invite Created", color=discord.Color.green())
        embed.add_field(name="Invite Creator", value=invite.inviter.name, inline=True)
        embed.add_field(name="User ID", value=invite.inviter.id, inline=True)
        embed.add_field(name="Invite Code", value=invite.code, inline=False)
        embed.add_field(name="Invite Channel", value=invite.channel.mention, inline=False)
        inviteschannel = self.bot.get_channel(int(channel_ids['invites']))
        await inviteschannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        global invites
        invites = await invite.guild.invites()
        embed = discord.Embed(title="Invite Deleted", color=discord.Color.red())
        if invite.inviter is not None:
            embed.add_field(name="Invite Creator", value=invite.inviter.name, inline=True)
            embed.add_field(name="User ID", value=invite.inviter.id, inline=True)
        embed.add_field(name="Invite Code", value=invite.code, inline=False)
        if invite.channel is not None:
            embed.add_field(name="Invite Channel", value=invite.channel.mention, inline=False)
        if invite.uses is not None:
            embed.add_field(name="Invite Uses", value=invite.uses, inline=False)
        inviteschannel = self.bot.get_channel(int(channel_ids['invites']))
        await inviteschannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Member Left", description=f"{member.name} has left Tech Support Central.", color=discord.Color.red())
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text=f"User ID: {member.id}")
        channel = self.bot.get_channel(int(channel_ids['member_changed']))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if payload.message_id == int(message_ids['reaction_role_bump']) and str(payload.emoji) == "✅":
            role = guild.get_role(int(role_ids['bump_reminders']))

            dmessage = f"Added the `{role.name}` role."
            try:
                await user.add_roles(role)
            except:
                dmessage = f"Failed to add the `{role.name}` role. Open a ticket and inform the owners."
            await user.send(dmessage)

        elif payload.message_id == int(message_ids['ticket_create']) and str(payload.emoji) == "🎟️":
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            mod_role = guild.get_role(int(role_ids['moderator']))

            thread = await channel.create_thread(name=f"Ticket for {user.display_name}", invitable=False)
            await thread.add_user(user)
            for mod in mod_role.members:
                await thread.add_user(mod)

            await thread.send(f"{user.mention}, your ticket has been created. Please explain your rationale and wait for a {mod_role.mention} to respond.")
            await message.remove_reaction("🎟️", user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        if payload.message_id == int(message_ids['reaction_role_bump']) and str(payload.emoji) == "✅":
            role = guild.get_role(int(role_ids['bump_reminders']))

            dmessage = f"Removed the `{role.name}` role."
            try:
                await user.remove_roles(role)
            except:
                dmessage = f"Failed to remove the `{role.name}` role. Open a ticket and inform the owners."
            await user.send(dmessage)

async def setup(bot):
    await bot.add_cog(listeners(bot))
