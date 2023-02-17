import json
import requests
import discord
from discord.ext import tasks

client = discord.Client()

with open('config.json') as config:
    configdata = json.load(config)
userIds = configdata['userIds']
message = configdata['message']
channelId = configdata['channelId']

@tasks.loop(minutes=3)
async def test():
    channel = client.get_channel(channelId)
    #await channel.send("test")
    url = 'https://presence.roblox.com/v1/presence/users'
    usrID = { "userIds": userIds }
    print(usrID)
    x = requests.post(url, json = usrID)
    y = x.json()
    print("\u001b[0m")
    print(y)
    for i in range(len(y["userPresences"])):
        z = y["userPresences"][i]
        if z["userPresenceType"] == 1:
            print("\u001b[93mOnline")
        elif z["userPresenceType"] == 2:
            a = requests.get('https://users.roblox.com/v1/users/' + str(userIds[i])).json()['name']
            await channel.send(a + message + "https://web.roblox.com/users/" + str(userIds[i]) + "/profile")
            print("\u001b[92mIngame")
        else:
            print("\u001b[31mFail")
@client.event
async def on_ready():
    print('Firewatch V2.1 by Bombshell2#8591 has loaded.')
    test.start()

client.run('OTk0MzYxNjI0NTQwNDc5NjY4.GUk4_Q.c21eFiAzCvFlyNW7Ttjjj6oZUxEyrwfUGCq38c')
