#!/usr/bin/env python3

#########################
#		NOTICE			#
#########################
# I AM NOT RESPONSIBLE	#
# FOR ANY TRAUMA,		#
# INJURY, OR DEATH THAT	#
# MAY OCCUR FROM THE	#
# VIEWING OF THE		#
# FOLLOWING CODE. I		#
# WILL MAKE IT BETTER	#
# SOME DAY!!!			#
#########################

# TODO: convert this shit to cogs, or at least make it a bit cleaner

import os
import discord
from discord import app_commands
import random
import aiohttp
from bs4 import BeautifulSoup
import moddb
import json
import datetime
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

client = discord.Client(intents=discord.Intents(message_content=True, guild_messages=True, guild_scheduled_events=True, guilds=True)) # You have no idea how long it took for me to figure this out...
tree = app_commands.CommandTree(client)

if not os.path.exists("triggers.json"):
	with open("triggers.json", "w") as triggers_file:
		print("triggers.json not found. Creating...")
		triggers_file.write(json.dumps({"goum": True, "jope": True, "homestuck": True, "svench": False, "randmsg": True}))

if not os.path.exists("offset.json"):
	with open("offset.json", "w") as offset_file:
		print("offset.json not found. Creating...")
		# Stored in its own file to keep the config.json file easy to read and edit
		offset_file.write(json.dumps({"": 0}))

if not os.path.exists("schedule.json"):
	with open("schedule.json", "w") as schedule_file:
		print("schedule.json not found. Creating...")
		schedule_file.write(json.dumps({}))

with open("triggers.json", "r") as triggers_file:
	triggers_dict = json.loads(triggers_file.read())

with open("config.json", "r") as config_file:
	botConfig = json.loads(config_file.read())

with open("gameData.json", "r") as gameData_file:
	gameData = json.loads(gameData_file.read())

with open("offset.json", "r") as offset_file:
	# Read from a json rather than a txt file so the value is automatically read as an integer
	weekOffset = json.loads(offset_file.read())

with open("schedule.json", "r") as schedule_file:
	eventSchedule = json.loads(schedule_file.read())

with open("assets/svenching.txt", "r") as svenching_file:
	svenching_words = svenching_file.readlines()

# Needs to be converted to lowercase as well or else it won't work with `message.content.lower()`
svenching_words = [svenching_word.strip().lower() for svenching_word in svenching_words]

async def getHalfLifeModPages(session: aiohttp.ClientSession):
	async with session.get("https://www.moddb.com/games/half-life/mods") as r:
		soup = BeautifulSoup(await r.text(), features="html.parser")
		spacer = soup.find("span", class_="spacer")
		lastpage = spacer.find_next("a").text
	return int(lastpage)

def getNextDayOfWeek(date, day_of_week):
	days_until_next_day = (day_of_week - date.weekday() + 7) % 7
	return date + datetime.timedelta(days=days_until_next_day)

