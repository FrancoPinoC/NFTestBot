import discord
from discord.ext import commands
import traceback
import sys
import secrets
import hinter
from discord.ext.commands import Bot
import config

# Means you will call commands by writing "!<name of command>" in Discord
NFTestBot = Bot(command_prefix="!")
passwords = config.Config('passwords.json')

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


@NFTestBot.command(aliases=["aBunny", "ABunny", "A_Bunny"])
async def a_bunny():
    bunny = ":\n" \
            "(\\\\(\\ \n" \
            "( - -)\n" \
            "((') (')"
    return await NFTestBot.say(bunny)

#Experimental command. Ask the bot to let you become role_name if you give it the right password.
@NFTestBot.command(pass_context=True)
async def role_it(ctx, role_name):
    member = ctx.message.author
    # role_name needs to be a role of lesser hierarchy than the bot's role. Just give the bot admin power and make the
    # role not be an admin role and it should work (admins can still use this command)
    role = discord.utils.find(lambda r: r.name == role_name, ctx.message.server.roles)
    # passwords it's just a json with this kinda content (this command will raise an error if the json doesn't exist)
    # {"week0":"pass1","week1":"pass2"}
    global passwords
    # I don't know why I don't have to call "passwords.all()" here and instead can do this directly.
    password = passwords["week0"]
    # Delete message so as to not clog with the chat with messages of people attempting to get the pass right.
    await NFTestBot.delete_message(ctx.message)
    await NFTestBot.send_message(member, 'Respond here with the password and I will let you in if it\'s correct.\n')

    def check(m):
        return m.author.id == member.id and \
               m.channel.is_private
    reply = await NFTestBot.wait_for_message(check=check, timeout=1500.0)
    if reply is None:
        return await NFTestBot.say("Time's up, {0.mention}. You gotta call the command again to try again".format(member))
    if reply.content.strip() != password:
        return await NFTestBot.send_message(member, "That's not the password.\n"
                                                    "http://www.icge.co.uk/languagesciencesblog/wp-content/uploads/2014"
                                                    "/04/you_shall_not_pass1.jpg")
    else:
        await NFTestBot.send_message(member, "Well done")
    await NFTestBot.add_roles(member, role)
    return await NFTestBot.say("{0.mention} evolved into {1.name}!".format(member, role))


# You can add commands from another class this way:
NFTestBot.add_cog(hinter.Hinter(NFTestBot))

NFTestBot.run(secrets.BOT_TOKEN)
