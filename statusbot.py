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
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.channel.send('hai')


@bot.event
async def on_presence_update(before, after):
    print('event fired: '+before.name)
    statusText = 'NULL'
    with open('userlist.txt') as z:
        if str(before.id) in z.read():
            filename = str(after.id) + '.txt'
            with open(filename, 'a', encoding='utf-8') as f:
                for s in after.activities:
                    if isinstance(s, discord.CustomActivity):
                        #await after.channel.send(s)
                        statusText = str(s.state)
                timestamp = datetime.datetime.now().date()
                if statusText != 'NULL':
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
                x = line.split(' 🏆 ')
                biglist = biglist + (x[0].strip() + ' (' + x[1].strip() + ')\n')
                #await ctx.channel.send(x[0].strip()+' ('+x[1].strip()+')')
            await ctx.channel.send(biglist)
        f.close()
    except:
        await ctx.channel.send('No list found :(')


@bot.command()  ## display a random status from your list
async def rand(ctx):
    seed(None)
    filename = str(ctx.author.id) + '.txt'

    try:
        with open(filename, 'r', encoding='utf-8') as f:
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
            await ctx.message.add_reaction("🤖")
            await ctx.message.add_reaction("❌")




@bot.event  ##CAREFUL WITH THIS ONE
async def on_message(message):
    await bot.process_commands(message)
    await react(message)


async def react(message):
    if message.content == "swag":
        #await message.add_reaction("🤖")
        await message.add_reaction("👍")






#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#
#    if message.content.startswith('$hello'):
#        id = message.author.id
#        await message.channel.send("Your status is: " + str(discord.CustomActivity))
#        await message.channel.send(':robot:')

#await message.channel.send('Hello!')

bot.run(TOKEN)
