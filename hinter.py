from discord.ext import commands
import config

class Hinter:
    def __init__(self, bot):
        # When you see how hints is used you will think "OMFG WHAT ABOUT THE RACE CONDITIONS"... you will be right.
        self.config = config.Config('hints.json')
        self.bot = bot

    # Use "commands" to later add this commands to a bot (in this case self.bot) as part of a cog. See bot.py for more.
    @commands.command(aliases=["addHint", "AddHint"], description="Add a hint. First argument is the name you are "
                                                               "going to use to later retrieve the hint, the second "
                                                               "argument is the hint itself. Surround with quotes if "
                                                               "the hint uses more than one word.")
    async def add_hint(self, hintname, hint):
        if hintname in self.hints:
            return await self.bot.say("A hint named '" + hintname + "' already exists.\n"
                          "please delete existing hint using '!del_hint' or choose another name.")
        else:
            # You may be thinking "OMFG RACECONDITIONS"... you are right.
            self.hints[hintname] = hint
            return await self.bot.say("Added hint '" + hintname + "'.")

    @commands.command(aliases=["delHint", "DelHint"], description="Give me a topic or hint name and I will give you"
                                                                  "a hint for it. If the name is more than one word"
                                                                  "long, surround it with \"quotation marks\"")
    async def del_hint(self, hintname):
        if hintname not in self.hints:
            return await self.bot.say("There is no hint named '" + hintname + "'.")
        else:
            del self.hints[hintname]
            return await self.bot.say("Deleted hint '" + hintname + "'.")

    @commands.command(aliases=["hintPls"])
    async def hint_pls(self, hintname):
        if hintname not in self.hints:
            return await self.bot.say("Sorry, there's no hint for '" + hintname + "'.")
        else:
            hint = self.hints[hintname]
            return await self.bot.say(hint)

    @commands.command()
    async def hints_list(self):
        #Backticks are used for code formatting which gives the list a nice look
        if not self.hints:
            return await self.bot.say("Sorry, there are no hints at all... but ask humans, I hear they are nice")
        result = "We have hints for the following topics:\n```"
        for hintname in self.hints:
            result += hintname + "\n"
        result += "```"
        return await self.bot.say(result)

    @commands.command()
    async def save_hints(self):
        return
