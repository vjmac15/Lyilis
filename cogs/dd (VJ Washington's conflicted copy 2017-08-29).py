import discord
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
import platform, asyncio, string, operator, random, textwrap
import os, re, aiohttp
from .utils.dataIO import fileIO
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
import time
import json
import random
import re
try:
    import scipy
    import scipy.misc
    import scipy.cluster
except:
    pass

prefix = fileIO("data/red/settings.json", "load")['PREFIXES']

dev = ["312127693242236928"]

class WarOfCrownRPG:
    def __init__(self, bot):
        self.bot = bot

    def _is_mention(self,user):
        if "mention" not in self.settings.keys() or self.settings["mention"]:
            return user.mention
        else:
            return user.name

    async def check_answer(self, ctx, valid_options):

        answer = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)

        if answer.content.lower() in valid_options:
            return answer.content

        elif answer.content in valid_options:
            return answer.content

        elif answer.content.upper() in valid_options:
            return answer.content

        else:
            return await self.check_answer(ctx, valid_options)

    @commands.command (pass_context = True)
    async def start(self, ctx):
        channel = ctx.message.channel
        server = channel.server
        user = ctx.message.author
        await self._create_user(user, server)
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")

        if not userinfo["class"] == "None" and not userinfo["race"] == "None":
            await self.bot.reply("Would you like to restart?")
            answer1 = await self.check_answer(ctx, ["yes", "no", "n", "y", ">start"])

            if answer1 == ">start":
                pass
            elif answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes":
                userinfo["gold"] = 0
                userinfo["race"] = "None"
                userinfo["class"] = "None"
                userinfo["enemieskilled"] = 0
                userinfo["equip"] = "None"
                userinfo["inventory"] = []
                userinfo["health"] = 100
                userinfo["deaths"] = 0
                userinfo["hp_potions"] = 0
                userinfo["inguild"] = "None"
                userinfo["guildhash"] = 0
                userinfo["lootbag"] = 0
                userinfo["name"] = user.name
                userinfo["location"] = "Golden Temple"
                userinfo["selected_enemy"] = "None"
                userinfo["daily_block"] = 0
                userinfo["rest_block"] = 0
                userinfo["in_dungeon"] = "False"
                userinfo["duneon_enemy_hp"] = 0
                userinfo["dungeon_enemy"] = "None"
                userinfo["wearing"] = "None"
                userinfo["keys"] = 0
                userinfo["roaming"] = "False"
                userinfo["lvl"] = 0
                userinfo["chop_block"] = 0
                userinfo["mine_block"] = 0
                userinfo["in_party"] = []
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
                await self.bot.say("You have been reset! Please use `>start` again.")
                return
            elif answer1 == "n" or answer1 == "N" or answer1 == "no" or answer1 == "No":
                await self.bot.say("Ok then")
                return

        await self.bot.say("Hello {}".format(user.name))
        await asyncio.sleep(2)
        await self.bot.say("Welcome to War of Crown RPG!\n\nMay i ask what race you are?\n`Choose one`\nOrc\nHuman\nTenti")

        answer1 = await self.check_answer(ctx, ["orc", "human", "tenti", ">start"])

        if answer1 == ">start":
            pass
        elif answer1 == "orc" or answer1 == "Orc":
            userinfo["race"] = "Orc"
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
        elif answer1 == "human" or answer1 == "Human":
            userinfo["race"] = "Human"
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
        elif answer1 == "tenti" or answer1 == "Tenti":
            userinfo["race"] = "Tenti"
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)

        await self.bot.reply("Great!\nWhat Class are you?\n`Choose one`\nRanged\nDPS\nMage\nAssassin")

        answer2 = await self.check_answer(ctx, ["ranged", "dps", "mage", "assassin", ">start"])

        if answer2 == ">start":
            return

        elif answer2 == "ranged" or answer2 == "Ranged":
            userinfo["class"] = "Ranged"
            userinfo["skills_learned"].append("Shoot")
            userinfo["equip"] = "Simple Bow"
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            await self.bot.say("Great, enjoy your stay!")
            return
        elif answer2 == "dps" or answer2 == "DPS":
            userinfo["class"] = "DPS"
            userinfo["skills_learned"].append("Swing")
            userinfo["equip"] = "Simple Sword"
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            await self.bot.say("Great, enjoy your stay!")
            return
        elif answer2 == "mage" or answer2 == "Mage":
            userinfo["class"] = "Mage"
            userinfo["skills_learned"].append("Cast")
            userinfo["equip"] = "Simple Staff"
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            await self.bot.say("Great, enjoy your stay!")
            return
        elif answer2 == "assassin" or answer2 == "Assassin":
            userinfo["class"] = "Assassin"
            userinfo["skills_learned"].append("Stab")
            userinfo["equip"] = "Simple Dagger"
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            await self.bot.say("Great, enjoy your stay!")
            return

    @commands.command(pass_context = True)
    async def fight(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return

        if userinfo["health"] <= 0:
            await self.bot.reply("You cannot fight with 0 HP")
            return

        if userinfo["location"] == "Golden Temple":
            monsterlist = ["Rachi", "Debin", "Oofer"]
        elif userinfo["location"] == "The Forest":
            monsterlist = ["Wolf", "Goblin", "Zombie"]
        elif userinfo["location"] == "Saker Keep":
            monsterlist = ["Draugr", "Stalker", "Souleater"]

        #IF PLAYER ISNT FIGHTING AN ENEMY, CHOOSE ONE BASED ON LOCATION
        if userinfo["selected_enemy"] == "None":
            debi = random.choice((monsterlist))
            userinfo["selected_enemy"] = debi
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)

            if userinfo["selected_enemy"] == "Rachi" or userinfo["selected_enemy"] == "Draugr":
                userinfo["enemyhp"] = random.randint(50, 75)
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            elif userinfo["selected_enemy"] == "Debin" or userinfo["selected_enemy"] == "Stalker":
                userinfo["enemyhp"] = random.randint(50, 100)
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            elif userinfo["selected_enemy"] == "Oofer" or userinfo["selected_enemy"] == "Souleater":
                userinfo["enemyhp"] = random.randint(75, 125)
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)    
            elif userinfo["selected_enemy"] == "Wolf":
                userinfo["enemyhp"] = random.randint(150, 200)
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo) 
            elif userinfo["selected_enemy"] == "Goblin":
                userinfo["enemyhp"] = random.randint(125, 150)
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)  
            elif userinfo["selected_enemy"] == "Zombie":
                userinfo["enemyhp"] = random.randint(175, 225)
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            
        #YOUR DAMAGE BASED ON THE WEAPON YOUR HOLDING
        youdmg = 0
        if userinfo["equip"] == "Simple Dagger":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Simple Staff":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Simple Bow":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Simple Sword":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Sprine Dagger":
            youdmg += random.randint(10, 60)
        elif userinfo["equip"] == "Sprine Staff":
            youdmg += random.randint(10, 60)
        elif userinfo["equip"] == "Sprine Bow":
            youdmg += random.randint(10, 60)
        elif userinfo["equip"] == "Sprine Sword":
            youdmg += random.randint(10, 60)

        #ENEMY DAMAGE BASED ON ENEMY GROUPS
        enemydmg = 0

        if userinfo["selected_enemy"] == "Rachi" or userinfo["selected_enemy"] == "Draugr":
            enemydmg += random.randint(0, 10)
            enemygold = random.randint(25, 40)
            goldlost = random.randint(0, 60)
            xpgain = random.randint(5, 10)
        elif userinfo["selected_enemy"] == "Debin" or userinfo["selected_enemy"] == "Stalker":
            enemydmg += random.randint(0, 20)
            enemygold = random.randint(25, 50)
            goldlost = random.randint(0, 70)
            xpgain = random.randint(5, 20)
        elif userinfo["selected_enemy"] == "Oofer" or userinfo["selected_enemy"] == "Souleater":
            enemydmg += random.randint(0, 30)
            enemygold = random.randint(35, 70)
            goldlost = random.randint(0, 80)
            xpgain = random.randint(10, 25)
        elif userinfo["selected_enemy"] == "Wolf":
            enemydmg += random.randint(10, 40)
            enemygold = random.randint(40, 90)
            goldlost = random.randint(0, 160)
            xpgain = random.randint(10, 30)
        elif userinfo["selected_enemy"] == "Goblin":
            enemydmg += random.randint(10, 60)
            enemygold = random.randint(40, 140)
            goldlost = random.randint(0, 160)
            xpgain = random.randint(10, 30)
        elif userinfo["selected_enemy"] == "Zombie":
            enemydmg += random.randint(10, 40)
            enemygold = random.randint(40, 90)
            goldlost = random.randint(0, 160)
            xpgain = random.randint(10, 30)

        #YOUR SKILL OPTIONS LIST
        show_list = []
        options = [">fight"]
        if "Swing" in userinfo["skills_learned"]:
            options.append("swing")
            options.append("Swing")
            show_list.append("Swing")
        elif "Stab" in userinfo["skills_learned"]:
            options.append("stab")
            options.append("Stab")
            show_list.append("Stab")
        elif "Shoot" in userinfo["skills_learned"]:
            options.append("shoot")
            options.append("Shoot")
            show_list.append("Shoot")
        elif "Cast" in userinfo["skills_learned"]:
            options.append("cast")
            options.append("Cast")
            show_list.append("Cast")
        #IF FOR WHATEVER REASON THE USER DOES >fight AGAIN, RETURN
        em = discord.Embed(description="<@{}> ```diff\n+ What skill would you like to use?\n\n- Choose one\n+ {}```".format(user.id, "\n+".join(show_list)), color=discord.Color.blue())
 
			
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["fight_block"])

        if delta >= 6.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `/start`")
                return
            if userinfo["class"] == "Ranged":
                answer2 = "Shoot"
            if userinfo["class"] == "Assassin":
                answer2 = "Stab"
            if userinfo["class"] == "Mage":
                answer2 = "Cast"
            if userinfo["class"] == "DPS":
                answer2 = "Swing"
        #DEFINE WHAT SKILL WE SELECTED
            if answer2 == "cast" or answer2 == "Cast":
                move = "Cast"
            elif answer2 == "shoot" or answer2 == "Shoot":
                move = "Shoot"
            elif answer2 == "swing" or answer2 == "Swing":
                move = "Swing"
            elif answer2 == "stab" or answer2 == "Stab":
                move = "Stab"
                
            #LETS DEFINE OUR VAR'S
            userhealth = userinfo["health"]
            userhealth1 = userhealth
            userhealth = userhealth - enemydmg
            userlvl = userinfo["lvl"]
            lvlexp = 100 * userlvl

            #LETS DEFINE THE ENEMY'S VAR'S
            enemyhp = userinfo["enemyhp"]
            enemyhp1 = enemyhp
            enemyhp = enemyhp - youdmg
            lootbag = random.randint(1, 10)
            #IF SELECTED A SKILL, FIGHT
            
            if answer2 in options:
                if enemydmg < 0:
                    enemydmg = 0
                if userhealth < 0:
                    userhealth = 0
                if enemyhp < 0:
                    enemyhp = 0
                em = discord.Embed(description="```diff\n- {} has {} HP\n+ {} has {} HP\n\n- {} hits {} for {} damage\n+ {} uses {} and hits for {} damage\n\n- {} has {} HP left\n+ {} has {} Hp left```".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Color.red())
                userinfo["health"] = userhealth
                userinfo["enemyhp"] = enemyhp

                if enemyhp <= 0 and userhealth <= 0:
                    em = discord.Embed(description="```diff\n- {} has killed you\n- {} lost {} gold.```".format(userinfo["selected_enemy"], userinfo["name"], goldlost), color=discord.Color.red())
                    userinfo["gold"] = userinfo["gold"] - goldlost
                    if userinfo["gold"] < 0:
                        userinfo["gold"] = 0
                    if userinfo["health"] < 0:
                        userinfo["health"] = 0
                    userinfo["health"] = 0
                    userinfo["selected_enemy"] = "None"
                    userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
                    userinfo["deaths"] = userinfo["deaths"] + 1
                    fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)

                elif userhealth <= 0:
                    em = discord.Embed(description="```diff\n- {} killed {}\n- {} lost {} gold```".format(userinfo["selected_enemy"], userinfo["name"], userinfo["name"], goldlost), color=discord.Color.red())
                    userinfo["gold"] = userinfo["gold"] - goldlost
                    if userinfo["gold"] < 0:
                        userinfo["gold"] = 0
                    if userinfo["health"] < 0:
                        userinfo["health"] = 0
                    userinfo["selected_enemy"] = "None"
                    userinfo["deaths"] = userinfo["deaths"] + 1
                    fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)

                elif enemyhp <= 0:
                    em = discord.Embed(description="```diff\n+ {} killed the {}\n+ {} gained {} Gold\n+ {} gained {} Exp```".format(userinfo["name"], userinfo["selected_enemy"], userinfo["name"], enemygold, userinfo["name"], xpgain), color=discord.Color.blue())
                    userinfo["selected_enemy"] = "None"
                    userinfo["gold"] = userinfo["gold"] + enemygold
                    userinfo["exp"] = userinfo["exp"] + xpgain
                    print(lootbag)
                    if lootbag == 6:
                        em = discord.Embed(description="```diff\n+ {} Obtained a Lootbag!```".format(userinfo["name"]), color=discord.Color.blue())
                        await self.bot.say(embed=em)
                        userinfo["lootbag"] = userinfo["lootbag"] + 1
                        fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
                    userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
                    fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)

                if userinfo["exp"] >= lvlexp:
                    em = discord.Embed(description="```diff\n+ {} gained a level!```".format(userinfo["name"]), color=discord.Color.blue())
                    userinfo["lvl"] = userinfo["lvl"] + 1
                    userinfo["health"] = 100
                    fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            
            
            userinfo["fight_block"] = curr_time
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            await self.bot.say(embed=em)
        else:
            # calulate time left
            seconds = 6 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You cannot fight yet!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)
			




    @commands.command(pass_context=True)
    async def lootbag(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        if userinfo["lootbag"] == 0:
            em = discord.Embed(description="```diff\n- You don't have any Lootbags!```", color=discord.Color.blue())
            await self.bot.say(embed=em)
            return
        else:
            em = discord.Embed(description="```diff\n+ {} Starts opening a Lootbag. . .```".format(userinfo["name"]), color=discord.Color.blue())
            await self.bot.say(embed=em)
            await asyncio.sleep(5)
            chance = random.randint(1, 3)
            goldmul = random.randint(10, 30)
            goldgain = goldmul * userinfo["lvl"]
            if chance == 3:
                em = discord.Embed(description="```diff\n+ The Lootbag obtained {} Gold!```".format(goldgain), color=discord.Color.blue())
                await self.bot.say(embed=em)
                userinfo["gold"] = userinfo["gold"] + goldgain
                userinfo["lootbag"] = userinfo["lootbag"] - 1
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            else:
                em = discord.Embed(description="```diff\n- The Lootbag didn't contain anything!```", color=discord.Color.blue())
                await self.bot.say(embed=em)
                userinfo["lootbag"] = userinfo["lootbag"] - 1
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)

    @commands.command (pass_context = True)
    async def travel(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        options = []
        options2 = []
        travel_location = []

        if userinfo["lvl"] > 0:
            options.append("(0) Golden Temple")
            options2.append("0")

            options.append("(1) Saker Keep")
            options2.append("1")

        if userinfo["lvl"] >= 10:
            options.append("(2) The Forest")
            options2.append("2")

        em = discord.Embed(description="<@{}>\n```diff\n+ Where would you like to travel?\n- Type a location number in the chat.\n+ {}```".format(user.id, "\n+ ".join(options)), color=discord.Color.blue())
        await self.bot.say(embed=em)

        answer1 = await self.check_answer(ctx, options2)

        if answer1 == "0":
            if userinfo["location"] == "Golden Temple":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(user.id, userinfo["location"]), color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            else:
                location_name = "Golden Temple"
                userinfo["location"] = "Golden Temple"

        elif answer1 == "1":
            if userinfo["location"] == "Saker Keep":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(user.id, userinfo["location"]), color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            else:
                location_name = "Saker Keep"
                userinfo["location"] = "Saker Keep"

        elif answer1 == "2":
            if userinfo["location"] == "The Forest":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(user.id, userinfo["location"]), color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            else:
                location_name = "The Forest"
                userinfo["location"] = "The Forest"

        em = discord.Embed(description="<@{}>\n```diff\n+ Traveling to {}...```".format(user.id, location_name), color=discord.Color.red())
        await self.bot.say(embed=em)
        await asyncio.sleep(3)
        userinfo["location"] = location_name
        fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
        await self.bot.say("You have arrived at {}".format(location_name))
        em = discord.Embed(description="<@{}>\n```diff\n+ You have arrived at {}```".format(user.id, location_name), color=discord.Color.red())
        await self.bot.say(embed=em)

    @commands.command(pass_context = True)
    async def inv(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        em = discord.Embed(description="```diff\n!======== [{}'s Inventory] ========!\n\n!==== [Supplies] ====!\n+ Gold : {}\n+ Wood : {}\n+ Stone : {}\n+ Metal : {}\n\n!===== [Items] =====!\n+ Keys : {}\n+ Loot Bags : {}\n+ Minor HP Potions : {}\n+ {}```".format(userinfo["name"], userinfo["gold"], userinfo["wood"], userinfo["stone"], userinfo["metal"], userinfo["keys"], userinfo["lootbag"], userinfo["hp_potions"], "\n+ ".join(userinfo["inventory"])), color=discord.Color.blue())
        await self.bot.say(embed=em)

    @commands.command(pass_context = True)
    async def stats(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        maxexp = 100 * userinfo["lvl"]
        em = discord.Embed(description="```diff\n!======== [{}'s Stats] ========!\n+ Name : {}\n+ Title : {}\n+ Race : {}\n+ Class : {}\n\n+ Level : {} | Exp : ({}/{})\n+ Health : ({}/100)\n+ Stamina : {}\n+ Mana : {}\n\n!===== [Equipment] =====!\n+ Weapon : {}\n+ Wearing : {}\n\n+ Killed : {} Enemies\n+ Died : {} Times```".format(userinfo["name"], userinfo["name"], userinfo["title"], userinfo["race"], userinfo["class"], userinfo["lvl"], userinfo["exp"], maxexp, userinfo["health"], userinfo["stamina"], userinfo["mana"], userinfo["equip"], userinfo["wearing"], userinfo["enemieskilled"], userinfo["deaths"]), color=discord.Color.blue())
        await self.bot.say(embed=em)

    @commands.command(pass_context = True)
    async def equip(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        choices = []
        inv_list = [i for i in userinfo["inventory"]]
        if len(inv_list) == 0:
            em = discord.Embed(description="```diff\n- You don't have anything else to equip!```", color=discord.Color.red())
            await self.bot.say(embed=em)
        else:
            choices.append(inv_list)
            em = discord.Embed(description="```diff\n+ What would you like to equip?\n- Note this is Uppercase and Lowercase sensitive.\n{}```".format("\n".join(inv_list)), color=discord.Color.blue())
            await self.bot.say(embed=em)
            answer1 = await self.check_answer(ctx, inv_list)
            await self.bot.say("You equiped the {}!".format(answer1))
            em = discord.Embed(description="```diff\n+ You equip the {}!```".format(answer1), color=discord.Color.blue())
            await self.bot.say(embed=em)
            userinfo["inventory"].append(userinfo["equip"])
            userinfo["equip"] = "None"
            userinfo["equip"] = answer1
            userinfo["inventory"].remove(answer1)
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)

    @commands.group(pass_context = True)
    async def buy(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        weapons_list = ["hp","Hp", "Sprine sword", "sprine sword", "Sprine bow", "sprine bow", "Sprine dagger", "sprine dagger", "Sprine staff", "sprine staff"]
        if ctx.invoked_subcommand is None:
            em = discord.Embed(description="```>buy item_name\n\nNote: It must all be lowercase.```", color=discord.Color.blue())
            await self.bot.say(embed=em)

    @buy.command(pass_context=True)
    async def hp(self, ctx, *, ammount : int):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        Sum = ammount * 30

        if ammount == None:
            ammount = 1

        if userinfo["gold"] < Sum:
            needed = Sum - userinfo["gold"]
            em = discord.Embed(description="```diff\n- You need {} more gold for {} potion(s)```".format(needed, ammount), color=discord.Color.red())
            await self.bot.say(embed=em)
        else:   
            userinfo["gold"] = userinfo["gold"] - Sum
            userinfo["hp_potions"] = userinfo["hp_potions"] + int(ammount)
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You bought {} potion(s) for {} Gold```".format(ammount, Sum), color=discord.Color.blue())
            await self.bot.say(embed=em)

    @buy.command(pass_context=True)
    async def item(self, ctx, *, item):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if item == "sprine sword":
            if not userinfo["class"] == "DPS":
                em = discord.Embed(description="```diff\n- You need to be a DPS to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Sprine Sword")
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)

        elif item == "sprine dagger":
            if not userinfo["class"] == "Assassin":
                em = discord.Embed(description="```diff\n- You need to be a Assassin to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Sprine Dagger")
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)

        elif item == "sprine bow":
            if not userinfo["class"] == "Ranged":
                em = discord.Embed(description="```diff\n- You need to be an Ranged to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Sprine Bow")
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)

        elif item == "sprine staff":
            if not userinfo["class"] == "Mage":
                em = discord.Embed(description="```diff\n- You need to be a Mage to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Sprine Staff")
                fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="```diff\n- You have requested to buy an invalid item.\n\n+ To see the list of the items, type >items```", color=discord.Color.red())
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def items(self, ctx, *, Class):
        user = ctx.message.author
        if Class == "Mage" or Class == "mage":
            em = discord.Embed(description="```diff\n+ Item list for the Mage Class.```\n\n1) Sprine Staff - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        elif Class == "DPS" or Class == "dps":
            em = discord.Embed(description="```diff\n+ Item list for the DPS Class.```\n\n1) Sprine Sword - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        elif Class == "Assassin" or Class == "assassin":
            em = discord.Embed(description="```diff\n+ Item list for the Assassin Class.```\n\n1) Sprine Dagger - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        elif Class == "Ranged" or Class == "ranged":
            em = discord.Embed(description="```diff\n+ Item list for the Ranged Class.```\n\n1) Sprine Bow - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="```diff\n- That is not a valid Class.```", color=discord.Color.red())
            await self.bot.say(embed=em)

    @commands.command(pass_context = True)
    async def heal(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        if userinfo["hp_potions"] > 0:
            gain = random.randint(40, 50)
            userinfo["health"] = userinfo["health"] + gain
            if userinfo["health"] > 100:
                userinfo["health"] = 100
            userinfo["hp_potions"] = userinfo["hp_potions"] - 1
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n- You use a Minor Health Potion\n+ {} HP```".format(gain), color=discord.Color.red())
            await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="```diff\n- You don't have any health potions!```", color=discord.Color.red())
            await self.bot.say(embed=em)


    @commands.command(pass_context=True)
    async def daily(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        goldget = random.randint(500, 1000)
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["daily_block"])

        if delta >= 86400.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `>start`")
                return
            userinfo["gold"] += goldget
            userinfo["daily_block"] = curr_time
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You recieved your daily gold!\n+ {}```".format(goldget), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calulate time left
            seconds = 86400 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You can't claim your daily reward yet!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def rest(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        HPget = random.randint(10, 30)
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["rest_block"])

        if delta >= 120.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `>start`")
                return
            userinfo["health"] = userinfo["health"] + HPget
            if userinfo["health"] > 100:
                userinfo["health"] = 100
            userinfo["rest_block"] = curr_time
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You gained {} HP for resting!```".format(HPget), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calulate time left
            seconds = 120 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You're not tired!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def mine(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        mined_metal = random.randint(1, 10)
        mined_rock = random.randint(1, 10)
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["mine_block"])

        if delta >= 600.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `/start`")
                return
            userinfo["metal"] = userinfo["metal"] + mined_metal
            userinfo["stone"] = userinfo["stone"] + mined_rock
            userinfo["mine_block"] = curr_time
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You mined a Rock!\n+ {} Metal\n+ {} Stone```".format(mined_metal, mined_rock), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calulate time left
            seconds = 600 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You cannot mine yet!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def chop(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        chopped = random.randint(1, 10)
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `>start`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["chop_block"])

        if delta >= 600.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `/start`")
                return
            userinfo["wood"] = userinfo["wood"] + chopped
            userinfo["chop_block"] = curr_time
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You chopped a Tree!\n+ {} Wood```".format(chopped), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calulate time left
            seconds = 600 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You cannot chop yet!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)


    def _name(self, user, max_length):
        if user.name == user.display_name:
            return user.name
        else:
            return "{} ({})".format(user.name, self._truncate_text(user.display_name, max_length - len(user.name) - 3), max_length)

    async def on_message(self, message):
        await self._handle_on_message(message)

    async def _handle_on_message(self, message):
        text = message.content
        channel = message.channel
        server = message.server
        user = message.author
        # creates user if doesn't exist, bots are not logged.
        await self._create_user(user, server)
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")

    # handles user creation.
    async def _create_user(self, user, server):
        if not os.path.exists("data/alcher/players/{}".format(user.id)):
            os.makedirs("data/alcher/players/{}".format(user.id))
            new_account = {
                "name": user.name,
                "race": "None",
                "class": "None",
                "health": 100,
                "enemyhp": 50,
                "enemylvl": 0,
                "lvl": 0,
                "gold": 0,
                "wood": 0,
                "metal": 0,
                "stone": 0,
                "enemieskilled": 0,
                "selected_enemy": "None",
                "deaths": 0,
                "exp": 0,
                "lootbag": 0,
                "wearing": "None",
                "defence": 0,
                "guild": "None",
                "inguild": "None",
                "skills_learned": [],
                "inventory" : [],
                "equip": "None",
                "title": "None",
                "wincry": "None",
                "losecry": "None",
                "location": "Golden Temple",
                "roaming": "False",
                "pet": "None",
                "mana": 100,
                "stamina": 100,
                "craftable": [],
                "daily_block": 0,
                "rest_block": 0,
                "fight_block": 0,
                "traveling_block": 0,
                "hp_potions": 0,
                "keys": 0,
                "mine_block": 0,
                "chop_block": 0,
                "in_dungeon": "False",
                "dungeon_enemy": "None",
                "duneon_enemy_hp": 0,
                "in_party": []
            }
            fileIO("data/alcher/players/{}/info.json".format(user.id), "save", new_account)
        userinfo = fileIO("data/alcher/players/{}/info.json".format(user.id), "load")

def check_folders():
    if not os.path.exists("data/alcher"):
        print("Creating data/alcher folder...")
        os.makedirs("data/alcher")

    if not os.path.exists("data/alcher/players"):
        print("Creating data/alcher/players folder...")
        os.makedirs("data/alcher/players")
        transfer_info()

def transfer_info():
    players = fileIO("data/alcher/players.json", "load")
    for user_id in players:
        os.makedirs("data/alcher/players/{}".format(user_id))
        # create info.json
        f = "data/alcher/players/{}/info.json".format(user_id)
        if not fileIO(f, "check"):
            fileIO(f, "save", players[user_id])

def setup(bot):
    check_folders()

    n = WarOfCrownRPG(bot)
    bot.add_listener(n.on_message,"on_message")
    bot.add_cog(n)
