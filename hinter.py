# Use of Config was copied from here:
# https://github.com/Rapptz/RoboDanny/blob/master/cogs/pokemon.py
from discord.ext import commands
import config


class Hinter:
    def __init__(self, bot):
        self.config = config.Config('hints.json')
        self.bot = bot

    # Use "commands" to later add this command to a bot (in this case self.bot) as part of a cog. See bot.py for more.
    @commands.command(aliases=["addHint", "AddHint"],
                      description="Add a hint. First argument is the name or topic you are going to use to later "
                                  "retrieve the hint, the second argument is the hint itself. Surround with quotes if "
                                  "the hint uses more than one word.")
    async def add_hint(self, hint_name, hint_content):
        hints = self.config.all()
        try:
            hint = hints[hint_name]
        except KeyError:
            # not found, so create it. Relying on errors is bad form... but eh.
            await self.config.put(hint_name, hint_content)
            return await self.bot.say("A hint for '" + hint_name + "' has been added!")
        else:
            # Get hint:
            return await self.bot.say("There's already a hint for {0}! It's this:\n"
                                      "```\n{1}\n```".format(hint_name, hint))

    @commands.command(aliases=["delHint", "DelHint"], description="Delete the hint for the chosen topic.")
    async def del_hint(self, hint_name):
        try:
            await self.config.remove(hint_name)
        except KeyError:
            return await self.bot.say("There wasn't any hint for '" + hint_name +
                                      "', please add a hint for that so you can delete it :robot:")
        else:
            return await self.bot.say(hint_name + " has been removed from the hints list.")

    @commands.command(aliases=["hintPls"], description="Give me a topic or hint name and I will give you"
                                                       "a hint for it. If the name is more than one word"
                                                       "long, surround it with \"quotation marks\"")
    async def hint_pls(self, hint_name):
        hints = self.config.all()
        try:
            hint = hints[hint_name]
        except KeyError:
            return await self.bot.say("There's not hint for " + hint_name + ". Maybe ask someone else :[?")
        else:
            return await self.bot.say('The hint for %s is:\n ```\n%s\n```' % (hint_name, hint))

    @commands.command(aliases=["hintsList", "hint_list", "hintList", "all_hints", "allHints"])
    async def hints_list(self):
        #Backticks are used for code formatting which gives the list a nice look
        hints = self.config.all()
        if not hints:
            return await self.bot.say("Sorry, there are no hints at all... but ask humans, I hear they are nice")
        result = "We have hints for the following topics:\n```\n"
        print(hints)
        for hint_name in hints:
            result += hint_name + "\n"
        result += "```"
        return await self.bot.say(result)
