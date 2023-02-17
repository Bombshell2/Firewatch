import discord
from discord.ext import tasks
import requests
import json

with open("config.json") as configfile:
    config = json.load(configfile)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
sendEmbed = True

#create request json
ids = []
userIdsJson = {}
for i in config['userIds']:
    ids.append(i[0])
userIdOnline = []
for i in range(len(ids)):
    userIdOnline.append([ids[i], False])
userIdsJson["userIds"] = ids
cookie = config['userIds']

#welcome to my mind
def search():
    global sendEmbed, userIdOnline
    embedVar = discord.Embed(title=config['onlineTitle'], description=config['description'], color=config['color'])
    data = requests.post('https://presence.roblox.com/v1/presence/users', json=userIdsJson).json()['userPresences']
    #synced is for cookie array
    synced = -1
    for i in data:
        synced += 1
        gamevalue = ""
        if i['userPresenceType'] == 2:
            #if user is playing game, mark user as playing a game
            userIdOnline[synced][1] = False
            #if there is no roblosecurity token associated, say user is playing unknown game
            if config['userIds'][synced][1] == "":
                gamevalue = "Playing unknown game."
            else:
                #wow! new feature begins here! get users online friends, then if matches id generate quick server join link.
                req = requests.get(
                    url="https://friends.roblox.com/v1/users/" + cookie[synced][2] + "/friends/online",
                    cookies={
                        ".ROBLOSECURITY": cookie[synced][1]
                    }
                )
                work = req.json()['data']
                for i in work:
                    if i['id'] == cookie[synced][0]:
                        gamevalue = "https://www.roblox.com/games/" + str(i['userPresence']['placeId']) + "/?serverJobId=" + i['userPresence']['gameInstanceId']
            embedVar.add_field(name=requests.get(url="https://users.roblox.com/v1/users/" + str(cookie[synced][0])).json()["name"], value=gamevalue, inline=True)
        else:
            #if user isnt playing a game, mark as offline.
            userIdOnline[synced][1] = True
    # not sure if need to remove line below, may do later :P
    synced = -1
    return embedVar

#loop for constant checking
@tasks.loop(minutes=config['refreshTime'])
async def main():
    global sendEmbed
    channel = client.get_channel(config['channelId'])
    prevtitle = [embed async for embed in channel.history(limit=1)][0].embeds[0].title
    newembed = discord.Embed(title=config['offlineTitle'], color=0x336EFF)
    embedVar = search()
    #count how many players are offline. if all of them are offline, move on to next step
    offlinecount = 0
    for i in range(len(userIdOnline)):
        if userIdOnline[i][1]:
            offlinecount += 1
    # if title of previous embed isnt the online title, allow embed to be sent. if it is, update embed. 
    if prevtitle != config['onlineTitle']:
        sendEmbed = True
    else:
        sendEmbed = False
        await [embed async for embed in channel.history(limit=1)][0].edit(embed=embedVar)
    # if all accounts are offline, update embed to be offline.
    if offlinecount == len(userIdOnline):
        await [embed async for embed in channel.history(limit=1)][0].edit(embed=newembed)
    #send embed if allowed, and if all players arn't offline. reset variable that controlls if you can send an embed.
    if sendEmbed and offlinecount != len(userIdOnline):
        sendEmbed = False
        await channel.send(embed=embedVar)

#congrats, you survived my terrible code. most likely will break.
@client.event
async def on_ready():
    print('Firewatch v3.0 By Bombshell2#8591, Logged on as', client.user)
    main.start()

client.run(config['token'])