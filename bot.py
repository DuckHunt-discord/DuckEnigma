#!/usr/bin/env python3.6
# This is DuckHunt V3
# You have to use it with the rewrite version of discord.py
# You can install it using
# pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
# You also have to use python 3.6 to run this
# Have fun !
# The doc for d.py rewrite is here : http://discordpy.readthedocs.io/en/rewrite/index.html

# Importing and creating a logger

import logging
import traceback

import time
from typing import Union

import cogs.helpers.aux_inits as inits
from cogs.helpers import checks
from cogs.helpers.context import CustomContext

base_logger = inits.init_logger()

extra = {"channelid": 0, "userid": 0}
logger = logging.LoggerAdapter(base_logger, extra)

logger.info("Starting the bot")

# Setting up asyncio to use uvloop if possible, a faster implementation on the event loop
import asyncio

try:
    import uvloop
except ImportError:
    logger.warning("Using the not-so-fast default asyncio event loop. Consider installing uvloop.")
    pass
else:
    logger.info("Using the fast uvloop asyncio event loop")
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Importing the discord API warpper
import discord
import discord.ext.commands as commands


# Prepare the bot object

async def get_prefix(bot, message):
    extras = ["-", "e-", "en"]
    return commands.when_mentioned_or(*extras)(bot, message)


logger.debug("Creating a bot instance of commands.AutoShardedBot")

from cogs.helpers import context


class DuckHunt(commands.AutoShardedBot):
    async def on_message(self, message):
        if message.author.bot:
            return  # ignore messages from other bots

        if message.author.id in self.blacklisted_users:
            return

        ctx = await self.get_context(message, cls=context.CustomContext)
        if ctx.prefix is not None:
            # ctx.command = self.all_commands.get(ctx.invoked_with.lower())  # This dosen't works for subcommands
            await self.invoke(ctx)

    async def on_command(self, ctx):
        bot.commands_used[ctx.command.name] += 1
        ctx.logger.info(f"<{ctx.command}> {ctx.message.clean_content}")
        try:
            await ctx.message.delete()
        except:
            pass


    async def update_playing(self):
        await self.wait_until_ready()
        game = discord.Game(name=f"{self.guilds[0].member_count} users")
        await bot.change_presence(status=discord.Status.online, activity=game)

    async def on_ready(self):
        logger.info("We are all set, on_ready was fired! Yeah!")
        logger.info(f"I see {len(self.guilds)} guilds")
        await self.update_playing()

    async def on_member_join(self, member):
        await self.update_playing()

    async def on_member_remove(self, member):
        await self.update_playing()

    async def on_command_error(self, context, exception):
        if isinstance(exception, discord.ext.commands.errors.CommandNotFound):
            return

        elif isinstance(exception, discord.ext.commands.errors.MissingRequiredArgument):
            await context.send(":x: A required argument is missing.", delete_after=5)  # Here is the command documentation : \n```\n", language) + context.command.__doc__ +
            # "\n```")
            return
        elif isinstance(exception, checks.NotADirectMessage):
            await context.send(":x: DM me this command to use it", delete_after=5)
            return
        elif isinstance(exception, checks.NotPlayer):
            await context.send(":x: Tsss... You can't do this and you know it", delete_after=5)
            return
        elif isinstance(exception, checks.NotSuperAdmin):
            await context.send(":x: You are not a super admin.", delete_after=5)
            return
        elif isinstance(exception, checks.NoVotesOnDBL):
            await context.send(":x: You haven't voted for DuckHunt on DiscordBotList for a while.", delete_after=5)
            await self.hint(ctx=context, message="Support the bot to use this command by voting at <https://discordbots.org/bot/duckhunt>. " \
                                                 "Be aware that the votes can take a minute to be registered by Duckhunt" \
                                                 "If you think this is an error, please contact my owner at the DuckHunt Support Server (see `dh!help`).")
            return
        elif isinstance(exception, discord.ext.commands.errors.CheckFailure):
            return
        elif isinstance(exception, discord.ext.commands.errors.CommandOnCooldown):
            if context.message.author.id in self.admins:
                await context.reinvoke()
                return
            else:

                await context.send("You are on cooldown :(, try again in {seconds}".format(seconds=round(exception.retry_after, 1)))
                return
        logger.error('Ignoring exception in command {}:'.format(context.command))
        logger.error("".join(traceback.format_exception(type(exception), exception, exception.__traceback__)))

    async def hint(self, ctx, message):
        hint_start = ctx.bot._(":bulb: HINT: ")
        await ctx.send(ctx, message=hint_start + message)


bot = DuckHunt(command_prefix=get_prefix, case_insensitive=True)

logger.debug("Configuring the bot")

from cogs.helpers.config import config

config(bot)
bot.base_logger = base_logger
bot.logger = logger

logger.debug("> Loading complete")

logger.debug("Loading cogs : ")

######################
#                 |  #
#   ADD COGS HERE |  #
#                 V  #
#################   ##
#################   ##
################   ###
###############   ####
##############   #####

cogs = ['cogs.superadmin_commands', 'cogs.evals', 'cogs.enigma'  # This must be the last to run, comment if you don't need it
        ]

for extension in cogs:
    try:
        bot.load_extension(extension)
        logger.debug(f"> {extension} loaded!")
    except Exception as e:
        logger.exception('> Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

logger.debug("Everything seems fine, we are now connecting to discord.")
try:
    # bot.loop.set_debug(True)
    bot.loop.run_until_complete(bot.start(bot.token))
except KeyboardInterrupt:
    pass
finally:
    # Stop cleanly : make ducks leave
    # try:
    game = discord.Game(name=f"Restarting...")
    bot.loop.run_until_complete(bot.change_presence(status=discord.Status.dnd, activity=game))

    # except:
    #    pass

    bot.loop.run_until_complete(bot.logout())

    asyncio.sleep(3)
    bot.loop.close()
