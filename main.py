#!/usr/bin/env python3

import discord
import random

client = discord.Client()

# Initialize bot and stuff
@client.event
async def on_ready():
    print("Bot has been initialized.")
    game = discord.Game(">help")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if "goum" in message.content.lower():
		print(f"{message.author.name} HAS GOUMED!!!")
		# NO MURDERING OR GOUMING
		await message.channel.send("STAHP!!! NO GOUMING!!!", file=discord.File("assets/gouming.png"))

	if message.content.lower() == ">help":
		print(f"{message.author.name} has called >help")
		embed = discord.Embed(title="Here is a list of commands!",
							  description=">ourple - and why he ourple\n"
										  ">samn - samn bro\n"
							  			  ">honse - i like the honses\n"
										  ">hollowgrave - Consider my power in a hollow grave\n"
										  ">8ball - Send this command with a question or something and Dr. Bennet will answer\n"
										  ">spray - Instructions how to make a custom GoldSrc spray\n"
										  ">credits - Credits and stuff\n\n"
							 			  "And remember, absolutely NO GOUMING!")
		await message.channel.send(embed=embed)

	if message.content.lower() == ">ourple":
		print(f"{message.author.name} has called >ourple")
		# and why he ourple tho
		await message.channel.send(file=discord.File("assets/ourple.png"))

	if message.content.lower() == ">samn":
		print(f"{message.author.name} has called >samn")
		# samn bro
		await message.channel.send(file=discord.File("assets/samn.png"))

	if message.content.lower() == ">honse":
		print(f"{message.author.name} has called >honse")
		# I LIKE HONSES AND SOGS
		await message.channel.send(file=discord.File("assets/HONSE.png"))

	if message.content.lower() == ">hollowgrave":
		print(f"{message.author.name} has called >hollowgrave")
		# Consider my power in a shallow grave
		await message.channel.send(file=discord.File("assets/hollowgrave.mp4"))
	
	if message.content.lower().startswith(">8ball"):
		print(f"{message.author.name} has called >8ball")
		await message.channel.send(random.choice(list(open("8ball_answers.txt"))))

	if message.content.lower() == ">spray":
		print(f"{message.author.name} has called >spray")
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
		print(f"{message.author.name} has called >credits")
		embed = discord.Embed(title="Credits",
							  description="Created by Veinhelm.\n\n"
										  "Programmed in Python using Discord.py with Visual Studio Code.\n\n"
										  "Hosted on Heroku.\n\n"
							  			  "Special thanks to my friend OliverOverworld.")
		await message.channel.send(embed=embed)

tokenfile = open("token.txt")
btoken = tokenfile.read()
tokenfile.close()
client.run(btoken)
