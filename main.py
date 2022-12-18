#!/usr/bin/env python3

import os
import discord
import moddb
import random

client = discord.Client()
hl = moddb.parse_page("https://www.moddb.com/games/half-life")

# Initialize bot and stuff
@client.event
async def on_ready():
    print("Bot has been initialized.")
    game = discord.Game(">help")
    await client.change_presence(status=discord.Status.online, activity=game)

# Sorry for the nonsense comments from this point on

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	if "goum" in message.content.lower():
		print(f"{message.author.name}#{message.author.discriminator} HAS GOUMED!!!")
		# NO MURDERING OR GOUMING
		await message.channel.send("STAHP!!! NO GOUMING!!!", file=discord.File("assets/gouming.png"))
	
	if "homestuck" in message.content.lower():
		print(f"{message.author.name}#{message.author.discriminator} HAS SAID HOMESTUCK!!!")
		# Homestuck is a webcomic created by Andrew Hussie that is widely considered to be one of the worst webcomics ever made. It is infamous for its poor writing, characters, and overall story.
		await message.channel.send("Homestuck is a webcomic created by Andrew Hussie that is widely considered to be one of the worst webcomics ever made. It is infamous for its poor writing, characters, and overall story.")

	if message.content.lower() == ">help":
		print(f"{message.author.name}#{message.author.discriminator} has called >help")
		embed = discord.Embed(title="Here is a list of commands!",
							  description=">8ball - Send this command with a question or something and Dr. Bennet will answer\n"
							  			  ">canada - he is literally canada\n"
										  ">cum - ranid loves it\n"
										  ">gaben - 3\n"
										  ">hollowgrave - Consider my power in a hollow grave\n"
										  ">honse - i like the honses\n"
										  ">hoot6 - hoot6.wav\n"
										  ">ourple - and why he ourple\n"
										  ">pain - i am in constant pain please send help\n"
										  ">randmod - Selects and sends a random Half-Life 1 mod from ModDB\n"
										  ">samn - samn bro\n"
										  ">spray - Instructions how to make a custom GoldSrc spray\n"
										  ">credits - Credits and stuff\n\n"
										  "/startserver - Start a game server (Goes offline after 10 minutes of inactivity)\n\n"
							 			  "And remember, absolutely NO GOUMING!")
		await message.channel.send(embed=embed)
	
	if message.content.lower().startswith(">8ball"):
		print(f"{message.author.name}#{message.author.discriminator} has called >8ball")
		await message.channel.send(random.choice(list(open("8ball_answers.txt"))))
	
	if message.content.lower() == ">canada":
		print(f"{message.author.name}#{message.author.discriminator} has called >canada")
		await message.channel.send(file=discord.File("assets/canada.png"))
	
	if message.content.lower() == ">cum":
		print(f"{message.author.name}#{message.author.discriminator} has called >cum")
		await message.channel.send(file=discord.File("assets/cum.png"))
	
	if message.content.lower() == ">gaben":
		print(f"{message.author.name}#{message.author.discriminator} has called >canada")
		await message.channel.send(file=discord.File("assets/gaben.png")) # 3

	if message.content.lower() == ">hollowgrave":
		print(f"{message.author.name}#{message.author.discriminator} has called >hollowgrave")
		# Consider my power in a shallow grave
		await message.channel.send(file=discord.File("assets/hollowgrave.mp4"))
	
	if message.content.lower() == ">honse":
		print(f"{message.author.name}#{message.author.discriminator} has called >honse")
		# I LIKE HONSES AND SOGS
		await message.channel.send(file=discord.File("assets/HONSE.png"))
	
	if message.content.lower() == ">hoot6":
		print(f"{message.author.name}#{message.author.discriminator} has called >hoot6")
		await message.channel.send(file=discord.File("assets/hoot6.wav"))
	
	if message.content.lower() == ">ourple":
		print(f"{message.author.name}#{message.author.discriminator} has called >ourple")
		# and why he ourple tho
		await message.channel.send(file=discord.File("assets/ourple.png"))
	
	if message.content.lower() == ">pain":
		print(f"{message.author.name}#{message.author.discriminator} has called >pain")
		# i am in constant pain please send help every second of my life is misery
		await message.channel.send(file=discord.File("assets/pain.png"))
	
	if message.content.lower() == ">samn":
		print(f"{message.author.name}#{message.author.discriminator} has called >samn")
		# samn bro
		await message.channel.send(file=discord.File("assets/samn.png"))

	# WARNING!!! THIS IS REALLY REALLY STUPID!!!
	if message.content.lower() == ">randmod":
		print(f"{message.author.name}#{message.author.discriminator} has called >randmod")
		bm = await message.channel.send("Checking ModDB...")
		mod = random.choice(hl.get_mods(random.randint(1, 40)))
		mn1 = str.replace(str(mod), "<Thumbnail name=", "")
		mn2 = str.replace(mn1, " type=mod>", "")
		await bm.edit(content=mn2)

	if message.content.lower() == ">spray":
		print(f"{message.author.name}#{message.author.discriminator} has called >spray")
		await message.channel.send("**How to create a custom GoldSrc Spray**\n"
								   "1. Find an image\n"
								   "2. Go to https://www.spraytool.net/ \n"
								   "3. Upload the image\n"
								   "4. Click `Preview`\n"
								   "5. Click `Download`\n"
								   "6. Move the `tempdecal.wad` file to your game directory (`steam/steamapps/common/Half-life/mod-name`), replacing the existing one\n"
								   "7. Right click the `tempdecal.wad` file\n"
								   "8. Click `properties`\n"
								   "9. Check the `Read-only` box\n"
								   "10. Hit `OK`\n"
								   "11. Start/restart the game\n"
								   "12. Enter a server and press the `spray` key. You may see the Half-Life logo the first time you spray - this is normal, and your custom spray should work the second time.")
	
	if message.content.lower() == ">credits":
		print(f"{message.author.name}#{message.author.discriminator} has called >credits")
		embed = discord.Embed(title="Credits",
							  description="Created by Veinhelm.\n\n"
										  "Programmed in Python using Discord.py with Visual Studio Code.\n\n"
										  "Hosted by Crazydog.\n\n"
							  			  "Special thanks to my friend OliverOverworld.")
		await message.channel.send(embed=embed)

client.run(os.getenv("GSSBOT_TOKEN"))
