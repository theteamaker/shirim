# Shirim - Eva Twin's Patrician Bot

A bot designed to output last.fm data. Designed with a non-committal minimalist philosophy.
Much of this bot's frontend is based off of [Amb1tion's Patrician-Bot](https://github.com/Amb1tion/Patrician-Bot), with a new backend and more consistent ways to fetch data.
To invite the bot to your server, click [here](https://discordapp.com/api/oauth2/authorize?client_id=659885086707286017&permissions=0&scope=bot).

# General Commands

**set**: sets your last.fm username (__example:__ ::set skiffskiffles)

**fm**: fetches your most recent last.fm scrobble. (__example:__ ::fm)

**weekly, monthly, 3months, 6months, yearly, alltime**: these commands fetch your top albums in a given timeframe. has optional arguments as well. (__example:__ ::weekly 3x3 -nc)

_optional arguments:_ <chart size: 3x3, 4x4, 5x5, 2x6> <-nc> (-nc generates a chart without captions over the album covers)

**get**: fetches someone else's data. has optional arguments. (__example:__ ::get <username/discord mention>)

_optional arguments:_ <chart type (e.g. weekly, monthly)> <chart size> <-nc> (__example:__ ::get evatwin weekly 4x4 -nc)

**taste**: compares your listening habits to another person's. (__example:__ ::taste <username/discord mention>)

# Configuration

**set_prefix**: can only be used by the server owner. sets a custom prefix for the server.

# Running the Bot

This bot is Docker compatible, and is how my instance runs -- however, it can be built and ran outside of Docker.

_**Requirements**_

* All packages specified in requirements.txt (discord.py, matplotlib, etc.) (use `pip install -r requirements.txt`).
* 2 SQL Databases. One for user settings, and one for server settings.
* Last.FM API Key. Can be obtained pretty easily, see [here](https://last.fm/api).
* Discord Bot Token. Can also be obtained pretty easily, see [here](https://discordapp.com/developers).

If you plan to run this using Docker, I would advise *not* using Docker's Alpine image, as it seems to crash upon attempting to install **matplotlib**.
