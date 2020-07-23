# Shirim - Eva Twin's last.fm Bot!

A bot designed to output last.fm data. Designed with a non-committal minimalist philosophy.

Much of this bot's frontend is based off of [Amb1tion's Patrician-Bot](https://github.com/Amb1tion/Patrician-Bot), with a new backend and more consistent ways to fetch data.

To **invite** the bot to your server, click [here](https://discordapp.com/api/oauth2/authorize?client_id=659885086707286017&permissions=0&scope=bot).

# General Commands

**set**: sets your last.fm username (__example:__ !set skiffskiffles)

**fm**: fetches your most recent last.fm scrobble. (__example:__ !fm)

**weekly, monthly, 3months, 6months, yearly, alltime**: these commands fetch your top albums in a given timeframe. has optional arguments as well. (__example:__ !weekly 3x3 -nc)

_optional arguments:_ <chart size: 3x3, 4x4, 5x5, 2x6> <-nc> (-nc generates a chart without captions over the album covers)

**recent**: fetches your most recent 10 scrobbles.

**fmyt**: fetches your current scrobble as the first video in a youtube search result. searches may return albums as opposed to tracks, unfortunately.

**yt**: fetch the first result of a youtube search with given search term(s). (__example:__ !yt xtal aphex twin)

**get**: fetches someone else's data. has optional arguments. (__example:__ !get <username/discord mention>)

_optional arguments:_ <chart type (e.g. weekly, monthly)> <chart size> <-nc>, yt, recent, chart, profile (__examples:__ !get evatwin weekly 4x4 -nc, !get evatwin recent)

**taste**: compares your listening habits to another person's. (__example:__ !taste <username/discord mention>)

# Profiles Functionality

This is something currently in beta testing. Currently, the related profiling commands are:

**chart**: Displays a chart you set using the **submit** command. (__example:__ !chart)
  
**submit**: Submit a chart to pull later using the **chart** command. (__example:__ !submit <chart link or username>)

**setrym**: Set your RYM username.

**setspotify**: Set your Spotify username.

**profile**: Displays a profile containing data from your last.fm, and links to your RYM and Spotify, if you've set them.

# Configuration

**set_prefix**: can only be used by the server owner. sets a custom prefix for the server. (__example:__ !set_prefix $)

**set_reactions**: can only be used by the server owner. determines whether up/down reactions are put on fm's, like Patrician-Bot does. (__example:__ !set_reactions on)

# Running the Bot

This bot is Docker compatible, and is how my instance runs -- however, it can be built and ran outside of Docker.

**Requirements**

* All packages specified in requirements.txt (discord.py, matplotlib, etc.) (use `pip install -r requirements.txt`).
* 2 SQL Databases - one for user settings, and one for server settings.
* Last.FM API Key - can be obtained pretty easily, see [here](https://last.fm/api).
* Discord Bot Token - can also be obtained pretty easily, see [here](https://discordapp.com/developers).

If you plan to run this using Docker, I would advise using Docker's Slim Buster image.
