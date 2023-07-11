#!/usr/bin/env python3

import os
import discord
from discord import app_commands
import moddb
import aiohttp
import random

client = discord.Client(intents=discord.Intents(message_content=True, guild_messages=True)) # You have no idea how long it took for me to figure this out...
tree = app_commands.CommandTree(client)

# I used Chat GPT to help me with this because I suck
with open("assets/svenching.txt", "r") as svenching_file:
	svenching_words = svenching_file.readlines()

# Needs to be converted to lowercase or else it won't work with `message.content.lower()`
svenching_words = [svenching_word.strip().lower() for svenching_word in svenching_words]

# Initialize bot
@client.event
async def on_ready():
	print("Bot has been initialized.")
	try:
		synced = await tree.sync()
		print(f"Synced {len(synced)} commands.")
	except Exception as e:
	    print(e)

@client.event
async def on_message(message):
	# Make sure a message that would normally be a trigger isn't from the bot itself
	if message.author == client.user:
		return
	
	if "goum" in message.content.lower():
		print(f"{message.author.name} HAS GOUMED!")
		# NO MURDERING OR GOUMING
		await message.channel.send("STAHP!!! NO GOUMING!!!", file=discord.File("assets/gouming.png"))
	
	if "jope" in message.content.lower():
		print(f"{message.author.name} HAS ACKNOWLEDGED KING JOPE!")
		await message.channel.send("ALL HAIL KING JOPE")
	
	if "homestuck" in message.content.lower():
		print(f"{message.author.name} HAS SAID HOMESTUCK!")
		# Homestuck is a webcomic created by Andrew Hussie that is widely considered to be one of the worst webcomics ever made. It is infamous for its poor writing, characters, and overall story.
		await message.channel.send("Homestuck is a webcomic created by Andrew Hussie that is widely considered to be one of the worst webcomics ever made. It is infamous for its poor writing, characters, and overall story.")
	
	if any(svenching_word in message.content.lower() for svenching_word in svenching_words):
		print(f"{message.author.name} HAS SVENCHED!")
		# NO SVENCHING EITHER
		await message.channel.send("STAHP!!! NO SVENCHING!!!")

@tree.command(name="8ball", description="Send this command with a question and Dr. Bennet will answer")
@app_commands.describe(question="Question")
async def command(interaction, question: str):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(random.choice(list(open("assets/8ball_answers.txt"))))

@tree.command(name="canada", description="he is literally canada")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/canada.png"))

@tree.command(name="cum", description="ranid loves it")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/cum.png"))

@tree.command(name="gaben", description="no way")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/gaben.png"))

@tree.command(name="hollowgrave", description="Consider my power in a hollow grave")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/hollowgrave.mp4"))

@tree.command(name="honse", description="i like the honses and the dobs")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/HONSE.png"))

@tree.command(name="hoot6", description="hoot6.wav")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/hoot6.wav"))

@tree.command(name="ourple", description="and why he ourple")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/ourple.png"))

@tree.command(name="pain", description="i am in constant pain")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/pain.png"))

@tree.command(name="randmod", description="Selects and sends a random Half-Life 1 mod from ModDB")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message("Checking ModDB...")
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://www.moddb.com/games/half-life/mods/page/{random.randint(1, 43)}") as response:
			# I don't know if there's a way to make it pick any page, so that will have to do
			soup = moddb.soup(await response.text())
	
	thumbnails, _, _, _ = moddb.boxes._parse_results(soup)
	thumbnail = random.choice(thumbnails)

	await interaction.edit_original_response(content=thumbnail.url)

@tree.command(name="samn", description="samn bro")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/samn.png"))

@tree.command(name="spray", description="Instructions how to make a custom GoldSrc spray")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message("**How to create a custom GoldSrc Spray**\n"
					 "1. Find an image\n"
					 "2. Go to https://www.spraytool.net/ \n"
					 "3. Upload the image\n"
					 "4. Click `Preview`\n"
					 "5. Click `Download`\n"
					 "6. Move the `tempdecal.wad` file to your game directory (`Steam/steamapps/common/Half-life/mod-name`), replacing the existing one\n"
					 "7. Right click the `tempdecal.wad` file\n"
					 "8. Click `properties`\n"
					 "9. Check the `Read-only` box\n"
					 "10. Hit `OK`\n"
					 "11. Start/restart the game\n"
					 "12. Enter a server and press the `spray` key. You may see the Half-Life logo the first time you spray - this is normal, and your custom spray should work the second time.")

@tree.command(name="credits")
async def command(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	embed = discord.Embed(title="Credits",
					  description="Created by Gryfhorn.\n"
					  "Programmed with Python using Discord.py in Visual Studio Code.\n"
					  "Hosted by Crazydog.\n"
					  "Special thanks to OliverOverworld.")
	await interaction.response.send_message(embed=embed)

# N0 K3Y 4 U! :^)
client.run(os.getenv("GSSBOT_TOKEN"))
