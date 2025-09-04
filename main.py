#!/usr/bin/env python3

import os
import discord
from discord import app_commands
import random
import aiohttp
from bs4 import BeautifulSoup
import moddb
import json

client = discord.Client(intents=discord.Intents(message_content=True, guild_messages=True)) # You have no idea how long it took for me to figure this out...
tree = app_commands.CommandTree(client)

if not os.path.exists("triggers.json"):
	with open("triggers.json", "w") as triggers_file:
		print("triggers.json not found. Creating...")
		triggers_file.write(json.dumps({"goum": True, "jope": True, "homestuck": True, "svench": False, "randmsg": True}))

with open("triggers.json", "r") as triggers_file:
	triggers_dict = json.loads(triggers_file.read())

# I used Chat GPT to help me with this because I suck
with open("assets/svenching.txt", "r") as svenching_file:
	svenching_words = svenching_file.readlines()

# Needs to be converted to lowercase or else it won't work with `message.content.lower()`
svenching_words = [svenching_word.strip().lower() for svenching_word in svenching_words]

async def getHalfLifeModPages():
	async with aiohttp.ClientSession() as s:
		async with s.get("https://www.moddb.com/games/half-life/mods") as r:
			soup = BeautifulSoup(await r.text(), features="html.parser")
			spacer = soup.find("span", class_="spacer")
			lastpage = spacer.find_next("a").text
	return int(lastpage)

# Initialize bot
@client.event
async def on_ready():
	print(f"{client.user} has been initialized.")
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
	
	if "goum" in message.content.lower() and triggers_dict["goum"]:
		print(f"{message.author.name} HAS GOUMED!")
		# who up gouming
		await message.channel.send("finna goum it", file=discord.File("assets/gouming.png"))
	
	if "jope" in message.content.lower() and triggers_dict["jope"]:
		print(f"{message.author.name} HAS ACKNOWLEDGED KING JOPE!")
		await message.channel.send("i love king jope  <3 i ")
	
	if "homestuck" in message.content.lower() and triggers_dict["homestuck"]:
		print(f"{message.author.name} HAS SAID HOMESTUCK!")
		# Homestuck is a webcomic created by Andrew Hussie that is widely considered to be one of the worst webcomics ever made. It is infamous for its poor writing, characters, and overall story.
		await message.channel.send("Homestuck is a webcomic.")
	
	if any(svenching_word in message.content.lower() for svenching_word in svenching_words) and triggers_dict["svench"]:
		print(f"{message.author.name} HAS SVENCHED!")
		# NO SVENCHING EITHER
		await message.channel.send("STAHP!!! NO SVENCHING!!!")
	
	if message.channel.id == 928478354414403635 and random.randint(1, 1000) == 1 and triggers_dict["randmsg"]:
		await message.channel.send(random.choice(["!", "Concerning"]))

@tree.command(name="8ball", description="Send this command with a question and Dr. Bennet will answer")
@app_commands.describe(question="Question")
async def eightball(interaction, question: str):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(f"> {question}\n{random.choice(list(open('assets/8ball_answers.txt')))}")

@tree.command(name="canada", description="he is literally canada")
async def canada(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/canada.png"))
	await interaction.response.send_message(file=discord.File("assets/canada.gif"))

@tree.command(name="cum", description="i love it")
async def cum(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/cum.png"))

@tree.command(name="gaben", description="no way")
async def gaben(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/gaben.png"))

@tree.command(name="hl_legacy", description="How to switch to HL Legacy")
async def hl_legacy(interaction):
	print(f"{interaction.user} has called ${interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/hl_legacy.png"))

@tree.command(name="hollowgrave", description="Consider my power in a hollow grave")
async def hollowgrave(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/hollowgrave.mp4"))

@tree.command(name="honse", description="i like the honses and the dobs")
async def honse(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/b1f-737620639.gif"))

@tree.command(name="hoot6", description="hoot6.wav")
async def hoot6(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/hoot6.wav"))

@tree.command(name="ourple", description="Furthermore, whatever for be his person ourple?")
async def ourple(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/ourple.png"))

@tree.command(name="pain", description="i am in constant pain")
async def pain(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/pain.png"))

@tree.command(name="randmod", description="Selects and sends a random Half-Life 1 mod from ModDB because you asked nicely")
async def randmod(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message("ok sweetheart just for you <3")
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://www.moddb.com/games/half-life/mods/page/{random.randint(1, await getHalfLifeModPages())}") as response:
			soup = moddb.soup(await response.text())
	
	thumbnails, _, _, _ = moddb.boxes._parse_results(soup)
	thumbnail = random.choice(thumbnails)

	await interaction.edit_original_response(content=thumbnail.url)

@tree.command(name="samn", description="samn bro")
async def samn(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message(file=discord.File("assets/samn.png"))

@tree.command(name="spray", description="Instructions how to make a custom GoldSrc spray")
async def spray(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	await interaction.response.send_message("i don't give a shit about your stupid ass sprays go fuck yourself")

@tree.command(name="triggers", description="[Admin] Enable or disable message triggers")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(trigger="Trigger", state="State")
@app_commands.choices(trigger = [app_commands.Choice(name=key.capitalize(), value=key) for key in triggers_dict])
async def triggers(interaction, trigger: app_commands.Choice[str], state: bool):
	print(f"{interaction.user} has called /{interaction.command.name}")
	with open("triggers.json", "w") as triggers_file:
		triggers_dict.update({trigger.value: state})
		triggers_file.write(json.dumps(triggers_dict))
	await interaction.response.send_message(f"`{trigger.name}` trigger has been set to `{state}`.")

@tree.command(name="credits")
async def credits(interaction):
	print(f"{interaction.user} has called /{interaction.command.name}")
	embed = discord.Embed(title="Credits",
					  description="Created by Gryfhorn and some dude in the server.\n"
					  "Programmed with Python using Discord.py in Visual Studio Code.\n"
					  "Hosted by Crazydog.\n"
					  "Special thanks to OliverOverworld.")
	await interaction.response.send_message(embed=embed)

# N0 K3Y 4 U! :^)
client.run(os.getenv("GSSBOT_TOKEN"))
