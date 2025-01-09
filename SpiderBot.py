import discord
from discord.ext import commands
import os
import getpass
import io
import aiohttp
from dotenv import load_dotenv
import random

load_dotenv()

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

TOKEN = os.getenv('DISCORD_KEY')
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if bot.user.id != message.author.id:
        if ':weh:' in message.content.lower():
            await message.channel.send('<:weh:630081507796582410>')
            
        #elif 'hello' in message.content.lower():
        #    await message.channel.send(f'Hello{random.choice(["!","!!","!!!"])}')
    await bot.process_commands(message)

#@bot.event
#async def on_reaction_add(message, reaction):
#    if bot.user.id != message.author.id:
#        if reaction.emoji == '<:pog:571499681637466113>':
#            await message.add_reaction('<:pog:571499681637466113>')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format; also allows modifiers."""
    if '+' in dice:
        dice, mod = dice.split('+')
        mod=int(mod)
    elif '-' in dice:
        dice, mod = dice.split('-')
        mod=int(mod)*-1       
    else:
        mod = 0
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
    if rolls > 20:
        await ctx.send('Please roll less dices! Max is 20 rolls.')
    elif limit >100:
        await ctx.send('Please choose a smaller dice! Max is d100.')
    elif limit <1:
        await ctx.send('Cannot roll less then one dice, chump!')
    else:
        result = [random.randint(1, limit) for r in range(rolls)]
    
    if mod != 0:
        output = (f'You rolled {result}, adding {mod} for a total of: {sum(result)+mod}.')
       
    else:
        output = (f'You rolled {result}, for a total of: {sum(result)}.')
    await ctx.send(output)

@bot.command()
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def coinflip(ctx):
    """Flips a coin."""
    await ctx.send(random.choice(['headaS','tails']))

@bot.command()
async def FtoC(ctx, number: int):
    """Converts Fahreneits to Celsius"""
    celsius = (number-32)*(5/9)
    await ctx.send(int(celsius))

@bot.command()
async def ball(ctx, question: str):
    """Magic 8 Ball."""
    ball_answers = [':green_circle: It is certain',':green_circle: It is decidedly so',':green_circle: Without a doubt',':green_circle: Yes definitely',
                    ':green_circle: You may rely on it',':green_circle: As I see it, yes',':green_circle: Most likely',':green_circle: Outlook good', ':green_circle: Yes',
                    ':green_circle: Signs point to yes',':yellow_circle: Reply hazy, try again',':yellow_circle: Ask again later',':yellow_circle: Better not tell you now',
                    ':yellow_circle: Cannot predict now',':yellow_circle: Concentrate and ask again',':red_circle: Do not count on it', ':red_circle: My reply is no',
                    ':red_circle: My sources say no',':red_circle: Outlook not so good',':red_circle: Very doubtful']
    await ctx.send(random.choice(ball_answers))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    if times > 10:
        await ctx.send('Number must be lower than 10')
    else:
        for i in range(times):
            await ctx.send(content)

@bot.command()
async def frog(ctx):
    '''Ribbit!'''
    await ctx.send('http://www.allaboutfrogs.org/funstuff/random/{0}.jpg'.format(str(random.randrange(1,55)).zfill(4)))

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

@bot.command()
async def pf(ctx):
    """Posts the website that one should use when consulting Pathfinder resources."""
    await ctx.send('Kobold always says to use this website: https://www.aonprd.com/ ...')

@bot.command()
async def credit(ctx):
    """Posts the creator's GitHub page."""
    await ctx.send('```https://github.com/t-revor```')

bot.run(TOKEN)
