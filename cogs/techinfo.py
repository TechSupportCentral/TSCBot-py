from discord.ext import commands
import discord

class techinfo(commands.Cog):
    @commands.hybrid_command(description="Get links to download various drivers")
    async def drivers(self, ctx):
        embed = discord.Embed(title="Drivers", description="Download links for various drivers", color=0x00a0a0)
        embed.add_field(name="Intel Driver & Support Assistant:", value="https://www.intel.com/content/www/us/en/support/detect.html", inline=False)
        embed.add_field(name="AMD Drivers:", value="https://amd.com/en/support", inline=False)
        embed.add_field(name="NVIDIA Drivers:", value="https://nvidia.com/Download/index.aspx", inline=False)
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
        embed.add_field(name="Other common keys:", value="F2, F10, F12, Esc, Del, or Enter", inline=True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to install or reinstall Windows 11")
    async def windowsusb(self, ctx):
        embed = discord.Embed(title="How to install or reinstall Windows 11", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Insert a USB flash drive with at least 8 GB of capacity into a Windows computer with access to the internet.", inline=False)
        embed.add_field(name="Step 2:", value="Download [Rufus](https://github.com/pbatard/rufus/releases/latest), the tool you will use to download and flash Windows to the USB.", inline=False)
        embed.add_field(name="Step 3:", value="Open Rufus. Next to the Select button, there should be an arrow. If not, try enabling [checking for updates](https://github.com/pbatard/rufus/wiki/FAQ#help-i-dont-see-the-iso-download-button). Click the arrow, then click download.\nPress the download button. Select Windows 11 in your preferred edition, and choose English International.\nSpecify where Rufus should save the ISO, and it will begin downloading.", inline=False)
        embed.add_field(name="Step 4:", value="When Rufus is done downloading the ISO, select your USB flash drive in the device menu. When you flash Windows to the drive, its previous contents will be erased, so now would be a good time to back them up if needed.\nSelect GPT as the partition scheme. Rufus should now look like [this](https://i.imgur.com/pgKRiJM.png). If so, click Start then OK to begin the flashing process.\nWhen prompted, enable 'Remove requirement for 4GB+ RAM, Secure Boot and TPM 2.0', 'Remove requirement for an online Microsoft account' and 'Disable data collection (Skip privacy questions)'.", inline=False)
        embed.add_field(name="Step 5:", value="After the flashing process is complete, turn off the computer you want to install Windows on, and insert the USB if it isn't already.\nTurn it back on and start spamming the boot menu key (figure out which one yours is with the `!bootkeys` command) until the menu appears.\nWhen the menu shows up, select the USB to boot to.", inline=False)
        embed.add_field(name="Step 6:", value="Go through the Windows setup process.\nIf setup asks you for a product key, select 'I don't have a product key'. Windows should automatically activate itself later.\nWhen asked what type of installation you want, select custom. Find out what drive you want to install Windows on (for example Drive 0), and delete all of its partitions so that only unallocated space remains. Select the unallocated space and click next.", inline=False)
        embed.add_field(name="Step 7:", value="The system will reboot at some point. In some cases, it will go back to the first setup screen. If this happens, turn off the computer, remove the USB, and turn it back on.", inline=False)
        embed.add_field(name="Step 8:", value="When you get to the next stage of setup, make sure to use a local account and avoid all prompts encouraging you to switch to a Microsoft one.\nIf you find yourself unable to do so, press Shift + F10 to open the command prompt. Type in `OOBE\BYPASSNRO` and press enter.", inline=False)
        embed.add_field(name="Step 9:", value="If everything went well, you should have a brand new Windows 11 installation! The first thing to do is to install all the drivers for your device.\n**Note:** Never use any third party driver management software, like Driver Booster. Only ever install drivers directly from your hardware manufacturer. When in doubt, use the !drivers command.", inline=False)
        embed.add_field(name="Step 10:", value="Format your USB so you can use it again.\nOpen File Explorer and find your USB flash drive. Right click it and select format. Use NTFS as the filesystem and tick the Quick Format box.\nOnce the format is complete, your drive will be empty and you can use it for your own purposes again.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to create a bootable Windows USB on macOS 11+")
    async def macwinusb(self, ctx):
        embed = discord.Embed(title="How to create bootable Windows 10 install media on macOS 11+", description="**Note:** Since Apple removed Boot Camp Assistant from macOS 11 Big Sur and later, this process has become significantly more difficult. If you have access to a computer running Windows or Linux, use that machine to create the install media instead. If you have a Mac running OS X 10.15 Mojave or earlier, follow the instructions given by `/osxwinusb`.", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Plug in a USB flash drive with at least 8 GB of capacity, that you don't mind erasing.", inline=False)
        embed.add_field(name="Step 2:", value="Go to https://microsoft.com/en-us/software-download/windows10ISO and download a Windows 10 ISO.", inline=False)
        embed.add_field(name="Step 3:", value="Open Disk Utility, found in the Utilities folder under Applications.\nSelect your USB drive under External in the left column and click Erase in the top bar.\nChoose a name for the drive; for this guide, `WIN10USB` will be used. Set the format as 'MS-DOS (FAT)' and the partition scheme as 'GUID Partition Map'. Click erase.", inline=False)
        embed.add_field(name="Step 4:", value="Find the ISO file in Finder and double click to mount it.\nOpen Terminal, also found in the Utilities folder, and run the command `ls /Volumes`. CCCOMA_X64FRE_EN-US_DV9 and WIN10USB should both be listed.", inline=False)
        embed.add_field(name="Step 5:", value="Use the terminal to install the [brew](https://brew.sh) package manager if it isn't installed already.\nOnce brew is installed, run the command `brew install wimlib`.", inline=False)
        embed.add_field(name="Step 6:", value="Run the command `rsync -av --exclude=sources/install.wim /Volumes/CCCOMA_X64FRE_EN-US_DV9/ /Volumes/WIN10USB/` to copy the Windows installation files to the USB drive.", inline=False)
        embed.add_field(name="Step 7:", value="Run the command `wimlib-imagex split /Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim /Volumes/WIN10USB/sources/install.swm 3500` to split install.wim into chunks small enough to fit into a FAT32 partition.", inline=False)
        embed.add_field(name="Step 8:", value="Eject the drive by dragging it into the trash can or right clicking and selecting eject.\nYou are finally done! To install Windows onto another computer, run the `/windowsusb` command and follow the instructions from step 5.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to create a bootable Windows USB on Mac OS X")
    async def osxwinusb(self, ctx):
        embed = discord.Embed(title="How to create bootable Windows 10 install media on Mac OS X", description="**Note:** This will only work on OS X 10.15 Mojave or earlier. If you're using macOS 11 Big Sur or later, you need to follow the instructions given by `/macwinusb` instead.", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Plug in a USB flash drive with at least 8 GB of capacity, that you don't mind erasing.", inline=False)
        embed.add_field(name="Step 2:", value="Go to https://microsoft.com/en-us/software-download/windows10ISO and download a Windows 10 ISO.", inline=False)
        embed.add_field(name="Step 3:", value="Open the Boot Camp Assistant application. It should be located in the Utilities folder under Applications.\nAt the introduction step, click continue.\nAt the 'Select Tasks' screen, make sure only the 'Create a Windows 10 or later install disk' box is checked ([picture](https://discussions.apple.com/content/attachment/87d23c1b-a4b5-4549-b58a-6c57e8d5e926)). Click continue.", inline=False)
        embed.add_field(name="Step 4:", value="In the next screen, choose the ISO file that you downloaded previously and select the correct USB drive to flash it to. Make sure the correct drive is selected, because this process will wipe its contents. Click continue.", inline=False)
        embed.add_field(name="Step 5:", value="If Boot Camp Assistant asks for your password, enter it. This gives the application permission to wipe your USB and put the Windows installer on it. The process of flashing the drive will take some time. When it's done, eject the drive by dragging it into the trash can or right clicking and selecting eject.", inline=False)
        embed.add_field(name="Step 6:", value="Congratulations, you now have bootable Windows 10 install media! To install Windows onto another (or the same) computer, run the `/windowsusb` command and follow the instructions from step 5.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to create a bootable Linux USB")
    async def linuxusb(self, ctx):
        embed = discord.Embed(title="How to get a Linux Live USB", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Decide what desktop environment is best for you.\nIf you prefer [KDE Plasma](https://kde.org/), use [Fedora KDE](https://fedoraproject.org/spins/kde).\nIf you prefer [GNOME](https://www.gnome.org/), use [Fedora Workstation](https://fedoraproject.org/workstation/).", inline=False)
        embed.add_field(name="Step 2:", value="Download the Linux ISO and the flashing tool.\nDownload the Linux ISO from one of the links above. If you chose Fedora, make sure to download the x86_64 ISO instead of Fedora Media Writer.\nFor the flashing tool, you can use [balenaEtcher](https://balena.io/etcher/) or [Rufus](https://rufus.ie).\nbalenaEtcher is simple and gets the job done fast; Rufus has many more features, but it can be confusing to beginners.", inline=False)
        embed.add_field(name="Step 3:", value="Once everything is downloaded, use the flashing tool to flash your ISO to a USB (must be 4 GB or larger).\nSelect the Linux ISO you downloaded and the USB you want to flash to, then start the flashing process.\nWhen the flashing is done, unplug the USB and plug it into the device you want to boot into Linux (if it's the same device, just leave it plugged in and shut down the PC).", inline=False)
        embed.add_field(name="Step 4:", value="Boot into Linux.\nTurn on the computer and start spamming the boot menu key (figure out which one yours is with the `!bootkeys` command) until the menu appears.\nWhen the menu shows up, select the USB to boot to.", inline=False)
        embed.add_field(name="Step 5:", value="Install or try out linux.\nYour computer will boot to show the Linux desktop. Note that Linux is not installed on the computer; this is called a Live USB, where you can test it out before installation. While anything you do on the USB in this state will not be saved, be aware that certain actions, such as modifying partitions, can have permanent and irreversible effects on your PC. If you wish to replace Windows with Linux, open the 'Install Linux' file on the desktop. If you want to return to Windows on the next reboot, simply restart the PC with the USB unplugged.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to flash a Linux ISO to USB on Android")
    async def androidusb(self, ctx):
        embed = discord.Embed(title="How to flash a Linux ISO to USB on Android", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Make sure you can actually plug your USB into the phone.\nIn a perfect world, you'll have a USB-C flash drive and a USB-C phone, so you can just plug it in. Unfortunately, most of the time it's USB type A and the phone is either Micro B or USB-C.\nIf this is the case, buy an adapter like one of these:\n[USB Micro B (most older phones)](https://amazon.com/dp/B00LN3LQKQ)\n[USB-C (most newer phones)](https://amazon.com/dp/B01GGKYXVE)", inline=False)
        embed.add_field(name="Step 2:", value="Download EtchDroid from [Google Play](https://play.google.com/store/apps/details?id=eu.depau.etchdroid) or manually install the APK from [here](https://github.com/EtchDroid/EtchDroid/releases/download/v1.5/EtchDroid-v1.5-release.apk).", inline=False)
        embed.add_field(name="Step 3:", value="Follow the instructions from EtchDroid's official YouTube tutorial: https://youtu.be/6gM5SoNO0Fc", inline=False)
        embed.set_footer(text="Note: EtchDroid will not work for Windows ISOs as they don't follow the ISOHybrid standard.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get instructions on how to run the system file checker in Windows 11")
    async def windowsrepair(self, ctx):
        embed = discord.Embed(title="How to repair Windows 11", description="System File Checker is a utility in Windows that checks for problems with files on your computer.", color=0x00a0a0)
        embed.add_field(name="Step 1:", value="Make sure you've installed the latest updates for Windows, and then restart your machine.", inline=False)
        embed.add_field(name="Step 2:", value="In the search box on the taskbar, type command prompt, and right-click or press and hold Command Prompt (Desktop app) from the list of results. Select Run as administrator, and then select Yes.", inline=False)
        embed.add_field(name="Step 3:", value="Type `DISM.exe /Online /Cleanup-image /Restorehealth`, and then press Enter.\n**Note:** This step may take a few minutes to start and complete.", inline=False)
        embed.add_field(name="Step 4:", value="After you see a message that says **The operation completed successfully**, type `sfc /scannow` and press Enter.", inline=False)
        embed.add_field(name="Step 5:", value="After you see a message that says **Verification 100% complete**, type `exit` and press Enter.", inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=['windows7', 'windows8'], description="Explain why Windows 7 and 8 should not be used")
    async def legacywindows(self, ctx):
        embed = discord.Embed(title="Legacy versions of Windows", description="Windows 7 and 8 are no longer officially supported by Microsoft, while [Windows 10 reaches end of support on October 14, 2025](https://www.microsoft.com/en-us/windows/end-of-support).\nUsing older versions of windows puts you at risk to malware and other vulnerabilities (even if you're careful), which can easily be avoided by upgrading your operating system.", color=0x00a0a0)
        embed.add_field(name="What can I do?", value="If your computer is good enough to run Windows 11 reliably, download the [Windows 11 Installation Assistant](https://www.microsoft.com/en-us/software-download/windows11).\nIf your computer isn't good enough to run Windows 11 very well, it's recommended to switch to a lighter Linux distribution such as [Fedora LXQt](https://fedoraproject.org/spins/lxqt). Instructions are available with the `!linuxusb` command.", inline=False)
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

    @commands.hybrid_command(description="Show the difference between various display connectors")
    async def videoports(self, ctx):
        await ctx.send(file=discord.File('images/video-ports.png', 'video-ports.png'))

    @commands.hybrid_command(description="Show the difference between SATA and NVMe M.2 SSDs using differently keyed M.2 connectors")
    async def m2(self, ctx):
        files = [discord.File('images/m.2-key-type.jpg', 'key-type.jpg'), discord.File('images/m.2-drive-type.jpg', 'drive-type.png')]
        await ctx.send(files=files)

async def setup(bot):
    await bot.add_cog(techinfo(bot))
