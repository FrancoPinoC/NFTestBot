import discord
from discord.ext import commands
import traceback
import sys
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
@NFTestBot.command(pass_context=True)
async def hello(context, member: discord.Member = None):
    # "context" is the context that's being passed.
    # I don't know why you need to make member default to None, but you do.
    if member is None:
        member = context.message.author
    botname = NFTestBot.user.name
    return await NFTestBot.say("YO " + member.mention + "!!")


@NFTestBot.command(pass_context=True)
async def waluigi(ctx):
    # Just a test. This method will PM whoever used this command
    return await NFTestBot.send_message(ctx.message.author,
                                        "Hey, " + ctx.message.author.name + " http://i.imgur.com/GfR30jl.gif")


# This method triggers when the event of a member joining occurs.
@NFTestBot.event
async def on_member_join(member):
    # Greets whoever joined in (I'm assuming) the default channel of 'server' (usually #general).
    server = member.server
    # Finds a channel so that we can link to it in our welcome message
    useful_channel = discord.utils.get(server.channels, name='rules_and_information')
    welcome = "Hey, {0.mention}! Welcome to {1.name}!\n" \
              "I am {2.user.name} an automated :robot:. You can see a list of my commands by messaging me '!help' " \
              "(without the quotes. Just click on my name from the members list and send me that message).\n\n"\
              "Please go here {3.mention} for general directions.\n" \
              "Don't be afraid to ask the meatbags anything! Have fun and DFTBA!"
    return await NFTestBot.send_message(server, welcome.format(member, server, NFTestBot, useful_channel))


# Shuts the bot down. Admins only
@NFTestBot.command(pass_context=True)
async def kill_bot(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    if not member.server_permissions.administrator:
        return await NFTestBot.say("Lol. You need to evolve into an admin if you want to take me on pal Q('-'Q).")
    await NFTestBot.say("That's not even nice, but ok...")
    return await NFTestBot.logout()


@NFTestBot.command(pass_context=True, aliases=["memberCount", "countMembers", "count_members"])
async def member_count(ctx):
    server = ctx.message.server
    count = server.member_count
    return await NFTestBot.say("There are {} members in this server.".format(count))


@NFTestBot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return await NFTestBot.send_message(ctx.message.channel, 'The command you attempted to use does not exist')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
    elif isinstance(error, commands.BadArgument):
        return await NFTestBot.send_message(ctx.message.channel, 'Whoa, something was wrong with '
                                                                 'the arguments you passed there')
    return


# You can add commands from another class this way:
NFTestBot.add_cog(hinter.Hinter(NFTestBot))

NFTestBot.run(secrets.BOT_TOKEN)
