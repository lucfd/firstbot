import discord
import json
import datetime


def read_list(filename):

    try:
        with open(filename, 'r') as json_file:
            loaded_data = json.load(json_file)
        return loaded_data
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{filename}': {e}")
        return None

def fetch_status_text(presence):

    for field in presence.activities:
        if isinstance(field, discord.CustomActivity):  # iterate through activities, look for CustomActivity
            statusText = str(field.name)  # copy down status text   
            return statusText

    return None # if nothing is found


def fetch_emoji(presence):
    
    for field in presence.activities:
        if isinstance(field, discord.CustomActivity):

            if field.emoji is not None: # not all status messages have an emoji
                if field.emoji.is_unicode_emoji() == True:
                    emoji = str(field.emoji)
                    return emoji
    
    return None


def emoji_exists(presence):
    
    for field in presence.activities:
        if isinstance(field, discord.CustomActivity):

            if field.emoji is not None:
                if field.emoji.is_unicode_emoji() == True:
                    return True
    
    return False


def read_status(presence):
    
    statusText = fetch_status_text(presence)

    if statusText == None:
        return None

    # emoji handler block
    if emoji_exists(presence):
        emoji = fetch_emoji(presence)
        statusText = emoji + ' ' + statusText

    timestamp = datetime.datetime.now().date()
    statusText = statusText + ' ' + str(timestamp)
    return statusText

        

def save_status(before, after):
    
    filename = 'test.json'


    with open(filename, 'a', encoding='utf-8') as f:  # recording the status message
        for s in after.activities:
            if isinstance(s, discord.CustomActivity):  # iterate through activities, look for CustomActivity
                statusText = str(s.name)  # copy down status text
                # await after.channel.send(s)

                if statusText != 'None':  # if status isn't empty, check for emoji attribute
                    if s.emoji is not None:
                        if s.emoji.is_unicode_emoji() == True:
                            statusText = str(s.emoji) + ' ' + statusText  # append emoji if it's unicode valid
                else:  # if status is empty, set it to None
                    statusText = None

        timestamp = datetime.datetime.now().date()
        if statusText != None:

            data = {
                'message': statusText,
                'timestamp': timestamp
                    }


            json.dump(data, f, indent=2, default=str, separators=(',', ':'))


            # await after.channel.send(timestamp)
        # else:
        # await after.channel.send('no status')
    f.close()
