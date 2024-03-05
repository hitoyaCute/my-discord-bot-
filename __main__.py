webhook_channel = "webhook link"
webhook = False 
hitoya = 1200330195387813903




import requests
import json
#import pathlib
import os
import discord
from discord.ext import commands
#print(pathlib.Path(__file__).parent)

#bot constants
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)
#vars
a = True
data_dir = "data.json"


def check_server_data(guild:int) -> bool:
	guild=str(guild)
	if guild not in data['Guild_data']:
		data["Guild_data"][guild] = {
			"name" : server.name,
			"wlcm_chnl" : 0,
			"exit_chnl" : 0,
			"wlcm_msg" : "elo {member.mention} welcome to {member.guild.name}",
			"exit_msg" : "{member.name} exits the server",
			"to_dm?" : False,
			"chat_speed" : 0
		}
		return False
	return True
	
			


def data_save():
	with open(data_dir,"w") as file:
		json.dump(data,file,indent=2)

def webhook_message(username, message,img, channel=webhook_channel):
    try:
        response = requests.post(channel, data=json.dumps({'content': message, 'username': username,"avatar_url":img}), headers={'Content-Type': 'application/json'})
        return response.text
    except Exception as e:
        return e

class Member:
	def __init__(self,data):
		self = data

class Guild:
	def __init__(self,data):
		self = data

@bot.event
async def on_ready():
	global a 
	print("log in as ",bot.user.name)
	print(f"\nwe are joined on {len(bot.guilds)} discord guilds")
	print("here are the server list\n")
	for server in bot.guilds:
		print(" "+server.name)
		check_server_data(server.id)
	data_save()


	if a:#i don't want to async the command Manny times on single session 
		a=False
		cmndsLis = await bot.tree.sync()
		print(f"\nsync {len(cmndsLis)} commands")
		print("here are the commands\n"+"\n".join(map(lambda x:" "+str(x),cmndsLis)))

	await bot.change_presence(status=discord.Status.dnd)



@bot.listen()
async def on_message(message):
	global webhook
	isnotcmndyrig = False
	#make sure it will ignore message of anny bot
	if message.author.bot:
		return
	guildId = message.guild.id
	guildName = message.guild.name
	member = message.author
	g = message.guild
	member.guild = g
	
	content = message.content
	
	botping = bot.user.mention
	#message base bot trigger her
	
	if message.author.id in [hitoya]:
		#builder only commands
		#creates member object
		
		
		#commands
		if content.startswith(botping+" flip the webhook"):
			webhook = not webhook
			await message.reply("flipping to...... "+str(webhook))
		elif content.startswith(botping+" stop"):
			await message.reply("session ending......")
			exit()
		else:
			isnotcmndyrig = True
	
	
	
	
	#event based text command
	if content.lower() in ["member count"]:
		
		guild = bot.get_guild(guildId)
		members = guild.members
		await message.reply(f"we got {len(guild.members)} members")
		
	elif content.startswith("join test"):
		await on_member_join(member)
			
	elif content.startswith("leaves test"):
		await on_member_remove(member)
	#elif content.startswith()
	else :
		isnotcmndyrig = True
	print("working",webhook,isnotcmndyrig)
	if webhook and isnotcmndyrig:
		
		print(webhook_message(message.author.display_name,content,message.author.display_avatar.url))
	
	
	
	
	
	
	
	#donr touch
	if not check_server_data(message.guild.id):
		await message.channel.send("hmmm seems this server is not yet recognize leme load it on my data base")
		data_save()
	#await bot.process_commands(message)

@bot.event
async def on_member_join(member):
	guild=str(member.guild.id)
	greetings = data["Guild_data"][guild]["wlcm_msg"]
	wlcm_chnl=bot.get_channel(data["Guild_data"][guild]["wlcm_chnl"])
	#how we can send message on first most channel ?
	if not greetings and not wlcm_chnl :
		await member.send(f"hello {member.mention} welcome to {member.guild.name} sadly the server isn't set yet so I'll greet you here")

	greetings=greetings.format(member=member)
	if data["Guild_data"][guild]["to_dm?"]:
		await member.send(greetings)
	else:
		await wlcm_chnl.send(greetings)

