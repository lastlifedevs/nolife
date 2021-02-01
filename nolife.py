#!/usr/bin/env python3

import discord
import logging
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='nolife.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

role_message_id = 805631453924294677

class NoLifeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.emoji_to_role = {
            '🇸': 805277339827044353, # she/her
            '🇹': 805277388098371644, # they/them
            '🇭': 805276868411785227, # he/him
            '🇮': 805280679779762196  # it/its
        }

    async def on_raw_reaction_add(self, payload):
        """Gives a role based on a reaction emoji."""
        if payload.message_id != role_message_id:
            return

        try:
            guild = self.get_guild(payload.guild_id)
            if guild is None:
                return
            role_id = self.emoji_to_role[payload.emoji.name]
            role = guild.get_role(role_id)
            if role is None:
                return
            await payload.member.add_roles(role)
        except KeyError:
            return
        except discord.HTTPException:
            pass

    async def on_raw_reaction_remove(self, payload):
        """Removes a role based on a reaction emoji."""
        if payload.message_id != role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
            guild = self.get_guild(payload.guild_id)
            if guild is None:
                return

            role = guild.get_role(role_id)
            if role is None:
                return

            member = guild.get_member(payload.user_id)

            if member is None:
                return
            await member.remove_roles(role)
        except KeyError:
            return
        except discord.HTTPException:
            pass

bot = NoLifeBot(command_prefix='!')

@bot.command()
@commands.has_any_role(83059413090308096, 730207364241948702)
async def postMsg(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
@commands.has_any_role(83059413090308096, 730207364241948702)
async def editRoleMsg(ctx, *, arg):
    msg = await ctx.fetch_message(role_message_id)
    await msg.edit(content=arg)

@bot.command()
@commands.has_any_role(83059413090308096, 730207364241948702)
async def addInitialReactions(ctx):
    msg = await ctx.fetch_message(role_message_id)
    await msg.add_reaction('🇸')
    await msg.add_reaction('🇹')
    await msg.add_reaction('🇭')
    await msg.add_reaction('🇮')

bot.run('token')