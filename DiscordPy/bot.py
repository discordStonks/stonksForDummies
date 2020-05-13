# bot.py
import os
import random
import yfinance as yf
import praw
import datetime
from discord.ext import commands
from dotenv import load_dotenv

r = praw.Reddit(client_id='Insert-ClientID',
                client_secret='Insert-ClientSecret',
                user_agent='Insert-User-Agent')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

subreddit = r.subreddit('wallstreetbets')
imageList = []
prev_append_meme_time = datetime.datetime.now()
print(prev_append_meme_time)

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

@bot.command(name='meme')
async def getMeme(ctx, *arg):
    global prev_append_meme_time
    global imageList

    current_time = datetime.datetime.now()   #Get the current time and compare with the last time the list got appended
    delta_time = current_time - prev_append_meme_time
    delta_seconds = delta_time.total_seconds()

    if(len(imageList) == 0 or delta_seconds >= 60): #Make a call only if we need to append the list
        new_python = subreddit.new(limit=100)

    if(len(imageList) == 0):    #Get the first 100 post and if they are images add them to the list
        for i in new_python:
            if i.link_flair_text in {"Meme", "Loss", "Gain", "Shitpost"} and i.url[-3:] in {"jpg", "png"}:
                imageList.append(tuple([i.title, i.url]))

    if(delta_seconds >= 60):    #Add new images if it has been 1min since the list has been appended
        for i in new_python:
            if i.link_flair_text in {"Meme", "Loss", "Gain", "Shitpost"} and i.url[-3:] in {"jpg", "png"}:
                redditSubmissionTime = datetime.datetime.fromtimestamp(i.created_utc)
                submissionPrevCallDelta = redditSubmissionTime - prev_append_meme_time
                if(submissionPrevCallDelta.total_seconds() > 0):
                    imageList.append(tuple([i.title, i.url]))
                else:
                    break

    if(delta_seconds >= 60):    #Update the last checked time variable
        prev_append_meme_time = current_time

    val = random.randint(0, len(imageList) - 1)         #Pick a random meme and pop it from the list
    response = imageList.pop(val)
    await ctx.send(response[0] + '\n' + response[1])    #Output with title and image

bot.run(TOKEN)