import discord
import json
from discord.ext import commands
import datetime
import asyncio
import random
import os


def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]	

		

client = commands.Bot(command_prefix = get_prefix)



@client.event
async def on_ready():

	

	await client.change_presence(activity=discord.Game(name=f"on {len(client.guilds)} servers | .help"))

	print("Your bot is ready.")

async def ch_pr():
	await client.wait_until_ready()
	statuses = [f"on {len(client.guilds)} servers | .help"]
	while not client.is_closed():
		status = random.choice(statuses)

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]




@client.event
async def on_guild_join(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = '.'

	with open('prefixes.json', 'w')	as f:
		json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

	with open('prefixes.json', 'w')	as f:
		json.dump(prefixes, f, indent=4)




@client.command()
async def invite(ctx):
	await ctx.author.send("To invite me use this: https://discord.com/api/oauth2/authorize?client_id=800743017958080522&permissions=8&scope=bot")






@client.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
	with open('prefixes.json', 'r') as f:
	 	prefixes = json.load(f)
	
	prefixes[str(ctx.guild.id)] = prefix
	
	with open('prefixes.json', 'w')	as f:
		json.dump(prefixes, f, indent=4)

	await ctx.send(f'Prefix changed to: `{prefix}`')
	

@client.command()
async def poll(ctx,*,message):
	emb=discord.Embed(title="POLL", description=f"{message}")
	msg=await ctx.channel.send(embed=emb)
	await msg.add_reaction('👍')
	await msg.add_reaction('👎')

@client.event
async def on_message(msg):
	for word in filtered_words:
		if word in msg.content:
			await msg.delete()
	
	await client.process_commands(msg)


@client.command()
async def hello(ctx):
	await ctx.send("hi")



filtered_words = ["fuck","shit","motherfucker","assholer","krab","dick","pussy","pucci","idiot"]



@client.command(aliases=['c','purge'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "No reason provided"):
	try:
		await member.send("You have been kicked from server. Reason:"+reason)
	except:
		await ctx.send("The member was kicked; but their dms are closed!")
	
	await member.kick(reason=reason)


@client.event
async def on_command_error(ctx,error):
	if isinstance(error,commands.MissingPermissions):
		await ctx.send("You don't have permission to do that! ;-;")
	elif isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("Please enter all the required args.")		

@client.command(aliases=['b','ez'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
	
	await ctx.send(member.mention +" has been banned from the server. Reason: "+reason)

	await member.ban(reason=reason)

@client.command(aliases=['ub','unez'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
	banned_users = await ctx.guild.bans()
	member_name, member_disc = member.split('#')
	
	for banned_entry in banned_users:
		user = banned_entry.user

		if(user.name, user.discriminator)==(member_name, member_disc):

			await ctx.guild.unban(user)
			await ctx.send(member_name +" has been unbanned!")
			return

	await ctx.send(member+" was not found")

@client.command(aliases=['m'])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")

	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

	await member.add_roles(mutedRole, reason=reason)
	await ctx.send(f"**Muted {member.mention}. Reason: {reason}**")
	await member.send(f"**You were muted in the server: {guild.name}. Reason: {reason}.")
	await asyncio.sleep(mute_time)
	await member.remove_roles(role)

@client.command(aliases=['um'])
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	await member.remove_roles(mutedRole)
	await ctx.send(f"**Unmuted {member.mention}!**")
	await member.send(f"**You were unmuted in the server {ctx.guild.name}**")


@client.command(aliases=['user','info'])
async def whois(ctx, member : discord.Member):
	embed = discord.Embed(title = member.name , description = member.mention , color = discord.Color.green())
	embed.add_field(name = "ID", value = member.id , inline = True )
	embed.set_thumbnail(url = member.avatar_url)
	
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
	
	await ctx.send(embed=embed)






client.remove_command("help")


@client.group(invoke_without_command=True)
async def help(ctx):
	em = discord.Embed(title = "Help", description = "Here is a list of command categories.", color = discord.Colour.green())

	em.add_field(name = "Moderation", value = "Type `.moderation` to get list of moderation commands!", inline = True)
	em.add_field(name = "Fun", value = "Type `.fun` to see fun commands!", inline = True)
	em.add_field(name = "Information", value = "Type `.infocmds` to see list of information commands!", inline = True)
	em.add_field(name = "Giveaways", value = "Type `.ghelp` to see list of giveaway commands!", inline = True)
	em.add_field(name = "Invite", value = "Type `.invite` to get my invite link!", inline = True)

	em.set_thumbnail(url = "https://i.gyazo.com/ee840e0540d647261c447ad9a445b5e4.png")
	em.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")


	await ctx.author.send(embed = em)
	


@client.command(aliases=['mod'])
async def moderation(ctx):
	embed = discord.Embed(title = "Moderation Commands" , description = "Commands" , color = discord.Color.green())
	embed.add_field(name = "Kick", value = "Usage: `.kick <member/id> [reason]` Aliases: k", inline = True)
	embed.add_field(name = "Ban", value = "Usage: `.ban <member/id> [reason]` Aliases: b , ez", inline = True)
	embed.add_field(name = "Mute", value = "Usage: `.mute <member/id>` Aliases: m", inline = True)
	embed.add_field(name = "Change Prefix", value = "Usage: `.changeprefix <newprefix>`", inline = True)
	embed.add_field(name = "Clear", value = "Usage: `.clear <amount>` Aliases: c , purge", inline = True)
	embed.set_thumbnail(url = "https://i.gyazo.com/72813ce44477bf1c5f28a58a3d2d237b.png")
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
	await ctx.send(embed=embed)


@client.command()
async def fun(ctx):
	embed = discord.Embed(title = "Fun Commands" , description = "Commands" , color = discord.Color.blue())
	embed.add_field(name = "Meme", value = "Usage: `.meme`", inline = True)
	embed.set_thumbnail(url = "https://cdn.broadbandsearch.net/blog/most-popular-internet-memes-in-history/success-baby-fly.jpg")
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
	await ctx.send(embed=embed)

@client.command()
async def infocmds(ctx):
	embed = discord.Embed(title = "Information Commands" , description = "Commands:" , color = discord.Color.green())
	embed.add_field(name = "Who is", value = "Usage: `.whois <member/id>` Aliases: user , info", inline = True)
	embed.set_thumbnail(url = "https://i.gyazo.com/72813ce44477bf1c5f28a58a3d2d237b.png")
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
	await ctx.send(embed=embed)

@client.command()
async def ghelp(ctx):
	embed = discord.Embed(title = "Giveaway Commands" , description = "Commands")
	embed.add_field(name = "Create Giveaway (Administrator Only)", value = "Usage: `.gcreate` Aliases: giveaway", inline = True)
	embed.set_thumbnail(url = "https://images.emojiterra.com/google/android-11/128px/1f389.png")
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
	await ctx.send(embed=embed)

invitemsg = ["To invite me to your server use this link! :white_check_mark: https://discord.com/api/oauth2/authorize?client_id=800743017958080522&permissions=2146959351&scope=bot"]

@client.command
async def invite(ctx):
	await ctx.author.send(invitemsg)

@client.command(aliases=['gcreate'])
@commands.has_permissions(administrator = True)
async def giveaway(ctx):
	await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

	questions = ["Which channel should it be hosted in?", 
            	"What should be the duration of the giveaway? (s|m|h|d)",
            	"What is the prize of the giveaway?"]

	answers = []

	def check(m):
		return m.author == ctx.author and m.channel == ctx.channel 

	for i in questions:
		await ctx.send(i)

		try:
			msg = await client.wait_for('message', timeout=15.0, check=check)
		except asyncio.TimeoutError:
			await ctx.send('You didn\'t answer in time, please be quicker next time!')
			return
		else:
			answers.append(msg.content)

    
	try:
		c_id = int(answers[0][2:-1])
	except:
		await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
		return

	channel = client.get_channel(c_id)

	time = convert(answers[1])
	if time == -1:
		await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
		return
	elif time == -2:
		await ctx.send(f"The time must be an integer. Please enter an integer next time")
		return            

	prize = answers[2]

	await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


	embed = discord.Embed(title = "Giveaway!", description = f"**Prize**: {prize}", color = ctx.author.color)

	embed.add_field(name = "Hosted by:", value = ctx.author.mention)

	embed.set_footer(text = f"Ends {answers[1]} from now!")

	embed.set_thumbnail(url = "https://images.emojiterra.com/google/android-11/128px/1f389.png")

	my_msg = await channel.send(embed = embed)


	await my_msg.add_reaction("🎉")


	await asyncio.sleep(time)


	new_msg = await channel.fetch_message(my_msg.id)


	users = await new_msg.reactions[0].users().flatten()
	users.pop(users.index(client.user))

	winner = random.choice(users)

	await channel.send(f"**Giveaway ended!** **Winner:** {winner.mention}.  **Prize:** *{prize}* ")


@client.command(aliases=['greroll'])
@commands.has_permissions(administrator = True)
async def rerollgiveaway(ctx, channel : discord.TextChannel, id_ : int):
	try:
		new_msg = await channel.fetch_message(id_)
	except:
		await ctx.send("The id was entered incorrectly.")
		return
    
	users = await new_msg.reactions[0].users().flatten()
	users.pop(users.index(client.user))

	winner = random.choice(users)

	await channel.send(f"Congratulations! The new winner is {winner.mention}.!")



client.run(os.environ['TOKEN'])