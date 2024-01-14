from discord.ext import commands
import discord
import yaml
from time import time

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('config.yaml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    global role_ids
    role_ids = config['role_ids']
    global channel_ids
    channel_ids = config['channel_ids']
    global message_ids
    message_ids = config['message_ids']

    @commands.Cog.listener()
    async def on_ready(self):
        global starttime
        starttime = time()

    @commands.hybrid_command(description="See how long the bot has been online")
    async def uptime(self, ctx):
        intervals = (
            ('days', 86400),
            ('hours', 3600),
            ('minutes', 60),
            ('seconds', 1),
        )

        seconds = round(time() - starttime)
        result = []
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
            uptime = ' '.join(result[:3])
        else:
            uptime = ', '.join(result[:3])

        await ctx.send(f"I have been online for {uptime}.")

    @commands.hybrid_command(description="Test the bot latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.hybrid_command(name='support-team-requirements', description="See the requirements to join the support team")
    async def spteam(self, ctx):
        embed = discord.Embed(title="Support Team Requirements", color=discord.Color.green())
        embed.add_field(name="Corruption:", value="If a member of the staff team does something they shouldn't have, let the owners know.", inline=False)
        embed.add_field(name="Activity:", value="Support Team members need to be active at least once a week.", inline=False)
        embed.add_field(name="Experience:", value="You need to have been on the server for at least a week and have a discord account older than a month.", inline=False)
        embed.add_field(name="Piracy:", value="If someone asks for support with pirated or cracked content, report them to the mod team and don't give them support.", inline=False)
        embed.add_field(name="Misinformation:", value="If you're not completely sure about something, ask other members of the support team to fact check it or let them take over the support instead of misinforming the user.", inline=False)
        embed.add_field(name="Confidence:", value="Be confident in the support you're applying. It's okay if you don't know much but be confident in what you do know.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='mod-requirements', description="See the requirements to join the mod team")
    async def modteam(self, ctx):
        embed = discord.Embed(title="Moderator Requirements", color=discord.Color.gold())
        embed.add_field(name="Corruption:", value="If a member of the staff team does something they shouldn't have, let the owners know.", inline=False)
        embed.add_field(name="Rules:", value="You need to read the rules and know when to warn, mute, kick, and ban.", inline=False)
        embed.add_field(name="Activity:", value="Moderators need to be active 6-7 times a week.", inline=False)
        embed.add_field(name="Experience:", value="You need to have been on the server for at least a month and have a discord account older than 6 months.", inline=False)
        embed.add_field(name="De-escalation:", value="You must be able to defuse heated situations efficiently and effectively.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get a list of server rules")
    async def rules(self, ctx):
        embed = discord.Embed(title="Server Rules", color=discord.Color.green())
        embed.add_field(name="Rule 1:", value="Be respectful to our Support Team; they provide support voluntarily for free during their own time.", inline=False)
        embed.add_field(name="Rule 2:", value="Profanity is not allowed on this server. If you send a message containing profanity, it will be deleted.", inline=False)
        embed.add_field(name="Rule 3:", value="We do not tolerate any form of racism, bigotry, or discrimination. This behavior will result in an immediate ban.", inline=False)
        embed.add_field(name="Rule 4:", value=f"For faster and easier help, post your issue in a support channel and ping the <@&{role_ids['support_team']}>. If you post your question in <#{channel_ids['general']}> and/or don't ping the Support Team, they will not notice it and it'll take longer to get support.", inline=False)
        embed.add_field(name="Rule 5:", value="All users must follow Discord TOS. https://discord.com/terms", inline=False)
        embed.add_field(name="Rule 6:", value="No self promotion or advertising of any kind is allowed, especially in DMs.", inline=False)
        embed.add_field(name="Rule 7:", value="Do not leak or request any personal information (IP Addresses, full names, locations, etc).", inline=False)
        embed.add_field(name="Rule 8:", value="If a Support Team member is helping someone, don't try to help at the same time. If you want to help more, please apply for Support Team via our staff application forms.", inline=False)
        embed.add_field(name="Rule 9:", value=f"English is the language used for support and discussion. Make a ticket in <#{channel_ids['ticket_create']}> if you require help in another language.", inline=False)
        embed.add_field(name="Rule 10:", value="We will not help you do something that is against the law. For example, we do not provide support for pirated, cracked, or hacked content, ban evasion on any platform (however unfair the ban), or bypassing a phone's iCloud/Google account lock (which probably isn't possible anyway).", inline=False)
        embed.add_field(name="Rule 11:", value="Do not beg for roles. When you apply for Support Team or Moderator, we carefully consider your application based on many factors. Our decision is final, and continuing to beg for the role(s) will do the opposite of what you want, lessening the chance you'll get them in the future.", inline=False)
        embed.add_field(name="Rule 12:", value=f"Do not post the same message in multiple channels. Find the best support channel for your question and post it to only that channel. When in doubt, use <#{channel_ids['general_support']}>.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Look at a specific server rule")
    async def rule(self, ctx, rule: int):
        channel = self.bot.get_channel(int(channel_ids['rules']))
        message = await channel.fetch_message(int(message_ids['rules']))

        if rule > len(message.embeds[0].fields):
            await ctx.send("This rule does not exist.")
            return

        embed = discord.Embed(title=f"Rule {rule}", description=message.embeds[0].fields[rule - 1].value, color=0x00a0a0)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(info(bot))
