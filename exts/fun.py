"""
Fun extension for r-wlw-bot
---
Copyright (C) 2019-2021 classabbyamp, 0x5c

This file is part of r-wlw-bot and is released under the terms of
the GNU General Public License, version 2.
"""


import json
import random

import discord.ext.commands as commands

import common as cmn


class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="xkcd", aliases=["x"], category=cmn.Cats.FUN)
    async def _xkcd(self, ctx: commands.Context, number: int):
        """Looks up an xkcd comic by number."""
        await ctx.send("http://xkcd.com/" + str(number))

    @commands.command(name="tar", category=cmn.Cats.FUN)
    async def _tar(self, ctx: commands.Context):
        """Returns xkcd: tar."""
        await ctx.send("http://xkcd.com/1168")

    @commands.command(name="standards", category=cmn.Cats.FUN)
    async def _standards(self, ctx: commands.Context):
        """Returns xkcd: Standards."""
        await ctx.send("http://xkcd.com/927")


def setup(bot: commands.Bot):
    bot.add_cog(FunCog(bot))
