from discord.ext import commands
import discord
import yaml
import datetime, time

class infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global starttime
        starttime = time.time()

    @commands.command()
    async def uptime(self, ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-starttime))))
        await ctx.send(f'The bot has been online for {uptime}.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name='commands')
    async def _commands(self, ctx, arg=None):
        with open('commands.yaml', 'r') as commands_file:
            commands = yaml.load(commands_file, Loader=yaml.BaseLoader)
        with open('config.yaml', 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.BaseLoader)
        role_ids = config['role_ids']

        if not arg:
            embed = discord.Embed(title="Command List", description="Commands come in categories. Here is a list of categories, run `!commands <category>` to see the commands in a certain category.", color=0x00a0a0)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            for category in commands:
                if not '_desc' in category:
                    embed.add_field(name=category + ':', value=commands[category + '_desc'], inline=True)
            await ctx.send(embed=embed)
        elif arg in commands:
            guild = ctx.message.guild
            mod_role = guild.get_role(int(role_ids['moderator']))
            owner_role = guild.get_role(int(role_ids['owner']))
            if arg == "moderation" and not mod_role in ctx.author.roles:
                await ctx.send("The `moderation` category can only be viewed by moderators.")
                return
            elif arg == "administration" and not owner_role in ctx.author.roles:
                await ctx.send("The `administration` category can only be viewed by admins.")
                return
            embed = discord.Embed(title="Command List", description=f"Commands in the {arg} category:", color=0x00a0a0)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            for command in commands[arg]:
                embed.add_field(name=command + ':', value=commands[arg].get(command), inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Please send a valid category')

    @commands.command(name='spteam-requirements')
    async def spteam(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Support Team Requirements", color=discord.Color.green())
        embed.add_field(name="Corruption:", value="If a member of the staff team does something they shouldn't have, let the owners know.", inline=False)
        embed.add_field(name="Activity:", value="Support Team members need to be active at least once a week.", inline=False)
        embed.add_field(name="Experience:", value="You need to have been on the server for at least a week and have a discord account older than a month.", inline=False)
        embed.add_field(name="Piracy:", value="If someone asks for support with pirated or cracked content, report them to the mod team and don't give them support.", inline=False)
        embed.add_field(name="Misinformation:", value="If you're not completely sure about something, ask other members of the support team to fact check it or let them take over the support instead of misinforming the user.", inline=False)
        embed.add_field(name="Confidence:", value="Be confident in the support you're applying. It's okay if you don't know much but be confident in what you do know.", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='mod-requirements')
    async def modteam(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Moderator Requirements", color=discord.Color.gold())
        embed.add_field(name="Corruption:", value="If a member of the staff team does something they shouldn't have, let the owners know.", inline=False)
        embed.add_field(name="Rules:", value="You need to read the rules and know when to warn, mute, kick, and ban.", inline=False)
        embed.add_field(name="Activity:", value="Moderators need to be active 6-7 times a week.", inline=False)
        embed.add_field(name="Experience:", value="You need to have been on the server for at least a month and have a discord account older than 6 months.", inline=False)
        embed.add_field(name="De-escalation:", value="You must be able to defuse heated situations efficiently and effectively.", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def rules(self, ctx):
        with open('config.yaml', 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.BaseLoader)
        channel_ids = config['channel_ids']
        role_ids = config['role_ids']

        await ctx.message.delete()
        embed = discord.Embed(title="Server Rules", color=discord.Color.green())
        embed.add_field(name="Rule 1:", value="Be respectful to our Support Team, they provide support voluntarily for free during their own time.", inline=False)
        embed.add_field(name="Rule 2:", value="Profanity is not allowed on this server. If you send a message with profanity it will be deleted.", inline=False)
        embed.add_field(name="Rule 3:", value="We do not tolerate any form of racism, sexism, discrimination, etc. This behavior will result in an immediate ban.", inline=False)
        embed.add_field(name="Rule 4:", value=f"For faster and easier help, post your issue in a support channel and ping the <@&{role_ids['support_team']}>. If you post your question in <#{channel_ids['general']}> and/or don't ping the Support Team, they will not notice it and it'll take longer to get support.", inline=False)
        embed.add_field(name="Rule 5:", value="All users must follow Discord TOS. https://discord.com/terms", inline=False)
        embed.add_field(name="Rule 6:", value="No self promotion or advertising of any kind is allowed, especially in DMs.", inline=False)
        embed.add_field(name="Rule 7:", value="Do not leak or request any personal information. (i.e. IP Addresses, Full Names, Locations, etc.)", inline=False)
        embed.add_field(name="Rule 8:", value="If a Support Team member is helping someone, don't try to help at the same time. If you want to help more than please apply for Support Team via our staff application forms.", inline=False)
        embed.add_field(name="Rule 9:", value=f"English is the language used for support and discussion. Make a ticket in <#{channel_ids['ticket_create']}> if you require help in another language.", inline=False)
        embed.add_field(name="Rule 10:", value="We do not provide support for pirated, cracked, or hacked content of any kind. It is illegal and against our rules.", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(infos(bot))
