# bot.py
import os
import random
import yfinance as yf
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.command(name = 'stonk')
async def nine_nine(ctx, *arg):
    try:
        stock = yf.Ticker(arg[0])
        data = stock.info['ask']
        if (len(arg) == 1):
            await ctx.send(data)
        else:
            response = stock.info.get(arg[1])
            await ctx.send(response)
    except IndexError:
        data = 'null'
        response = "I can't find your ticker. Sorry :( "
        await ctx.send(response)
bot.run(TOKEN)