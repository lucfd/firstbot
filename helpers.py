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


def is_duplicate(status, filename): # returns True if a status message already exists in a user's list (ignores timestamp)

    status_list = read_list(filename)

    for entry in status_list:

        if(entry["message"] == status):
            return True
        
    return False


def is_opted_in(presence):  # checking to see if this user has opted-in

    try:
        with open('userlist.txt') as file:
            if str(presence.id) in file.read():
                return True
            else:
                return False
    except:
        return False


def save_status(before, after):
    
    filename = str(after.id) + '.json'


    try:
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        print('file not found')
        json_data = []
    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON or is empty.")
        json_data = []


        status_text = read_status(after)

        if status_text != None:

            new_status = {
                'message': status_text,
                'timestamp': datetime.datetime.now().date()
                    }

        json_data.append(new_status)
    
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=2, default=str)