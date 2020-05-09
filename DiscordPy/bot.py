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
    if(len(arg) == 1):
        stock = yf.Ticker(arg[0])
        response = stock.info.get("ask")
        await ctx.send(response)
    else:
        stock = yf.Ticker(arg[0])
        response = stock.info.get(arg[1])
        await ctx.send(response)
bot.run(TOKEN)