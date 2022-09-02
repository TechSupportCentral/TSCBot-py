from discord.ext import commands
import discord

class techinfo(commands.Cog):
    @commands.hybrid_command(description="Get links to download various drivers")
    async def drivers(self, ctx):
        embed = discord.Embed(title="Drivers", description="Links to downloads for various drivers", color=0x00a0a0)
        embed.add_field(name="AMD Drivers:", value="https://amd.com/en/support", inline=False)
        embed.add_field(name="nVidia Drivers:", value="https://nvidia.com/Download/index.aspx", inline=False)
        embed.add_field(name="Intel Driver & Support Assistant:", value="https://dsadata.intel.com/installer", inline=False)
        embed.add_field(name="Realtek Audio Drivers:", value="https://www.realtek.com/en/downloads", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="driver-managers", aliases=["driverbooster", "drivereasy", "microsoft-drivers"], description="Explain why third party driver managers should not be used")
    async def driver_managers(self, ctx):
        embed = discord.Embed(title="Third Party Driver Managers", description="Do not use third party driver managers like Driver Booster or Driver Easy. They are usually either spyware or adware and install broken or outdated drivers which can cause many problems.", color=0x00a0a0)
        embed.add_field(name="What should I do instead?", value="If you have a prebuilt computer, go to the manufacturer's website and download the drivers for your model. [Here](https://support.hp.com/us-en/drivers/selfservice/hp-envy-m6-aq100-x360-convertible-pc/12499188/model/13475171) is an example of an OEM driver page.\nIf you built your own computer, go to the motherboard manufacturer's page and download the drivers for your motherboard, then any other drivers from the pages of the manufacturers of the parts. For example, if you have an Asus TUF GAMING X570-PLUS WiFi with an RTX 3090, you would download your BIOS, chipset, audio, and WiFi drivers [here](https://www.asus.com/supportonly/TUF%20GAMING%20X570-PLUS%20(WI-FI)/HelpDesk_Download/) and your graphics drivers [here](https://nvidia.com/Download/driverResults.aspx/190552/).", inline=False)
        embed.add_field(name="Graphics Drivers", value="Even if your computer is a prebuilt, you should still get your graphics drivers directly from the manufacturer of the GPU ([AMD](https://amd.com/en/support), [NVIDIA](https://nvidia.com/Download/index.aspx), [Intel](https://dsadata.intel.com/installer), etc).", inline=False)
        embed.add_field(name="What about Windows Update?", value="Microsoft usually doesn't supply the best drivers for your hardware. In many cases they're out of date, and for graphics drivers, they're commonly less functional and will have decreased performance and support.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=["bootkey"], description="Get a list of keys used to get into the BIOS Boot Menu")
    async def bootkeys(self, ctx):
        embed = discord.Embed(title="How to get into the boot menus of various computers:", description="Find your brand below and spam the relevant key when you start the computer up.", color=0x00a0a0)
        embed.add_field(name="Dell, Toshiba, Huawei, Lenovo, and many others:", value="F12", inline=True)
        embed.add_field(name="Acer:", value="F12, F9, F2, or Esc", inline=True)
        embed.add_field(name="Apple:", value="Option (Alt)", inline=True)
        embed.add_field(name="Asus:", value="Esc", inline=True)
        embed.add_field(name="HP:", value="F9", inline=True)
        embed.add_field(name="Intel:", value="F10", inline=True)
        embed.add_field(name="MSI:", value="F11", inline=True)
        embed.add_field(name="Samsung:", value="Esc, F12, or F2", inline=True)
        embed.add_field(name="Sony:", value="Esc, F10, or F11", inline=True)
        embed.add_field(name="Other common keys:", value="F2, F10, F12, Esc, or Del", inline=True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to install or reinstall Windows 10")
    async def windowsusb(self, ctx):
        embed = discord.Embed(title="How to install or reinstall Windows 10", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Insert a USB flash drive with at least 8 GB of capacity into a Windows computer with access to the internet.", inline=False)
        embed.add_field(name="Step 2:", value="Download [Rufus](https://rufus.ie), the tool you will use to download and flash Windows to the USB.", inline=False)
        embed.add_field(name="Step 3:", value="Open Rufus. Next to the Select button, there should be an arrow. Click the arrow, then click download.\nPress the download button. Select Windows 10 in your preferred language and edition, for the x64 architecture.\nOnce you choose where Rufus should save the ISO, it will begin downloading.", inline=False)
        embed.add_field(name="Step 4:", value="When Rufus is done downloading the ISO, select your USB flash drive in the device menu. When you flash Windows to the drive, its previous contents will be erased, so now would be a good time to back them up if needed.\nIf the computer you want to install Windows on is UEFI (most computers made after 2010), select GPT as the partition scheme. If it has a legacy BIOS instead, select MBR.\nRufus should now look like [this](https://i.imgur.com/pgKRiJM.png) or [this](https://i.imgur.com/gu92Uel.png). If so, click Start then OK to begin the flashing process.", inline=False)
        embed.add_field(name="Step 5:", value="After the flashing process is complete, turn off the computer you want to install Windows on, and insert the USB if it isn't already.\nTurn it back on and start spamming the boot menu key (figure out which one yours is with the `!bootkeys` command) until the menu appears.\nWhen the menu shows up, select the USB to boot to.", inline=False)
        embed.add_field(name="Step 6:", value="Go through the Windows setup process.\nIf setup asks you for a product key, select 'I don't have a product key.' Windows should automatically activate itself later.\nWhen asked what type of installation you want, select custom. Find out what drive you want to install Windows on (for example Drive 0), and delete all of its partitions so that only unallocated space remains. Select the unallocated space and click next.", inline=False)
        embed.add_field(name="Step 7:", value="The system will reboot at some point. In some cases, it will go back to the first setup screen. If this happens, turn off the computer, remove the USB, and turn it back on.", inline=False)
        embed.add_field(name="Step 8:", value="When you get to the next stage of setup, make sure to use a local account and avoid all prompts encouraging you to switch to a Microsoft one.\nFor your privacy, disable every option on the Privacy Options screen. Do not set up Cortana.", inline=False)
        embed.add_field(name="Step 9:", value="If everything went well, you should have a brand new Windows 10 installation! The first thing to do is to install all the drivers for your device.\n**Note:** Never use any third party driver management software, like Driver Booster. Only ever install drivers directly from your hardware manufacturer.", inline=False)
        embed.add_field(name="Step 10:", value="Format your USB so you can use it again.\nOpen File Explorer and find your USB flash drive. Right click it and select format. Use NTFS as the filesystem and tick the Quick Format box.\nOnce the format is complete, your drive will be empty and you can use it for your own purposes again.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to create a bootable Linux USB")
    async def linuxusb(self, ctx):
        embed = discord.Embed(title="How to get a Linux Live USB", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Decide what distro is best for you.\nIf you're not experienced with computers, use [Linux Mint](https://linuxmint.com/download.php).\nIf you're experienced with computers but not with Linux, use [Fedora](https://getfedora.org/en/workstation/download/).", inline=False)
        embed.add_field(name="Step 2:", value="Download the Linux ISO and the flashing tool.\nDownload the Linux ISO from one of the links above. If you chose Fedora, make sure to download the x86_64 ISO instead of Fedora Media Writer.\nFor the flashing tool, you can use [balenaEtcher](https://balena.io/etcher/) or [Rufus](https://rufus.ie).\nbalenaEtcher is simple and gets the job done fast; Rufus has many more features, but it can be confusing to beginners.", inline=False)
        embed.add_field(name="Step 3:", value="Once everything is downloaded, use the flashing tool to flash your ISO to a USB (must be 4 GB or larger).\nSelect the Linux ISO you downloaded and the USB you want to flash to, then start the flashing process.\nWhen the flashing is done, unplug the USB and plug it into the device you want to boot into Linux (if it's the same device, just leave it plugged in and shut down the PC).", inline=False)
        embed.add_field(name="Step 4:", value="Boot into Linux.\nTurn on the computer and start spamming the boot menu key (figure out which one yours is with the `!bootkeys` command) until the menu appears.\nWhen the menu shows up, select the USB to boot to.", inline=False)
        embed.add_field(name="Step 5:", value="Install or try out linux.\nYour computer will boot to show the Linux desktop. Note that Linux is not installed on the computer; it's what is called a Live USB, where you can test it out before installation. Anything you do on the USB in this state will not be saved and doesn't affect your PC. If you wish to replace Windows with Linux, open the 'Install Linux' file on the desktop. If you want to return to Windows on the next reboot, simply restart the PC with the USB unplugged.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to flash a Linux ISO to USB on Android")
    async def androidusb(self, ctx):
        embed = discord.Embed(title="How to flash a Linux ISO to USB on Android", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Make sure you can actually plug your USB into the phone.\nIn a perfect world, you'll have a USB-C flash drive and a USB-C phone, so you can just plug it in. Unfortunately, most of the time it's USB type A and the phone is either Micro B or USB-C.\nIf this is the case, buy an adapter like one of these:\n[USB Micro B (most older phones)](https://amazon.com/dp/B00LN3LQKQ)\n[USB-C (most newer phones)](https://amazon.com/dp/B01GGKYXVE)", inline=False)
        embed.add_field(name="Step 2:", value="Download EtchDroid from [Google Play](https://play.google.com/store/apps/details?id=eu.depau.etchdroid) or manually install the APK from [here](https://github.com/EtchDroid/EtchDroid/releases/download/v1.5/EtchDroid-v1.5-release.apk).", inline=False)
        embed.add_field(name="Step 3:", value="Follow the instructions from EtchDroid's official YouTube tutorial: https://youtu.be/6gM5SoNO0Fc", inline=False)
        embed.set_footer(text="Note: EtchDroid will not work for Windows ISOs as they don't follow the ISOHybrid standard.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=['windows7', 'windows8'], description="Explain why Windows 7 and 8 should not be used")
    async def legacywindows(self, ctx):
        embed = discord.Embed(title="Legacy versions of Windows", description="Windows 7 and 8 are no longer officially supported by Microsoft.\nUsing older versions of windows puts you at risk to malware and other vulnerabilities (even if you're careful), which can easily be avoided by upgrading your operating system.", color=0x00a0a0)
        embed.add_field(name="What can I do?", value="If your computer is good enough to run Windows 10 reliably, download the [Media Creation Tool](https://microsoft.com/en-us/software-download/windows10) and select 'Upgrade this PC now' to upgrade to Windows 10. It's not recommend to upgrade to Windows 11 at this time.\nIf your computer isn't good enough to run Windows 10 very well, it's recommended to switch to a lighter Linux distribution such as Linux Mint. Instructions are available with the `!linuxusb` command.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get links to various versions of the Microsoft Visual C++ Redistributable")
    async def vcredist(self, ctx):
        embed = discord.Embed(title="Visual C++ Redistributable", url="https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist", description="If you are missing any of the following DLLs, download the corresponding file(s) and install them.", color=0x00a0a0)
        embed.add_field(name="MSVCP140.dll or MSVCR140.dll", value="[x86](https://aka.ms/vs/17/release/vc_redist.x86.exe), [x64](https://aka.ms/vs/17/release/vc_redist.x64.exe), or [ARM64](https://aka.ms/vs/17/release/vc_redist.arm64.exe) (Only install the one that pertains to your system)", inline=False)
        embed.add_field(name="MSVCP120.dll or MSVCR120.dll", value="[x86](https://aka.ms/highdpimfc2013x86enu) and [x64](https://aka.ms/highdpimfc2013x64enu) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP110.dll or MSVCR110.dll", value="[x86](https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x86.exe) and [x64](https://download.microsoft.com/download/1/6/B/16B06F60-3B20-4FF2-B699-5E9B7962F9AE/VSU_4/vcredist_x64.exe) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP100.dll or MSVCR100.dll", value="[x86](https://download.microsoft.com/download/C/6/D/C6D0FD4E-9E53-4897-9B91-836EBA2AACD3/vcredist_x86.exe) and [x64](https://download.microsoft.com/download/A/8/0/A80747C3-41BD-45DF-B505-E9710D2744E0/vcredist_x64.exe) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP90.dll or MSVCR90.dll", value="[x86](https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x86.exe) and [x64](https://download.microsoft.com/download/5/D/8/5D8C65CB-C849-4025-8E95-C3966CAFD8AE/vcredist_x64.exe) (Install both unless using a 32 bit system)", inline=False)
        embed.add_field(name="MSVCP80.dll or MSVCR80.dll", value="[Select the ones you need](https://www.microsoft.com/download/details.aspx?id=26347) (Install both x86 and x64 unless using a 32 bit system)", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Show the proper location to plug in a monitor")
    async def monitor(self, ctx):
        await ctx.send(file=discord.File('images/monitor.jpg', 'monitor.jpg'))

    @commands.hybrid_command(description="Show the difference between SATA and NVMe M.2 SSDs using differently keyed M.2 connectors")
    async def m2(self, ctx):
        files = [discord.File('images/m.2-key-type.jpg', 'key-type.jpg'), discord.File('images/m.2-drive-type.jpg', 'drive-type.png')]
        await ctx.send(files=files)

async def setup(bot):
    await bot.add_cog(techinfo(bot))
