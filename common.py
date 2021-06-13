"""
Common tools for the bot.
---
Copyright (C) 2019-2021 classabbyamp, 0x5c

This file is part of r-wlw-bot and is released under the terms of
the GNU General Public License, version 2.
"""


import enum
import re
import traceback
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Union

import aiohttp

import discord
import discord.ext.commands as commands
from discord import Emoji, Reaction, PartialEmoji

import data.options as opt


__all__ = ["colours", "BoltCats", "Cats", "emojis", "paths", "embed_factory",
           "error_embed_factory", "add_react", "check_if_owner"]


# --- Common values ---

colours = SimpleNamespace(
    good=0x43B581,
    neutral=0x7289DA,
    bad=0xF04747,
    timeout=0xF26522,
    pink=0xF7A8DA,
    purple=0xB57EDC,
)


class BoltCats(enum.Enum):
    OTHER = "Other"
    INFO = "Bot Information"
    ADMIN = "Bot Control"


# meow
class Cats(enum.Enum):
    CALC = "Calculators"
    CODES = "Code References and Tools"
    FUN = "Fun"
    LOOKUP = "Information Lookup"
    REF = "Reference"
    STUDY = "Exam Study"
    TIME = "Time and Time Zones"
    UTILS = "Utilities"
    WEATHER = "Land and Space Weather"


emojis = SimpleNamespace(
    check_mark="✅",
    x="❌",
    warning="⚠️",
    question="❓",
    no_entry="⛔",
    bangbang="‼️",
    clock="🕗",
    stopwatch="⏱",
    a="🇦",
    b="🇧",
    c="🇨",
    d="🇩",
    e="🇪",
)

paths = SimpleNamespace(
    data=Path("./data/"),
)


# --- Exceptions ---

class BotHTTPError(Exception):
    """Raised whan a requests fails (status != 200) in a command."""
    def __init__(self, response: aiohttp.ClientResponse):
        msg = f"Request failed: {response.status} {response.reason}"
        super().__init__(msg)
        self.response = response
        self.status = response.status
        self.reason = response.reason


# --- Converters ---

class GlobalChannelConverter(commands.IDConverter):
    """Converter to get any bot-acessible channel by ID/mention (global), or name (in current guild only)."""
    async def convert(self, ctx: commands.Context, argument: str):
        bot = ctx.bot
        guild = ctx.guild
        match = self._get_id_match(argument) or re.match(r"<#([0-9]+)>$", argument)
        result = None
        if match is None:
            # not a mention/ID
            if guild:
                result = discord.utils.get(guild.text_channels, name=argument)
            else:
                raise commands.BadArgument(f"""Channel named "{argument}" not found in this guild.""")
        else:
            channel_id = int(match.group(1))
            result = bot.get_channel(channel_id)
        if not isinstance(result, (discord.TextChannel, discord.abc.PrivateChannel)):
            raise commands.BadArgument(f"""Channel "{argument}" not found.""")
        return result


# --- Helper functions ---

def embed_factory(ctx: commands.Context) -> discord.Embed:
    """Creates an embed with neutral colour and standard footer."""
    embed = discord.Embed(timestamp=datetime.utcnow(), colour=colours.neutral)
    embed.set_footer(text=str(ctx.author), icon_url=str(ctx.author.avatar_url))
    return embed


def error_embed_factory(ctx: commands.Context, exception: Exception, debug_mode: bool) -> discord.Embed:
    """Creates an Error embed."""
    if debug_mode:
        fmtd_ex = traceback.format_exception(exception.__class__, exception, exception.__traceback__)
    else:
        fmtd_ex = traceback.format_exception_only(exception.__class__, exception)
    embed = embed_factory(ctx)
    embed.title = "⚠️ Error"
    embed.description = "```\n" + "\n".join(fmtd_ex) + "```"
    embed.colour = colours.bad
    return embed


async def add_react(msg: discord.Message, react: Union[Emoji, Reaction, PartialEmoji, str]):
    try:
        await msg.add_reaction(react)
    except discord.Forbidden:
        idpath = (f"{msg.guild.id}/" if msg.guild else "") + str(msg.channel.id)
        print(f"[!!] Missing permissions to add reaction in '{idpath}'!")


# --- Checks ---

async def check_if_owner(ctx: commands.Context):
    if ctx.author.id in opt.owners_uids:
        return True
    raise commands.NotOwner
