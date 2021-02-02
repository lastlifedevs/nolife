#!/usr/bin/env python3

import discord
import logging
import config
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='nolife.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

role_message_id = config.role_message_id

class NoLifeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.emoji_to_role = {
            '🇸': config.she_her,
            '🇹': config.they_them,
            '🇭': config.he_him,
            '🇮': config.it_its,
            '🇦': config.any_pronouns,
            '❔': config.ask_for_pronouns
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
            role_id = self.emoji_to_role[payload.emoji.name]
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

intents = discord.Intents.default()
intents.members = True
bot = NoLifeBot(command_prefix='!', intents=intents)

@bot.command()
@commands.has_any_role(*config.authenticated_roles)
async def postMsg(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
@commands.has_any_role(*config.authenticated_roles)
async def editRoleMsg(ctx, *, arg):
    msg = await ctx.fetch_message(role_message_id)
    await msg.edit(content=arg)

@bot.command()
@commands.has_any_role(*config.authenticated_roles)
async def addInitialReactions(ctx):
    msg = await ctx.fetch_message(role_message_id)
    await msg.add_reaction('🇦')
    await msg.add_reaction('❔')

bot.run(config.token)