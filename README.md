# TSCBot-py
The current custom bot of [Tech Support Central](https://www.techsupportcentral.cf) written in Python.

## Dependencies
* Pycord
* PyMongo
* PyYAML
* [pypartpicker](https://github.com/quakecodes/pypartpicker)

## Assistant Bot
There are some things that the bot currently cannot do, that were previously part of the [JS Bot](https://github.com/TechSupportCentral/TSCBot-JS).
To provide those features, we have written a new [companion bot](https://github.com/TechSupportCentral/TSCBot-assistant) in JS.

## Pycord
The method in which this bot manages the muting of members is Discord's new timeout feature.
After the [discord.py](https://github.com/Rapptz/discord.py) library was [discontinued](https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1), newer features such as this couldn't be implemented.
This means that we are switching to [Pycord](https://github.com/Pycord-Development/pycord) to support these features.
The main reason this is important is that it uses the same `discord` library name as discord.py, so if someone tries to run the bot with discord.py, it'll appear to run fine until the bot tries to use one of the new Pycord features, where it will crash and leave the user confused about what caused it.
