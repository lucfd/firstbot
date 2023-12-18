import discord
from discord import app_commands
from discord.ext import commands
import datetime
from random import seed
from random import randint
import helpers

class aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False  # prevents syncing more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync()  # put guild=discord.Object(id=) to specify guild
            self.synced = True
        print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)


@client.event
async def on_presence_update(before, after):
    print('event fired: ' + before.name)
    statusText = None
    helpers.save_status(before, after)


@tree.command(name='random', description='Posts a random status from your list')
async def slashrand(interaction: discord.Interaction):
    await rand(interaction)


@tree.command(name='list', description='Displays all of your recorded status messages')
async def slashlist(interaction: discord.Interaction):
    filename = str(interaction.user.id) + '.txt'
    biglist = ''
    print(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                x = line.split(' 🏆 ')
                biglist = biglist + (x[0].strip() + ' (' + x[1].strip() + ')\n')
                # await ctx.channel.send(x[0].strip()+' ('+x[1].strip()+')')
            await interaction.response.send_message(biglist)
        f.close()
    except:
        await interaction.response.send_message('No list found :(')


@tree.command(name='opt-in', description='opt in to have your status messages recorded')
async def record(interaction: discord.Interaction):
    goahead = 0  # tracker variable

    with open('userlist.txt', 'r', encoding='utf-8') as q:
        if (str(interaction.user.id) in q.read()):
            await interaction.response.send_message("You've already opted in!", ephemeral=True)
        else:
            goahead = 1

    if (goahead == 1):
        try:
            with open('userlist.txt', 'a', encoding='utf-8') as f:
                f.write(str(interaction.user.id) + '\n')
                f.close()
                print('Successfully added ' + interaction.user.display_name + ' to userlist\n')
                await interaction.response.send_message(
                    "Success! Your status messages are now being recorded :]", ephemeral=True)
        except:
            print('unable to add ' + interaction.user.display_name + ' to userlist\n')
            await interaction.response.send_message("Something went wrong! Contact the dev for help", ephemeral=True)


async def rand(ctx):
    seed(None)
    filename = str(ctx.user.id) + '.txt'
    print(filename)
    print('hhh')
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            target = randint(0, len(lines) - 1)
            print(len(lines))
            chosen = lines[target]
            chosenList = chosen.split(' 🏆 ')
            await ctx.response.send_message(chosenList[0].strip() + ' (' + chosenList[1].strip() + ')')
        f.close()
    except:
        await ctx.response.send_message("something is broken!", ephemeral=True)


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


client.run(TOKEN)
