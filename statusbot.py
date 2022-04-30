import discord
from discord.ext import commands, tasks
#from datetime import datetime, date, time, timezone
import datetime
from random import seed
from random import randint

#code to hide my token
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("TOKEN")
#end of .env code

intents = discord.Intents().all()
intents.members = True
intents.presences = True
intents.messages = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.channel.send('hello!')


@bot.event
async def on_presence_update(before, after):
    print('event fired: '+before.name)
    statusText = None

    with open('userlist.txt') as z: #checking to see if this user has opted-in
        if str(before.id) in z.read():
            filename = str(after.id) + '.txt'
            with open(filename, 'a', encoding='utf-8') as f: # recording the status message
                for s in after.activities:
                    if isinstance(s, discord.CustomActivity): # iterate through activities, look for CustomActivity
                        statusText = str(s.name)              # copy down status text
                        #await after.channel.send(s)

                        if statusText != 'None': #if status isn't empty, check for emoji attribute
                            if s.emoji is not None:
                                if s.emoji.is_unicode_emoji() == True:
                                    statusText = str(s.emoji) + ' ' + statusText #append emoji if it's unicode valid
                        else: #if status is empty, set it to None
                            statusText = None

                timestamp = datetime.datetime.now().date()
                if statusText != None:
                    if await checkforduplicate(filename, statusText) <= 0:
                        f.write(statusText + ' \u0001🏆\u0001 ' + str(timestamp) + '\n')
                    #await after.channel.send(timestamp)
                #else:
                #await after.channel.send('no status')
            f.close()
        else:
            print('UID not found in userlist.txt')

@bot.command()  ## display entire list
async def list(ctx):
    filename = str(ctx.author.id) + '.txt'
    biglist = ''
    print(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                x = line.split(' 🏆 ') #funky text delimiter because processing user input
                biglist = biglist + (x[0].strip() + ' (' + x[1].strip() + ')\n')
                #await ctx.channel.send(x[0].strip()+' ('+x[1].strip()+')')
            await ctx.channel.send(biglist)
        f.close()
    except:
        await ctx.channel.send('No list found :(')


@bot.command()  ## display a random status from your list
async def rand(ctx):
    seed(None) #generate seed based off of our clock
    filename = str(ctx.author.id) + '.txt' #get filename from user's UID

    try:
        with open(filename, 'r', encoding='utf-8') as f: #open user's respective file
            lines = f.readlines()
            target = randint(0, len(lines) - 1)
            print(len(lines))
            chosen = lines[target]
            chosenList = chosen.split(' 🏆 ')
            await ctx.channel.send(chosenList[0].strip() + ' (' + chosenList[1].strip() + ')')
        f.close()
    except:
        await ctx.channel.send('No list found :(')


async def checkforduplicate(filename, string):
    answerkey = 0
    print(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as q:
            lines = q.readlines()
            for line in lines:
                editedLine = line.split(' 🏆 ')
                print(editedLine[0] + ' vs ' + string)
                if editedLine[0].strip() == string.strip():
                    answerkey = 1
        q.close()
        print('answerkey = ' + str(answerkey))
        return answerkey
    except:
        print('file not found\n')
        answerkey = -1
        print('answerkey = ' + str(answerkey))
    return answerkey


@bot.command()  ## opt-in to have your status messages recorded
async def record(ctx):

    goahead = 0 #tracker variable

    with open('userlist.txt', 'r', encoding='utf-8') as q:
        if (str(ctx.author.id) in q.read()):
            await ctx.message.reply("You've already opted-in!")
        else:
            goahead = 1

    if(goahead == 1):
        try:
            with open('userlist.txt', 'a', encoding='utf-8') as f:
                f.write(str(ctx.author.id)+'\n')
                f.close()
                await ctx.message.add_reaction("🤖")
                await ctx.message.add_reaction("👍")
        except:
            print('unable to add '+ctx.author.display_name+' to userlist\n')
            ctx.message.reply('Something went wrong, please contact the bot\'s creator!')
            await ctx.message.add_reaction("🤖")
            await ctx.message.add_reaction("❌")




@bot.event  ##CAREFUL WITH THIS ONE
async def on_message(message):
    await bot.process_commands(message)
    await react(message)


async def react(message):
    if message.content == "test":
        if message.author.activities[0].emoji is not None:
            if message.author.activities[0].emoji.is_unicode_emoji() == True:
                await message.reply('your status is: '+ str(message.author.activities[0].emoji))
            else:
                await message.reply('your emoji is not available')
        else:
            await message.reply("You have no emoji!")
        #await message.add_reaction("🤖")
        #await message.add_reaction("👍")
    elif message.content == "statuscheck":
        await message.reply('your status is: ' + str(message.author.activities[0].name))
        if message.author.activities[0].name == None:
            await message.reply("Empty status")


bot.run(TOKEN)