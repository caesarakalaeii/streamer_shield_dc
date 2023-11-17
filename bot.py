import discord
from discord.ext import commands
import requests

# Discord Bot Token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# API Endpoint
API_ENDPOINT = 'YOUR_REST_API_ENDPOINT'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    # Send the new member's username to the REST API
    response = send_to_api(member.name)

    if response is not None:
        # Check the response value
        value = response.get('value', 0)

        if value > 0.5:
            # Ban the user
            await member.guild.ban(member, reason=f'Scored {value} on the API')
            print(f'Banning user {member.name} with a score of {value}')
        else:
            print(f'User {member.name} joined with a score of {value}, not banning')
    else:
        print(f'Unable to check user {member.name}')

def send_to_api(username):
    # Send a POST request to the API endpoint
    data = {'username': username}
    try:
        response = requests.post(API_ENDPOINT, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.status_code} - {response.text}')
            return None
    except requests.RequestException as e:
        print(f'Request to API failed: {e}')
        return None

# Run the bot
bot.run(TOKEN)
