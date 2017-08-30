from discord.ext import commands
from cogs.utils.dataIO import dataIO
import random


class RecyclingPlant:
    """Apply for a job at the recycling plant!"""
    def __init__(self, bot):
        self.bot = bot
        self.junk = dataIO.load_json('data/recyclingplant/junk.json')
        self.bank = self.bot.get_cog('Economy').bank

    @commands.command(pass_context=True)
    async def recyclingplant(self, context):
        """Apply for a job at the recycling plant!"""
        x = 0
        await self.bot.say('{0} has signed up for a shift at the Recycling Plant! Type ``exit`` to terminate it early.'.format(context.message.author.display_name))
        while x in range(0, 10):
            used = random.choice(self.junk['can'])
            reward = 0
            if used['action'] == 'trash':
                opp = 'recycle'
            else:
                opp = 'trash'
            await self.bot.say('``{}``! Will {} ``trash`` it or ``recycle`` it?'.format(used['object'], context.message.author.display_name))
            answer = await self.bot.wait_for_message(timeout=10,
                                                     author=context.message.author)
            if answer is None:
                await self.bot.say('``{}`` fell down the conveyor belt to be sorted again!'.format(used['object']))
            elif answer.content.lower().strip() == used['action']:
                await self.bot.say('Congratulations! You put ``{}`` down the correct chute! (**+50**)'.format(used['object']))
                reward = reward + 50
                x += 1
            elif answer.content.lower().strip() == opp:
                await self.bot.say('{}, you little brute, you put it down the wrong chute! (**-50**)'.format(context.message.author.display_name))
                reward = reward - 50
            elif answer.content.lower().strip() == 'exit':
                await self.bot.say('{} has been relived of their duty.'.format(context.message.author.display_name))
                break
            else:
                await self.bot.say('``{}`` fell down the conveyor belt to be sorted again!'.format(used['object']))
        else:
            if reward > 0:
                self.bank.deposit_credits(context.message.author, reward)
            await self.bot.say('{} been given **{}$** for your services.'.format(context.message.author.display_name, reward))


def setup(bot):
    bot.add_cog(RecyclingPlant(bot))
