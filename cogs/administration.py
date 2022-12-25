from discord.ext import commands
import discord
import yaml
import re
import subprocess
from main import get_database
mongodb = get_database()

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
    @commands.has_permissions(administrator=True)
    async def sendmessage(self, ctx, *, message=None):
        if not message:
            await ctx.send("Please specify a message to send.")
            return
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, pingtype=None, *, message=None):
        if not message:
            await ctx.send("Please specify the announcement message.")
            return
        if pingtype == "everyone":
            content = "@everyone"
        elif pingtype == "here":
            content = "@here"
        elif pingtype == "none":
            content = ""
        else:
            await ctx.send("Please specify whether or not you'd like your message to include a ping.\nPossible Values: `everyone`, `here`, `none`\nExample Usage: `!announce everyone hello there`")
            return

        await ctx.message.delete()
        embed=discord.Embed(title="Announcement", description=message, color=0x00a0a0)
        await ctx.send(content=content, embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, user=None, *, message=None):
        if not user:
            await ctx.send("Please specify a user to DM.")
            return
        elif not message:
            await ctx.send("Please specify a DM to send.")
            return

        if re.search(r"<@!?\d+>", user):
            id = int(re.search(r"\d+", user).group())
        elif user.isdigit():
            id = int(user)
        else:
            await ctx.send("Users have to be in the form of an ID or a mention.")
            return
        guild = ctx.message.guild

        member = guild.get_member(id)
        if member is None:
            await ctx.send("User is not in the server.")
            return

        dmbed = discord.Embed(title="Message from the owners of TSC", description=message, color=0x00a0a0)
        try:
            await member.send(embed=dmbed)
        except:
            await ctx.send("Failed to DM the user")
            return

        await ctx.message.add_reaction("✅")
        embed = discord.Embed(title="DM Sent", color=discord.Color.green())
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Sent to", value=member, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Sent by", value=ctx.message.author, inline=False)
        embed.add_field(name="Message:", value=message, inline=False)
        channel = self.bot.get_channel(int(channel_ids['bot_dm']))
        await channel.send(embed=embed)

    @commands.command(name="accept-suggestion")
    @commands.has_permissions(administrator=True)
    async def accept_suggestion(self, ctx, id=None, *, reason=None):
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
        try:
            await member.send(embed=dmbed)
        except:
            await ctx.send("The suggestion was accepted successfully but the the user was unable to be DMed.")
            return

        await ctx.message.add_reaction("✅")

    @commands.command(name="decline-suggestion")
    @commands.has_permissions(administrator=True)
    async def decline_suggestion(self, ctx, id=None, *, reason=None):
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
        try:
            await member.send(embed=dmbed)
        except:
            await ctx.send("The suggestion was declined successfully but the the user was unable to be DMed.")
            return

        await ctx.message.add_reaction("✅")

    @discord.app_commands.command(name="accept-application", description="Accept a staff application")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    @discord.app_commands.describe(
        user="User who submitted the application",
        type="Type of application (support_team or moderator)"
    )
    async def accept_application(self, interaction: discord.Interaction, user: discord.Member, type: str):
        match type:
            case "moderator":
                role = "trial_mod"
            case "support_team":
                role = type
            case _:
                await interaction.response.send_message(f"`{type}` is not a valid application type. Valid types are `support_team` or `moderator`.", ephemeral=True)
                return

        collection = mongodb['applications']
        found = False
        for app in collection.find({"id": str(user.id)}):
            if app['type'] == type:
                found = True
        if not found:
            await interaction.response.send_message(f"`{type}` application for {user} not found.", ephemeral=True)
            return

        collection.update_one({"id": str(user.id), "type": type}, {"$set": {"accepted": "yes"}})
        await user.add_roles(user.guild.get_role(int(role_ids[role])))
        await interaction.response.send_message("Application accepted.")

    @discord.app_commands.command(name="add-swear", description="Add a swear to the swearlist")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    @discord.app_commands.rename(arg="swear")
    async def add_swear(self, interaction: discord.Interaction, arg: str):
        collection = mongodb['swears']
        for swear in collection.find():
            if swear['swear'] == arg:
                await interaction.response.send_message(f"The swear `{arg}` already exists.", ephemeral=True)
                return
        collection.insert_one({"swear": arg})
        await interaction.response.send_message(f"Swear `{arg}` successfully added.")
        await interaction.channel.send("reload swears")

    @discord.app_commands.command(name="remove-swear", description="Remove a swear from the swearlist")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    @discord.app_commands.rename(arg="swear")
    async def remove_swear(self, interaction: discord.Interaction, arg: str):
        collection = mongodb['swears']
        found = False
        for swear in collection.find():
            if swear['swear'] == arg:
                found = True
                break
        if not found:
            await interaction.response.send_message(f"The swear `{arg}` was not found.", ephemeral=True)
            return
        collection.delete_one({"swear": arg})
        await interaction.response.send_message(f"Swear `{arg}` successfully removed.")
        await interaction.channel.send("reload swears")

    @discord.app_commands.command(description="Get a list of the current swears")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    async def swearlist(self, interaction: discord.Interaction):
        collection = mongodb['swears']
        description = ""
        for swear in collection.find():
            description += f"\n{swear['swear']}"
        embed = discord.Embed(title="Swearlist", description=description, color=0x00a0a0)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(description="Ban a user to delete all their messages, then unban them")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    async def softban(self, interaction: discord.Interaction, user: discord.User):
        await interaction.guild.ban(discord.Object(id=user.id), delete_message_days=7, reason="softban")
        await interaction.response.send_message(user + "softbanned successfully.")
        await interaction.guild.unban(discord.Object(id=user.id), reason="softban")

    @commands.hybrid_command(description="See what git commit the bot is currently running on")
    @discord.app_commands.guild_only()
    @discord.app_commands.default_permissions()
    async def commit(self, ctx):
        commit = subprocess.run(['git', 'show', '-s', '--oneline'], stdout=subprocess.PIPE).stdout.decode('utf-8')[:7]
        await ctx.send(f"I am currently running on commit {commit}.\nhttps://github.com/TechSupportCentral/TSCBot-py/commit/{commit}")

async def setup(bot):
    await bot.add_cog(administration(bot))
