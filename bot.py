import discord
import asyncio
import secrets
import hinter
from discord.ext.commands import Bot

# Means you will call commands by writing "!<name of command>" in Discord
NFTestBot = Bot(command_prefix="!")

# Stuff that happens when you turn this mofo on. (Print goes to the console you start this from, not a Discord chat)
@NFTestBot.event
async def on_ready():
    print("DFTB-DFTB-DFTB READY!")

# Anotate your command methods this way, using "command()" after your bot's name
@NFTestBot.command()
async def hello(*args):
    return await NFTestBot.say("YO!!")


@NFTestBot.command(pass_context=True)
async def waluigi(ctx):
    await NFTestBot.say("Hey, " + ctx.message.author + "http://i.imgur.com/GfR30jl.gif")

# You can add commands from another class this way:
NFTestBot.add_cog(hinter.Hinter(NFTestBot))

NFTestBot.run(secrets.BOT_TOKEN)
