# Firewatch
A discord bot capable of checking user statuses, getting what game a player is in with a .ROBLOSECURITY token, and generating a link to join that game.

## Setup
Run 'py -3 setup.py', then run 'py -3 main.py' after configuring config.json.

## Config
channelId - Discord channel Id. Find by enabling developer mode in settings, and then right clicking the channel and clicking copy ID.

refreshTime - How long between message updates. Measured in minutes.

online/offlineTitle - Title for embed messages of Online users, and all users going offline.

description - Discription of embeds.

color - Color of embed. Stored as the hexedecimal color value, converted to an integer value.

UserIds - 2d array that stores userId, .ROBLOSECURITY token, and userId of the user who has the token. In format of [[userId, ".ROBLOSECURITY", ROBLOSECURITYuserId], [userId2, ".ROBLOSECURITY2", ROBLOSECURITYuserId2]]

token - Discord bot token. Look up how to get this one.

## Quickjoin link

Using the extension Roblox JobID Join 'https://chrome.google.com/webstore/detail/roblox-jobid-join/pdeebkpgdaflejgihpbniammmelkdnac?hl=en-US', you are able to join servers quickly by clicking the generated link in the embed. Only works with Accounts associated with a .ROBLOSECURITY token.
