import os
import discord
from dotenv import load_dotenv
from leakcheck import LeakCheckAPI
from termcolor import colored
import colorama

# Initialize colorama
colorama.init()

# Load the token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LEAKCHECK_KEY = os.getenv('LEAKCHECK_KEY')

# Create a new bot instance with all intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)

leakcheck = LeakCheckAPI()
leakcheck.set_key(LEAKCHECK_KEY)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Streaming(name="18B Leaked Records", url="http://google.com"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!leakcheck'):
        if message.guild is not None:
            await message.reply("This bot operates strictly via user DMs for privacy reasons. Please send your command in a DM.")
            return

        if ' ' not in message.content:
            await message.reply("Please include an email with the `!leakcheck` command. The full format is `!leakcheck email@example.com`.")
            return

        _, email = message.content.split()
        results = leakcheck.lookup(email)
        
        print(colored(f"User {message.author} leakchecked {email}", 'magenta'))
        
        if not results:
            embed = discord.Embed(title="No Leaks Found", description=f"No leaks were found for {email}.", color=0xff0000)
            await message.author.send(embed=embed)
            return
        
        embed = discord.Embed(title="LeakCheck Results", color=0x00ff00)
        
        for i, result in enumerate(results, start=1):
            sources = ', '.join(result['sources'])
            email_only = 'Yes' if result['email_only'] else 'No'
            if ':' in result['line']:
                username, password = result['line'].split(':')
            else:
                username = result['line']
                password = 'N/A'
            last_breach = result['last_breach'] if result['last_breach'] else 'N/A'
            
            value = f"Sources: {sources}\nEmail Only: {email_only}\nUsername: {username}\nPassword: {password}\nLast Breach: {last_breach}"
            embed.add_field(name=f"Leak {i}", value=value, inline=False)
            
            if i % 25 == 0:  # Discord embed field limit
                await message.author.send(embed=embed)
                embed = discord.Embed(title="LeakCheck Results (cont'd)", color=0x00ff00)
        
        await message.author.send(embed=embed)

# Run the bot
client.run(TOKEN)