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
