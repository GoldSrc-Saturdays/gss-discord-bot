# GSS Discord Bot
The source code for the GoldSrc Saturdays Walter Bennet Discord bot.

## Setting up

### Requirements
- Python 3.8.0 or later
- A Discord account
- The following pip packages
	- discord.py 2.3.2
	- aiohttp 3.8.5
	- beautifulsoup4 4.12.2
	- pyrate-limiter 2.10.0
	- moddb 0.9.0

If you aren't installing from [requirements.txt](requirements.txt), install the packages in the order they're listed above.

### Running the bot
Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications) like normal, and copy the bot token.

Create an environment variable called GSSBOT_TOKEN and set its value to the token.

Now you should be able to run the bot.
