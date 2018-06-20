import gettext
import logging
import json
from collections import Counter

import discord
from discord.ext import commands

from cogs.helpers import context



def config(bot):
    """
    This function will populate the bot object.

    This is the main config file of the bot. Replace variables you want to modify between the

    ## START CONFIG HERE

    and

    ## END CONFIG HERE

    comments. Thanks for using DuckHunt :)
    """

    # Load credentials so they can be used later
    with open("credentials.json", "r") as f:
        credentials = json.load(f)

    ## START CONFIG HERE

    # Change this to True once you are ready to run the bot
    bot.configured = True

    bot.enigma_guild = 449663867841413120
    bot.log_channel = 449673132165300245


    # This is the bot token. Used by the bot to connect to discord.
    # As this is a sensitive setting, you need to change it in credentials.json
    bot.token = credentials["token"]

    # > User settings < #
    # This is a list of users IDs that are set as super admins on the bot. The bot will accept any command, from them,
    # regardless of the server and their permissions there
    bot.admins = [138751484517941259]

    # This is a list of users that are blacklisted from the bot. The bot will ignore dem messages
    bot.blacklisted_users = [
        # 2018-03-01
        # Abused a bug in the bot to set his server to 99999999999 ducks per day, and didn't report. Lagged the bot for a few hours
        #377585801258598410,

        # 2018-03-01
        # Admin on the previous guy server
        # 293533150204657675,

        # 2018-03-01
        # Abused a bug in the bot to set his server to 99999999999 ducks per day, and didn't report. Lagged the bot for a few hours.
        # Unrelated to the two previous guys
        386516042882482177,

        # 2018-03-01
        # Abused a bug in the bot to set his server to 99999999999 ducks per day, and didn't report. Lagged the bot for a few hours
        # Unrelated too
        # > Was sorry so unbanned
        # 330841376474267651,

        # 2018-04-15
        # Abused the unlimited number of channels to get an higer number of ducks on his 5 members guild.
        # With 26 channels created, we have a winner.
        # https://api-d.com/snaps/2018-04-15_23-14-13-3ggwqd57mj.png
        331466244131782661,

        # 2018-04-15
        # Abused the unlimited number of channels to get an higer number of ducks on his 1 member guild.
        # [20]Tunbridge Wells PoGo Raid (342562516850704385) : Owned by 339294911935414272 with 5 members
        # 20 channels total, owner of the server
        339294911935414272,

        # All for now
        ]

    bot.commands_used = Counter()

    ## END CONFIG HERE










