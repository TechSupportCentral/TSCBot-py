from discord.ext import commands
import discord
import yaml
from asyncio import sleep
from time import time
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

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global channel_ids
    channel_ids = config['channel_ids']
    global role_ids
    role_ids = config['role_ids']

    @commands.Cog.listener()
    async def on_ready(self):
        async def remind(self, collection, reminder):
            text = reminder['text']
            total = reminder['time']
            id = int(reminder['user'])
            start = int(reminder['start'])
            end = start + int(reminder['seconds'])
            now = time()

            if self.bot.guilds[0].get_member(id) is None:
                collection.delete_one({"_id": reminder['_id']})
                return
            user = self.bot.guilds[0].get_member(id)

            if end > now:
                print(f"Resuming reminder of {total} from {user}")
                await sleep(end - now)
                embed = discord.Embed(title=f"Reminder from <t:{start}:F> ({total} ago):", description=text, color=0x00a0a0)
            else:
                print(f"Sending belated reminder of {total} from {user}")
                embed = discord.Embed(title="Belated reminder", description=f"Sorry, it looks like the bot was offline when you were supposed to get your reminder from <t:{start}:F> (should've lasted {total}).\n\nHere was the reminder:\n{text}", color=0x00a0a0)
            collection.delete_one({"_id": reminder['_id']})

            if user.dm_channel is None:
                dm = await user.create_dm()
            else:
                dm = user.dm_channel
            await dm.send(embed=embed)

        collection = mongodb['reminders']
        for reminder in collection.find():
            await remind(self, collection, reminder)

    @discord.app_commands.command(description="Alert the moderators")
    @discord.app_commands.guild_only()
    @discord.app_commands.describe(description="What you're alerting the moderators about")
    async def alert(self, interaction: discord.Interaction, description: str = "A description was not provided."):
        embed = discord.Embed(title="Moderator Alert", description=interaction.channel.mention + "\n\n" + description, color=discord.Color.red())
        embed.add_field(name="Alert Author", value=interaction.user, inline=True)
        embed.add_field(name="User ID", value=interaction.user.id, inline=True)
        channel = self.bot.get_channel(int(channel_ids['modlog']))
        await channel.send(f"<@&{role_ids['moderator']}> <@&{role_ids['trial_mod']}>", embed=embed)
        await interaction.response.send_message("The moderators have been alerted.", ephemeral=True)

    @discord.app_commands.command(description="Make a suggestion on how to improve the server")
    @discord.app_commands.guild_only()
    async def suggest(self, interaction: discord.Interaction, suggestion: str):
        embed = discord.Embed(description=f"**Suggestion:** {suggestion}", color=discord.Color.lighter_grey())
        embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        embed.add_field(name="Status", value="Pending")
        channel = self.bot.get_channel(int(channel_ids['suggestions_list']))
        await channel.send(embed=embed)
        await interaction.response.send_message("Thanks for your suggestion! You will be notified when the owners respond.")

    @discord.app_commands.command(description="Remind yourself of something")
    @discord.app_commands.rename(total="time")
    @discord.app_commands.describe(
        total="The amount of time you'd like to be reminded in.\nSyntax is `1d2h3m4s` (example of 1 day, 2 hours, 3 minutes, and 4 seconds).",
        reminder="What you're reminding yourself of"
    )
    async def remindme(self, interaction: discord.Interaction, total: str, reminder: str = "No description provided."):
        gran = 0
        for char in total:
            gran += char.isalpha()
        if gran > 4:
            await interaction.response.send_message("The time you requested to be reminded in is not in the correct format.\nIt should look something like `1d2h3m4s` (1 day, 2 hours, 3 minutes, and 4 seconds).", ephemeral=True)
            return
        cooltime = [int(a[ :-1]) if a else b for a,b in zip(re.search('(\d+d)?(\d+h)?(\d+m)?(\d+s)?', total).groups(), [0, 0, 0, 0])]
        seconds = cooltime[0]*86400 + cooltime[1]*3600 + cooltime[2]*60 + cooltime[3]
        fancytime = await seconds_to_fancytime(seconds, gran)

        collection = mongodb['reminders']
        collection.insert_one({"text": reminder, "time": fancytime, "user": str(interaction.user.id), "start": str(round(time())), "seconds": str(seconds)})
        await interaction.response.send_message(f"I will remind you in {fancytime} (<t:{round(time() + seconds)}:F>).", ephemeral=True)
        await sleep(seconds)
        collection.delete_one({"text": reminder, "time": fancytime, "user": str(interaction.user.id)})

        embed = discord.Embed(title=f"Reminder from <t:{round(time() - seconds)}:F> ({fancytime} ago):", description=reminder, color=0x00a0a0)
        if interaction.user.dm_channel is None:
            dm = await interaction.user.create_dm()
        else:
            dm = interaction.user.dm_channel
        await dm.send(embed=embed)

    @discord.app_commands.command(name="create-ticket", description="Open a ticket")
    async def create_ticket(self, interaction: discord.Interaction, title: str):
        channel = self.bot.get_channel(int(channel_ids['ticket_create']))
        mod_role = self.bot.guilds[0].get_role(int(role_ids['moderator']))

        thread = await channel.create_thread(name=title, invitable=False)
        await thread.add_user(interaction.user)
        for mod in mod_role.members:
            await thread.add_user(mod)

        await thread.send(f"{interaction.user.mention}, your ticket has been created. Please explain your rationale and wait for a {mod_role.mention} to respond.")
        await interaction.response.send_message(f"Your ticket {thread.mention} was created successfully.", ephemeral=True)

    @commands.hybrid_command(description="Shorten a link")
    async def shorten(self, ctx, link: str):
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

async def setup(bot):
    await bot.add_cog(misc(bot))
