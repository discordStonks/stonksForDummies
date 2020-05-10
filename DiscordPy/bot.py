# bot.py
import os
import random
import yfinance as yf
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

@bot.command(name = 'stonk')
async def getTickerData(ctx, *arg):
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

@bot.command(name='help')
async def getHelp(ctx, *arg):
    response = "Here are some popular commands you can you use with !stonk TICKER command \n" \
               "'longBusinessSummary', 'website', 'previousClose', 'open', 'dayHigh', 'dayLow', \n" \
               "'marketCap', 'profitMargins', 'shortRatio', 'heldPercentInstitutions', \n" \
               "Go to [Insert Website] to see more commmands. \n"
    await ctx.send(response)

bot.run(TOKEN)