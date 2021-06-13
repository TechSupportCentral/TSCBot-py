from discord.ext import commands

class infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def amddrivers(ctx: commands.Context):
        await ctx.send(f"https://www.amd.com/en/support")

    @commands.command()
    async def cpuz(ctx: commands.Context):
        await ctx.send(f"https://www.cpuid.com/downloads/cpu-z/cpu-z_1.95-en.exe")

    @commands.command()
    async def hwmonitor(ctx: commands.Context):
        await ctx.send(f"https://www.cpuid.com/downloads/hwmonitor/hwmonitor_1.43.exe")

    @commands.command()
    async def key(ctx: commands.Context):
        await ctx.send(f"https://www.magicaljellybean.com/downloads/KeyFinderInstaller.exe")

    @commands.command()
    async def key(ctx: commands.Context):
        await ctx.send(f"https://www.nvidia.com/Download/index.aspx")

    @commands.command()
    async def safemode(ctx: commands.Context):
        await ctx.send(f"https://support.microsoft.com/en-us/windows/start-your-pc-in-safe-mode-in-windows-10-92c27cff-db89-8644-1ce4-b3e5e56fe234")

    @commands.command()
    async def security(ctx: commands.Context):
        await ctx.send(f"https://www.malwarebytes.com/mwb-download/thankyou/")

    @commands.command()
    async def windows-setup(ctx: commands.Context):
        await ctx.send(f"This tutorial will lead you how to do a fresh windows installation:  (All your data will be gone,  back it up and use `!key` in case you need to back up your Product Key too, please save it somewhere safe and don't show us or anyone the key!)\nhttps://youtu.be/bwJ_E-I9WRs\nTo figure out which key you need to use to boot to a usb, run the command `!bootkeys`.")

def setup(bot):
    bot.add_cog(core(bot))
