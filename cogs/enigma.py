import json
import random

import discord
from discord.ext import commands
from discord.ext.commands import BucketType

from cogs.helpers import checks


class Enigma:
    def __init__(self, bot):
        self.bot = bot
        with open("enigmas.json", "r") as f:
            self.enigmas = json.load(f)
            self.bot.logger.info(f'{len(self.enigmas)} enigmas loaded!')

    async def get_player_level(self, user: discord.User):

        g = self.bot.get_guild(self.bot.enigma_guild)
        member = g.get_member(user.id)

        top_role = member.top_role.name

        try:
            return int(top_role)
        except TypeError:
            self.bot.logger.info(top_role)
            return 0  # Shouldn't happen except if he never played, but just in case we are allowing a spectator here, that works too
        except ValueError:
            return 0

    async def check_answer_for_level(self, level, answer_given):
        if "no-case" in self.enigmas[level]["flags"]:
            answer_given = answer_given.lower()

        if answer_given in self.enigmas[level]["answers"]:
            return True
        else:
            return False

    async def success(self, user):
        """
        A user won an enigma, let's make him progress to the next level!
        """

        g = self.bot.get_guild(self.bot.enigma_guild)
        log_chan = g.get_channel(self.bot.log_channel)

        previous_level = await self.get_player_level(user)
        next_level = previous_level + 1

        next_level_rank = discord.utils.get(g.roles, name=str(next_level).zfill(2))
        member = g.get_member(user.id)
        await member.add_roles(next_level_rank, reason="Solved enigma")

        embed = discord.Embed()
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_footer(text='I <3 Ducks')

        embed.title = f'Wow! {user.name} leveled up'
        embed.add_field(name='Level', value=f'{previous_level} -> {next_level}')

        await log_chan.send(embed=embed)

    @commands.command()
    @checks.in_private_message()
    @checks.is_player()
    @commands.cooldown(2, 30 * 60, type=BucketType.user)
    async def hint(self, ctx):
        """
        Get a hint, if available, on your current level enigma
        Warning, this command have a big cooldown : you can't use it more than every 10 minutes or so
        """
        level = await self.get_player_level(ctx.author)

        if len(self.enigmas[level]["hints"]) == 0:
            await ctx.send("No hints available for this level, sorry!")
        else:
            await ctx.send(random.choice(self.enigmas[level]["hints"]))

    @commands.command(aliases=['code'])
    @checks.in_private_message()
    @checks.is_player()
    @commands.cooldown(10, 120, type=BucketType.user)
    async def answer(self, ctx, *, answer_given):
        """
        Try to answer your current enigma level.
        """
        level = await self.get_player_level(ctx.author)

        embed = discord.Embed()
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_footer(text='I love Ducks')

        if await self.check_answer_for_level(level, answer_given):
            ctx.logger.debug(f"[Y - {level}] {answer_given} in {self.enigmas[level]['answers']}")


            embed.colour = discord.Colour.green()
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

            embed.title = f'Congratulations!'

            embed.add_field(name='Result', value=f'The answer provided is valid.')
            embed.add_field(name='Next moves', value=f'Use the `-info` command to learn more about the next enigma!')
            embed.add_field(name='Your level', value=f'{level} -> {level+1}')

            if self.enigmas[level]['win-message']:
                embed.add_field(name='A special message for you', value=self.enigmas[level]['win-message'])

            await ctx.send(embed=embed)

            await self.success(ctx.author)

        else:
            ctx.logger.debug(f"[X - {level}] {answer_given} not in {self.enigmas[level]['answers']}")

            embed.colour = discord.Colour.red()

            embed.title = f'Oh No!'

            embed.add_field(name='Result', value=f'The answer provided is invalid.')
            embed.add_field(name='Next moves', value=f'Use the `-hint` command to learn more about this question, maybe this will help you!')

            await ctx.send(embed=embed)

    @commands.command(aliases=['rank'])
    @checks.is_player()
    @commands.cooldown(2, 15, type=BucketType.user)
    async def level(self, ctx):
        """
        Show your current rank
        """

        level = await self.get_player_level(ctx.author)
        await ctx.send(f"{ctx.author.mention}, your level is {level}. Use the `-info` command to learn more!")

    @commands.command()
    @checks.in_private_message()
    @checks.is_player()
    @commands.cooldown(2, 15, type=BucketType.user)
    async def info(self, ctx):
        """
        Show your current level information
        """

        level = await self.get_player_level(ctx.author)
        embed = discord.Embed()
        embed.colour = discord.Colour.blurple()
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        embed.title = f'Your current level : {level}'

        embed.add_field(name='Question', value=f'{self.enigmas[level]["question"]}')

        embed.set_footer(text='I love Ducks')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Enigma(bot))
