"""
Base extension for r-wlw-bot
---
Copyright (C) 2019-2021 classabbyamp, 0x5c

This file is part of r-wlw-bot and is released under the terms of
the GNU General Public License, version 2.
"""


from datetime import datetime
from io import BytesIO
import asyncio

import asyncpraw

import discord
from discord.ext import commands

import common as cmn
from data import keys
from data import options as opt


class RedditCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(client_id=keys.reddit_app_id,
                                       client_secret=keys.reddit_secret,
                                       user_agent="r/wlw subreddit feed bot by classabbyamplifier")
        self.reddit.read_only = True
        self.pub_chan = None
        self.mod_chan = None

    @commands.Cog.listener("on_ready")
    async def post_feed(self):
        self.pub_chan = self.bot.get_channel(opt.public_feed_channel)
        self.mod_chan = self.bot.get_channel(opt.mod_feed_channel)

        subreddit = await self.reddit.subreddit(opt.subreddit)

        while not self.bot.is_closed():
            try:
                async for post in subreddit.stream.submissions(skip_existing=True, pause_after=0):
                    selftext_file = None
                    if post:
                        preview = discord.Embed(colour=cmn.colours.pink)
                        if post.created_utc:
                            preview.timestamp = datetime.fromtimestamp(post.created_utc)
                        if post.id:
                            preview.set_footer(text="id: " + post.id)
                        if post.author:
                            await post.author.load()
                            if post.author.name:
                                if post.author.icon_img:
                                    preview.set_author(name=post.author.name,
                                                       url="https://www.reddit.com/user/" + post.author.name,
                                                       icon_url=post.author.icon_img)
                                else:
                                    preview.set_author(name=post.author.name,
                                                       url="https://www.reddit.com/user/" + post.author.name)
                        if post.title:
                            preview.title = post.title[:250] + "..." if len(post.title) >= 250 else post.title
                        else:
                            preview.title = "Title not Found"
                        if post.link_flair_text:
                            preview.add_field(name="Flair", value=post.link_flair_text)
                        if post.permalink:
                            preview.url = "https://www.reddit.com" + post.permalink
                            preview.add_field(name="URL", value="https://www.reddit.com" + post.permalink)

                        full = preview.copy()
                        if post.selftext:
                            if not post.over_18:
                                preview.description = post.selftext[:500] + "..." if len(post.selftext) > 500 else post.selftext
                            else:
                                preview.description = "NSFW Post"
                            if len(post.selftext) >= 2048:
                                full.description = "See attached file for full text."
                                selftext_file = discord.File(BytesIO(post.selftext.encode("utf-8")), f"{post.id}.txt")
                            else:
                                full.description = post.selftext

                        if self.pub_chan:
                            await self.pub_chan.send(embed=preview)
                        if self.mod_chan:
                            if selftext_file:
                                await self.mod_chan.send(embed=full, file=selftext_file)
                            else:
                                await self.mod_chan.send(embed=full)
                    else:
                        await asyncio.sleep(10)
            except Exception as e:
                print(e)
                self.mod_chan.send((f"<@!{opt.owners_uids[0]}>, the post feed seems to be broken!\n"
                                    f"See error message:\n```\n{e}\n```"),
                                   allowed_mentions=discord.AllowedMentions.all())
                await asyncio.sleep(30)

    @commands.Cog.listener("on_ready")
    async def comment_feed(self):
        subreddit = await self.reddit.subreddit(opt.subreddit)

        while not self.bot.is_closed():
            try:
                async for com in subreddit.stream.comments(skip_existing=True, pause_after=0):
                    body_file = None
                    if com:
                        embed = discord.Embed(colour=cmn.colours.purple)
                        if com.link_id:
                            embed.title = f"New comment on Post `{com.link_id.removeprefix('t3_')}`"
                        else:
                            embed.title = "New Comment"
                        if com.created_utc:
                            embed.timestamp = datetime.fromtimestamp(com.created_utc)
                        if com.id:
                            embed.set_footer(text="id: " + com.id)
                        if com.author:
                            await com.author.load()
                            if com.author.name:
                                if com.author.icon_img:
                                    embed.set_author(name=com.author.name,
                                                     url="https://www.reddit.com/user/" + com.author.name,
                                                     icon_url=com.author.icon_img)
                                else:
                                    embed.set_author(name=com.author.name,
                                                     url="https://www.reddit.com/user/" + com.author.name)
                        if com.body:
                            if len(com.body) >= 2048:
                                embed.description = "See attached file for full text."
                                body_file = discord.File(BytesIO(com.body.encode("utf-8")), f"{com.id}.txt")
                            else:
                                embed.description = com.body
                        if com.permalink:
                            embed.url = "https://www.reddit.com" + com.permalink
                            embed.add_field(name="URL", value="https://www.reddit.com" + com.permalink)
                        if self.mod_chan:
                            if body_file:
                                await self.mod_chan.send(embed=embed, file=body_file)
                            else:
                                await self.mod_chan.send(embed=embed)
                    else:
                        await asyncio.sleep(10)
            except Exception as e:
                print(e)
                self.mod_chan.send((f"<@!{opt.owners_uids[0]}>, the comment feed seems to be broken!\n"
                                    f"See error message:\n```\n{e}\n```"),
                                   allowed_mentions=discord.AllowedMentions.all())
                await asyncio.sleep(30)


def setup(bot: commands.Bot):
    bot.add_cog(RedditCog(bot))
