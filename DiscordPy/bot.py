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

def get3Digits(num, digits):
    numString = str(num)
    digitString = ''
    i = 0
    while i < digits:
        digitString = digitString + numString[i]
        if(numString[i] == '.'):
            digits = digits + 1
        i = i + 1
    return digitString

def convertNum(num):
    if((float(num)/1000000) < 999 and (float(num)/1000000) > 1):
        digits = (float(num)/1000000)
        val = get3Digits(digits, 3) + 'M'
    elif((float(num)/1000000000) < 999 and (float(num)/1000000000) > 1):
        digits = (float(num) / 1000000000)
        val = get3Digits(digits, 3) + 'B'
    elif((float(num)/1000000000000) < 999 and (float(num)/1000000000000) > 1):
        digits = (float(num) / 1000000000000)
        val = get3Digits(digits, 3) + 'T'
    else:
        return num
    return val


@bot.command(name = 'stonk')
async def getTickerData(ctx, *arg):
    try:
        stock = yf.Ticker(arg[0])
        data = stock.info['ask']
        if (len(arg) == 1):
            await ctx.send(data)
        else:
            response = convertNum(stock.info.get(arg[1]))
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