def findSaturday(future = 0):
	start = datetime.datetime.now() + datetime.timedelta(weeks=future)
	next_saturday = getNextDayOfWeek(start, 5) # 5 represents Saturday
	if datetime.datetime.now(pytz.timezone(botConfig["timezone"])).dst():
		return next_saturday.replace(hour=19, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
	else:
		return next_saturday.replace(hour=20, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
	# Uses UTC rather than EST/EDT because using eastern time for some reason causes it to add 56 minutes to the value... What the fuck??

def findWeekCount():
	first = datetime.datetime(year=2021, month=12, day=11, tzinfo=datetime.timezone.utc) # First Saturday
	delta = abs(findSaturday() - first)
	delta = datetime.timedelta(seconds=int(delta.total_seconds()))
	# The offset will generally be used for subtracting, but the value is added just in case if anyone
	# wants to make their own version of this bot and need to add for whatever reason.
	return (delta.days // 7) + weekOffset[""]

async def sendReminderAnnouncement1():
	if str(findSaturday()) in eventSchedule:
		print("Sending day reminder")
		msg = f"<@&{gameData[eventSchedule[str(findSaturday())]["game"]]["roleId"]}> Reminder: {gameData[eventSchedule[str(findSaturday())]["game"]]["name"]} tomorrow at <t:{int(findSaturday().timestamp())}:T>! {botConfig["invite"]}?event={eventSchedule[str(findSaturday())]["id"]}"
		await client.get_guild(botConfig["guildId"]).get_channel(botConfig["announcementChannelId"]).send(msg)
		await client.get_guild(botConfig["guildId"]).get_channel(botConfig["extAnnouncementChannelId"]).send(msg)

async def sendReminderAnnouncement2():
	if str(findSaturday()) in eventSchedule:
		print("Sending hour reminder")
		await client.get_guild(botConfig["guildId"]).get_channel(botConfig["announcementChannelId"]).send(f"<@&{gameData[eventSchedule[str(findSaturday())]["game"]]["roleId"]}> {gameData[eventSchedule[str(findSaturday())]["game"]]["name"]} in ONE HOUR! {botConfig["invite"]}?event={eventSchedule[str(findSaturday())]["id"]}")

async def sendStartAnnouncement():
	if str(findSaturday()) in eventSchedule:
		print("Sending start announcement")
		msg = f"<@&{gameData[eventSchedule[str(findSaturday())]["game"]]["roleId"]}> {gameData[eventSchedule[str(findSaturday())]["game"]]["name"]} NOW!!! {gameData[eventSchedule[str(findSaturday())]["game"]]["ip"]}"
		await client.get_guild(botConfig["guildId"]).get_channel(botConfig["announcementChannelId"]).send(msg)
		await client.get_guild(botConfig["guildId"]).get_channel(botConfig["extAnnouncementChannelId"]).send(msg)
		with open("schedule.json", "w") as schedule_file:
			eventSchedule.pop(str(findSaturday()))
			schedule_file.write(json.dumps(eventSchedule))

#async def checkDST(scheduler: AsyncIOScheduler):
#	dst1 = datetime.datetime.now(pytz.timezone(botConfig["timezone"])).dst()
#	while True:
#		await asyncio.sleep(1800) # 30 minutes
#		print("Checking for DST change...")
#		dst2 = datetime.datetime.now(pytz.timezone(botConfig["timezone"])).dst()
#		if dst1 != dst2:
#			print("Updated for DST change")
#			scheduler.reschedule_job("remind1", trigger=CronTrigger(day_of_week="fri", hour=15, minute=0, second=0, timezone=pytz.timezone(botConfig["timezone"])))
#			scheduler.reschedule_job("remind2", trigger=CronTrigger(day_of_week="sat", hour=14, minute=0, second=0, timezone=pytz.timezone(botConfig["timezone"])))
#			scheduler.reschedule_job("start", trigger=CronTrigger(day_of_week="sat", hour=15, minute=0, second=10, timezone=pytz.timezone(botConfig["timezone"])))
#			dst1 = dst2
#		else:
#			print("DST has not changed")

# Initialize bot
@client.event
async def on_ready():
	print(f"{client.user} has been initialized.")

	scheduler = AsyncIOScheduler()

	scheduler.add_job(sendReminderAnnouncement1, CronTrigger(day_of_week="fri", hour=15, minute=0, second=0, timezone=pytz.timezone(botConfig["timezone"])), id="remind1")
	scheduler.add_job(sendReminderAnnouncement2, CronTrigger(day_of_week="sat", hour=14, minute=0, second=0, timezone=pytz.timezone(botConfig["timezone"])), id="remind2")
	scheduler.add_job(sendStartAnnouncement, CronTrigger(day_of_week="sat", hour=15, minute=0, second=0, timezone=pytz.timezone(botConfig["timezone"])), id="start")
	
	scheduler.start()

	#client.loop.create_task(checkDST(scheduler))

	try:
		synced = await tree.sync()
		print(f"Synced {len(synced)} commands.")
	except Exception as e:
	    print(e)

@client.event
async def on_message(message: discord.Message):
	# Make sure a message that would normally be a trigger isn't from the bot itself
	if message.author == client.user:
		return
	
	if "goum" in message.content.lower() and triggers_dict["goum"]:
		print(f"{message.author.name} HAS GOUMED!")
		# NO MURDERING OR GOUMING
		await message.channel.send("STAHP!!! NO GOUMING!!!", file=discord.File("assets/gouming.png"))
	
	if "jope" in message.content.lower() and triggers_dict["jope"]:
		print(f"{message.author.name} HAS ACKNOWLEDGED KING JOPE!")
		await message.channel.send("ALL HAIL KING JOPE")
	
	if "homestuck" in message.content.lower() and triggers_dict["homestuck"]:
		print(f"{message.author.name} HAS SAID HOMESTUCK!")
		# Homestuck is a webcomic created by Andrew Hussie that is widely considered to be one of the worst webcomics ever made. It is infamous for its poor writing, characters, and overall story.
		await message.channel.send("Homestuck is a webcomic created by Andrew Hussie that is widely considered to be one of the worst webcomics ever made. It is infamous for its poor writing, characters, and overall story.")
	
	if any(svenching_word in message.content.lower() for svenching_word in svenching_words) and triggers_dict["svench"]:
		print(f"{message.author.name} HAS SVENCHED!")
		# NO SVENCHING EITHER
		await message.channel.send("STAHP!!! NO SVENCHING!!!")
	
	if message.channel.id == botConfig["historyChannelId"] and not message.author.get_role(botConfig["historyRoleId"]):
		await message.author.add_roles(discord.utils.get(message.guild.roles, id=botConfig["historyRoleId"]))
	
	if message.channel.id == botConfig["generalId"] and random.randint(1, 1000) == 1 and triggers_dict["randmsg"]:
		await message.channel.send(random.choice(["!", "Concerning"]))

@tree.command(name="8ball", description="Send this command with a question and Dr. Bennet will answer")
@app_commands.describe(question="Question")
async def eightball(interaction: discord.Interaction, question: str):
	await interaction.response.send_message(f"> {question}\n{random.choice(list(open('assets/8ball_answers.txt')))}")

@tree.command(name="canada", description="he is literally canada")
async def canada(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/canada.png"))

@tree.command(name="cum", description="ranid loves it")
async def cum(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/cum.png"))

@tree.command(name="gaben", description="no way")
async def gaben(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/gaben.png"))

@tree.command(name="hollowgrave", description="Consider my power in a hollow grave")
async def hollowgrave(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/hollowgrave.mp4"))

@tree.command(name="honse", description="i like the honses and the dobs")
async def honse(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/HONSE.png"))

@tree.command(name="hoot6", description="hoot6.wav")
async def hoot6(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/hoot6.wav"))

@tree.command(name="ourple", description="and why he ourple")
async def ourple(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/ourple.png"))

@tree.command(name="pain", description="i am in constant pain")
async def pain(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/pain.png"))

@tree.command(name="randmod", description="Selects and sends a random Half-Life 1 mod from ModDB")
async def randmod(interaction: discord.Interaction):
	await interaction.response.send_message("Checking ModDB...")
	async with aiohttp.ClientSession() as session:
		async with session.get(f"https://www.moddb.com/games/half-life/mods/page/{random.randint(1, await getHalfLifeModPages(session))}") as response:
			soup = moddb.soup(await response.text())
	
	thumbnails, _, _, _ = moddb.boxes._parse_results(soup)
	thumbnail = random.choice(thumbnails)

	await interaction.edit_original_response(content=thumbnail.url)

@tree.command(name="samn", description="samn bro")
async def samn(interaction: discord.Interaction):
	await interaction.response.send_message(file=discord.File("assets/samn.png"))

@tree.command(name="schedule", description="Schedule an event")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(game="Game", announce="Announce", event_location="Event Location", event_subtitle="Event Subtitle", event_description="Event Description", week_number="Week Number")
@app_commands.choices(game = [app_commands.Choice(name=gameData[key]["name"], value=key) for key in gameData])
async def schedule(interaction: discord.Interaction, game: app_commands.Choice[str], announce: bool, event_location: str = None, event_subtitle: str = None, event_description: str = "Come play or watch live at https://twitch.tv/GoldSrcSaturdays", week_number: int = None):
	if not week_number:
		# This has to be done or else the offset won't update
		week_number = findWeekCount()
	if not event_location:
		event_location = gameData[game.value]["ip"]
	
	eventname = f"Week {week_number} - {game.name}"
	if event_subtitle:
		eventname = f"{eventname} - {event_subtitle}"
	if "link" in gameData[game.value]:
		event_description = f"Download the mod: {gameData[game.value]["link"]}\n{event_description}"
	
	if week_number < findWeekCount():
		await interaction.response.send_message(f"Week number cannot be in the past. Entered `{week_number}`, next is `{findWeekCount()}`.")
		return
	
	future = week_number - findWeekCount()

	if str(findSaturday(future)) in eventSchedule and week_number == eventSchedule[str(findSaturday(future))]["week"]:
		print("Updating existing event")
		event = await client.get_guild(interaction.guild.id).get_scheduled_event(eventSchedule[str(findSaturday(future))]["id"]).edit(
			name=eventname,
			privacy_level=discord.PrivacyLevel.guild_only,
			start_time=findSaturday(future),
			end_time=findSaturday(future) + datetime.timedelta(hours=2),
			description=event_description,
			entity_type=discord.EntityType.external,
			image=Path(f"assets/games/{game.value}.png").read_bytes(),
			location=event_location
		)
		with open("schedule.json", "w") as schedule_file:
			eventSchedule.update({str(findSaturday(future)): {"game": game.value, "week": week_number, "id": event.id}})
			schedule_file.write(json.dumps(eventSchedule))
		await interaction.response.send_message(f"Updated `{game.name}` for week `{week_number}`")
		print(f"{interaction.user} has updated {game.name} for week {week_number}")
	else:
		print("Creating new event")
		event = await client.get_guild(interaction.guild.id).create_scheduled_event(
			name=eventname,
			privacy_level=discord.PrivacyLevel.guild_only,
			start_time=findSaturday(future),
			end_time=findSaturday(future) + datetime.timedelta(hours=2),
			description=event_description,
			entity_type=discord.EntityType.external,
			image=Path(f"assets/games/{game.value}.png").read_bytes(),
			location=event_location
		)
		with open("schedule.json", "w") as schedule_file:
			eventSchedule.update({str(findSaturday(future)): {"game": game.value, "week": week_number, "id": event.id}})
			schedule_file.write(json.dumps(eventSchedule))
		await interaction.response.send_message(f"Scheduled `{game.name}` for week `{week_number}`")
		print(f"{interaction.user} has scheduled {game.name} for week {week_number}")
	if announce:
		await interaction.guild.get_channel(botConfig["announcementChannelId"]).send(f"<@&{gameData[game.value]["roleId"]}> Saturday #{week_number} will be {game.name}. {botConfig["invite"]}?event={event.id}")

@tree.command(name="spray", description="Instructions how to make a custom GoldSrc spray")
async def spray(interaction: discord.Interaction):
	await interaction.response.send_message(
		"**How to create a custom GoldSrc Spray**\n"
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
		"12. Enter a server and press the `spray` key. You may see the Half-Life logo the first time you spray - this is normal, and your custom spray should work the second time."
	)

@tree.command(name="triggers", description="[Admin] Enable or disable message triggers")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(trigger="Trigger", state="State")
@app_commands.choices(trigger = [app_commands.Choice(name=key.capitalize(), value=key) for key in triggers_dict])
async def triggers(interaction: discord.Interaction, trigger: app_commands.Choice[str], state: bool):	
	with open("triggers.json", "w") as triggers_file:
		triggers_dict.update({trigger.value: state})
		triggers_file.write(json.dumps(triggers_dict))
	await interaction.response.send_message(f"`{trigger.name}` trigger has been set to `{state}`.")
	print(f"{interaction.user} has set trigger \"{trigger.name}\" to {state}")

@tree.command(name="weekoffset", description="[Admin] Set how many weeks the week count is offset by")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(offset="Use a positive or negative value")
async def weekoffset(interaction: discord.Interaction, offset: int):
	weekOffset.update({"": offset})
	with open("offset.json", "w") as offset_file:
		offset_file.write(json.dumps(weekOffset))
	await interaction.response.send_message(f"Week offset has been set to `{weekOffset[""]}`.")
	print(f"{interaction.user} has set week offset to {weekOffset[""]}")

@tree.command(name="weekoffsetget", description="[Admin] Get how many weeks the week count is offset by")
@app_commands.default_permissions(administrator=True)
async def weekoffsetget(interaction: discord.Interaction):
	await interaction.response.send_message(f"Week offset is currently set to `{weekOffset[""]}`.")

@tree.command(name="credits")
async def credits(interaction: discord.Interaction):
	embed = discord.Embed(title="Credits",
					  description="Created by Gryfhorn.\n"
					  "Programmed with Python using Discord.py in Visual Studio Code.\n"
					  "Hosted by Crazydog.\n"
					  "Special thanks to OliverOverworld.")
	await interaction.response.send_message(embed=embed)

# N0 K3Y 4 U! :^)
client.run(os.getenv("GSSBOT_TOKEN"))