@bot.event
async def on_member_remove(member):
	guild=str(member.guild.id)
	greetings = data["Guild_data"][guild]["exit_msg"]
	exit_chnl=bot.get_channel(data["Guild_data"][guild]["exit_chnl"])
	if not greetings and not wlcm_chnl :
		await member.send(f"hello {member.mention} welcome to {member.guild.name} sadly the server isn't set yet so I'll greet you here")

	greetings=greetings.format(member=member)
	if data["Guild_data"][guild]["to_dm?"]:
		await member.send(greetings)
	else:
		await exit_chnl.send(greetings)

#listener here
@bot.listen('on_message')
async def on_message(message):
	if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
		await message.reply('uhm '+message.author.mention+" pls don't dm if no good reason")

#text base command
@bot.command()
async def ello(ctx):
	await ctx.send(f"Ello {ctx.author.mention}")

@bot.command()
async def reactEm(ctx):
	await ctx.reply('nice')
	await ctx.message.add_reaction("🦊")
	await ctx.message.add_reaction("🤯")
	

#slash base comman
@bot.tree.command(name="ello")
async def ello(interaction: discord.Interaction):
	await interaction.response.send_message('ello '+interaction.user.mention, ephemeral=True)

@bot.tree.command(name="set_chat_speed", description="only for user with \"admin\" role")
async def wlcm_msg(interaction:discord.Interaction,max_chat_per_sec:float = float("inf")):
	guild = str(interaction.guild.id)
	
	if "admin"  not in [str(role).lower() for role in interaction.user.roles]:
		await interaction.response.send_message("srr but you need to have role \"admin\" in order to use this")
		return
	data["Guild_data"][guild]["chat_speed"] = 1.0/max_chat_per_sec
	
	data_save()
	await interaction.response.send_message(interaction.user.mention+f" new chat speed is set to {max_chat_per_sec} per sec",ephemeral=True)
	

@bot.tree.command(name="set_welcome_message", description="only for user with \"admin\" role")
async def wlcm_msg(interaction:discord.Interaction,message:str="elo {member.name.mention} welcome to {member.guild.name}"):
	guild = str(interaction.guild.id)
	
	if "admin"  not in [str(role).lower() for role in interaction.user.roles]:
		await interaction.response.send_message("srr but you need to have role \"admin\" in order to use this")
		return
	data["Guild_data"][guild]["wlcm_msg"] = message
	
	data_save()
	await interaction.response.send_message(interaction.user.mention+" new welcome message is set to "+message,ephemeral=True)

@bot.tree.command(name="set_farewell_message", description="only for user with \"admin\" role")
async def exit_msg(interaction:discord.Interaction,message:str="{member.name} exits the server"):
	guild = str(interaction.guild.id)
	
	if "admin"  not in [str(role).lower() for role in interaction.user.roles]:
		await interaction.response.send_message("srr but you need to have role \"admin\" in order to use this")
		return
	data["Guild_data"][guild]["exit_msg"] = message

	data_save()
	await interaction.response.send_message(interaction.user.mention+" new farewell message is set to "+message,ephemeral=True)

@bot.tree.command(name="set_welcome_channel", description="only for user with \"admin\" role")
async def wlcm_msg(interaction:discord.Interaction,channel:discord.TextChannel):
	guild = str(interaction.guild.id)
	
	if "admin"  not in [str(role).lower() for role in interaction.user.roles]:
		await interaction.response.send_message("srr but you need to have role \"admin\" in order to use this")
		return
	data["Guild_data"][guild]["wlcm_chnl"] = channel.id
	
	data_save()
	
	await interaction.response.send_message(interaction.user.mention+f" new welcome channel is set to <#{channel.id}>",ephemeral=True)


@bot.tree.command(name="set_farewell_channel", description="only for user with \"admin\" role")
async def exit_msg(interaction:discord.Interaction,channel:discord.TextChannel):
	guild = str(interaction.guild.id)
	
	if "admin"  not in [str(role).lower() for role in interaction.user.roles]:
		await interaction.response.send_message("srr but you need to have role \"admin\" in order to use this")
		return
	
	data["Guild_data"][guild]["exit_chnl"] = int(channel.id)

	data_save()
	await interaction.response.send_message(interaction.user.mention+f" new farewell channel is set to <#{channel.id}>",ephemeral=True)
	

if os.path.exists(data_dir):
	with open(data_dir,"r") as file:
		data = json.load(file)
else:
	data = {}

for dat in ("Guild_data","User_data","Self_data"):
		if dat not in data:
			data[dat]={}
data_save()
