from discord.ext import commands
import discord

class techinfo(commands.Cog):
    @commands.command()
    async def cpuz(self, ctx):
        await ctx.send("https://www.cpuid.com/downloads/cpu-z/cpu-z_1.95-en.exe")

    @commands.command(aliases=["nvidiadrivers", "amddrivers", "realtekdrivers", "IntelDSA"])
    async def olddrivers(self, ctx):
        await ctx.send("If you're looking for driver links, run the `!drivers` command.")

    @commands.command()
    async def drivers(self, ctx):
        embed = discord.Embed(title="Drivers", description="Links to downloads for various drivers", color=0x00a0a0)
        embed.add_field(name="AMD Drivers:", value="https://amd.com/en/support", inline=False)
        embed.add_field(name="nVidia Drivers:", value="https://nvidia.com/Download/index.aspx", inline=False)
        embed.add_field(name="Intel Driver & Support Assistant:", value="https://dsadata.intel.com/installer", inline=False)
        embed.add_field(name="Realtek Audio Drivers:", value="https://www.realtek.com/en/downloads", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def hwmonitor(self, ctx):
        await ctx.send("https://www.cpuid.com/downloads/hwmonitor/hwmonitor_1.43.exe")

    @commands.command()
    async def key(self, ctx):
        await ctx.send("https://www.magicaljellybean.com/downloads/KeyFinderInstaller.exe")

    @commands.command()
    async def safemode(self, ctx):
        await ctx.send("https://support.microsoft.com/en-us/windows/start-your-pc-in-safe-mode-in-windows-10-92c27cff-db89-8644-1ce4-b3e5e56fe234")

    @commands.command(aliases=["mwb"])
    async def malwarebytes(self, ctx):
        await ctx.send("https://malwarebytes.com/mwb-download")

    @commands.command()
    async def windowsinstall(self, ctx):
        await ctx.send("This tutorial will lead you how to do a fresh windows installation: (All your data will be gone, back it up and use `!key` in case you need to back up your Product Key too, please save it somewhere safe and don't show us or anyone the key!)\nhttps://youtu.be/bwJ_E-I9WRs\nTo figure out which key you need to use to boot to a usb, run the command `!bootkeys`.")

    @commands.command()
    async def bootkeys(self, ctx):
        embed = discord.Embed(title="", description="", color=0x00a0a0)
        embed.add_field(name="Dell, Toshiba, Huawei, Lenovo:", value="F12", inline=True)
        embed.add_field(name="Acer:", value="F12, F9, F2, Esc", inline=True)
        embed.add_field(name="Apple:", value="Option / Alt", inline=True)
        embed.add_field(name="Asus:", value="Esc", inline=True)
        embed.add_field(name="HP:", value="F9", inline=True)
        embed.add_field(name="Intel:", value="F10", inline=True)
        embed.add_field(name="MSI:", value="F11", inline=True)
        embed.add_field(name="Samsung:", value="Esc, F12, F2", inline=True)
        embed.add_field(name="Sony:", value="Esc, F10, F11", inline=True)
        embed.add_field(name="Other Common Ones:", value="F2, F10, F12, Esc, Del", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def linuxusb(self, ctx):
        embed = discord.Embed(title="How to get a Linux Live USB", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Decide what distro is best for you.\nIf you're not experienced with computers, go with Linux Mint.\nIf you're experienced with computers but not with Linux, go for Fedora.\nIf you're experienced with Linux, what are you doing here?", inline=False)
        embed.add_field(name="Step 2:", value="Download the Linux ISO and the flashing tool.\nDepending on what distro you chose pick one of these links:\nLinux Mint: https://linuxmint.com/download.php\nFedora: https://getfedora.org/en/workstation/download/ (Instead of Fedora Media Writer, make sure to download the x86_64 ISO)\nFor the flashing tool you can use balenaEtcher or Rufus.\nbalenaEtcher is simple and gets the job done fast: https://balena.io/etcher/\nRufus has many more features but can be confusing to novices: https://rufus.ie", inline=False)
        embed.add_field(name="Step 3:", value="Once everything is downloaded, use the flashing tool to flash your ISO to a USB (the usb must be 8 GB or larger).\nSelect the Linux ISO you downloaded and the USB you want to flash to, then start the flashing process.\nWhen the flashing is done, unplug the usb and plug it into the device you want to boot into Linux (if it's the same device just leave it plugged in and shut down the PC).", inline=False)
        embed.add_field(name="Step 4:", value="Boot into Linux.\nTurn on the computer and start spamming the boot menu key (figure out which one yours is with the `!bootkey` command) until the menu pops up.\nWhen the menu pops up, select the USB to boot to.", inline=False)
        embed.add_field(name="Step 5:", value="Install or try out linux.\nYour computer will boot to show the Linux desktop. Note that Linux is not installed on the computer, it's what is called a Live USB where you can test it out before you try it. Anything you do on the USB in this state will not be saved and doesn't affect your PC. If you wish to replace Windows with Linux, open the 'Install Linux' file on the desktop. If you want to return to Windows on the next reboot, simply restart the PC with the USB unplugged.", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def vcredist(self, ctx):
        embed = discord.Embed(title="Visual C++ Redistributable", url="https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist", description="If you are missing any of the following DLLs, download the corresponding file(s) and install them.", color=0x00a0a0)
        embed.add_field(name="MSVCP140.dll or MSVCR140.dll", value="[x86](https://aka.ms/vs/17/release/vc_redist.x86.exe), [x64](https://aka.ms/vs/17/release/vc_redist.x64.exe), or [ARM64](https://aka.ms/vs/17/release/vc_redist.arm64.exe) (Only install the one that pertains to your system)", inline=False)
        embed.add_field(name="MSVCP120.dll or MSVCR120.dll", value="[x86](https://aka.ms/highdpimfc2013x86enu) and [x64](https://aka.ms/highdpimfc2013x64enu) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP110.dll or MSVCR110.dll", value="[x86](https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x86.exe) and [x64](https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x64.exe) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP100.dll or MSVCR100.dll", value="[x86](https://download.microsoft.com/download/C/6/D/C6D0FD4E-9E53-4897-9B91-836EBA2AACD3/vcredist_x86.exe) and [x64](https://download.microsoft.com/download/A/8/0/A80747C3-41BD-45DF-B505-E9710D2744E0/vcredist_x64.exe) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP90.dll or MSVCR90.dll", value="[x86](https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x86.exe) and [x64](https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x64.exe) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP80.dll or MSVCR80.dll", value="[Select the ones you need](https://www.microsoft.com/download/details.aspx?id=26347) (Install both x86 and x64 unless using a 32 bit system)", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(techinfo(bot))
