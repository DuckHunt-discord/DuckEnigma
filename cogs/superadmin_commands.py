import inspect
from discord.ext import commands
from cogs.helpers import checks


class SuperAdmin:

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["quit", "stop"])
    @checks.is_super_admin()
    async def exit(self, ctx):
        """Quit the bot, duh"""
        await self.bot.log(level=40, title="Bot is restarting", message=f"Exited with command", where=ctx)
        raise KeyboardInterrupt("Exited with command")

def setup(bot):
    bot.add_cog(SuperAdmin(bot))
