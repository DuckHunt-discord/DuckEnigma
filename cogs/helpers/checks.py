import aiohttp
import time

import discord
from discord.ext import commands


def is_ready():
    async def predicate(ctx):
        await ctx.bot.wait_until_ready()
        return True

    return commands.check(predicate)


class NotSuperAdmin(commands.CheckFailure):
    pass


def is_super_admin():
    async def predicate(ctx):
        # await ctx.bot.wait_until_ready()
        cond = ctx.message.author.id in ctx.bot.admins
        ctx.logger.debug(f"Check for super-admin returned {cond}")
        if cond:
            return True
        else:
            raise NotSuperAdmin

    return commands.check(predicate)

class NotPlayer(commands.CheckFailure):
    pass


def is_player():
    async def predicate(ctx):
        g = ctx.bot.get_guild(ctx.bot.enigma_guild)
        member = g.get_member(ctx.author.id)

        if not member:
            raise NotPlayer

        spectators = ["spectator", "moderator"]

        for role in member.roles:
            if role.name.lower() in spectators:
                raise NotPlayer
        return True

    return commands.check(predicate)


class NotADirectMessage(commands.CheckFailure):
    pass


def in_private_message():
    async def predicate(ctx):
        # await ctx.bot.wait_until_ready()
        if isinstance(ctx.channel, discord.DMChannel):
            return True
        else:
            raise NotADirectMessage

    return commands.check(predicate)

DISCORD_BOTS_ORG_API = 'https://discordbots.org/api'
session = aiohttp.ClientSession()


class NoVotesOnDBL(commands.CheckFailure):
    pass


def voted_lately():
    async def predicate(ctx):
        player = ctx.message.author

        headers = {'authorization': ctx.bot.discordbots_org_key, 'content-type': 'application/json'}

        url = '{0}/bots/{1.user.id}/check?userId={2.id}'.format(DISCORD_BOTS_ORG_API, ctx.bot, player)
        async with session.get(url, headers=headers) as resp:
            cond = bool((await resp.json())['voted'])

        if cond:
            return True
        else:
            raise NoVotesOnDBL

    return commands.check(predicate)
