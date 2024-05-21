import os
import discord
import csv
import random
from discord.ext import commands
from dotenv import load_dotenv # dependancy. Run "pip install -U python-dotenv" to install

load_dotenv() # initiates dotenv (lets read from .env file)
# .env
TOKEN = os.getenv('DISCORD_TOKEN') # token can be changed i .env file
CHANNEL_ID = os.getenv('CHANNEL_ID') # channel can be chaneged in .env file
FILE_NAME = os.getenv('FILE_NAME')# csv file name can be chanegd in .env file

# Define intents
intents = discord.Intents.default()
intents.members = True

# Initialize the Discord client
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! I am ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

# Function to clean and format channel names
def format_channel_name(name):
    return name.strip().lower().replace(":", "-").replace(" ", "-").replace("&", "n").replace(".", "")

@client.command(name='create_roles', help='Create roles from CSV column 2')
async def create_roles(message):
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You do not have permission to use this command.")
        return
    # Parse the CSV file
    with open(f'./{FILE_NAME}', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader) #skips first row
        for row in reader:  

            user_name = row[0] # Assuming global username here
            if row[1] == '':
                continue
            roles = row[1].split(',')  # Split roles by comma

            # Get the user and the guild from the message
            guild = message.guild
            user = discord.utils.get(guild.members, name=user_name.lower().strip()) #set to lowercase, remove leading/trailing spaces        

            # Logging for debugging
            print(f"Searching for user: {user_name}")
            print(f"User found: {user}")

            # If user not found by global name, look for display name                  
            if not user:
                user = discord.utils.get(guild.members, display_name=user_name.strip()) #remove leading/trailing spaces
                await message.channel.send(f"Looking for {user_name}.")

            # If user still not found, skip to the next row
            if not user:
                await message.channel.send(f"User {user_name} not found.")
                continue

            # Assign each role to the user
            for role_name in roles:
                role_name = role_name.strip()  # Remove leading/trailing spaces
                # Check if the role exists, create it if not
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    role = await guild.create_role(name=role_name)
                    await message.channel.send(f"Created role {role_name}.")
                # Assign the role to the user
                await user.add_roles(role)
                await message.channel.send(f"Assigned role {role_name} to {user.display_name}")

@client.command(name='assign_roles', help='Assign roles from CSV collumn 3 to users from collumn 1')
async def assign_roles(message):
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You do not have permission to use this command.")
        return
    # Parse the CSV file
#        with open('./Book1.csv', 'r', newline='', encoding='utf-8') as file:
    with open(f'./{FILE_NAME}', 'r', newline='', encoding='utf-8') as file:
        
        reader = csv.reader(file, delimiter=';')
        next(reader) #skips first row
        print(f"assign roles heard0")

        for row in reader:  
            user_name = row[0] # Assuming global username here
            print(f"user_name")
            #checks if role row is empty
            if row[2] == '':
                continue
            print(f"assign roles heard1")
            roles = row[2].split(',')  # Split roles by comma
            # Get the user and the guild from the message
            print(f"assign roles heard2")
            guild = message.guild
            user = discord.utils.get(guild.members, name=user_name.lower().strip()) #set to lowercase, remove leading/trailing spaces        
            print(f"assign roles heard3")
            # Logging for debugging
            print(f"Searching for user: {user_name}")
            print(f"User found: {user}")
            # If user not found by global name, look for display name                  
            if not user:
                user = discord.utils.get(guild.members, display_name=user_name.strip()) #remove leading/trailing spaces
                await message.channel.send(f"Looking for {user_name}.")
            # If user still not found, skip to the next row
            if not user:
                await message.channel.send(f"User {user_name} not found.")
                continue
            # Assign each role to the user
            for role_name in roles:
                role_name = role_name.strip()  # Remove leading/trailing spaces
                # Check if the role exists, spit if not
                role = discord.utils.get(guild.roles, name=role_name)                    
                if not role:
                    continue
                # Assign the role to the user
                await user.add_roles(role)
                await message.channel.send(f"Assigned role {role_name} to {user.display_name}")

@client.command(name='unassign_roles', help='Unassign role from CSV column 3 from users in column 1')
async def unassign_roles(message):
    print(f"Command heard")
    # Check if the user who sent the message has the necessary permissions
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You do not have permission to use this command.")
        return

    # Parse the CSV file
    with open(FILE_NAME, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader) #skips first row
        for row in reader:  

            user_name = row[0] # Assuming global username here
            #checks if role row is empty
            if row[2] == '':
                continue
            roles = row[2].split(',')  # Split roles by comma

            # Get the user and the guild from the message
            guild = message.guild
            user = discord.utils.get(guild.members, name=user_name.lower().strip()) #set to lowercase, remove leading/trailing spaces        

            # Logging for debugging
            print(f"Searching for user: {user_name}")
            print(f"User found: {user}")

            # If user not found by global name, look for display name                  
            if not user:
                user = discord.utils.get(guild.members, display_name=user_name.strip()) #remove leading/trailing spaces
                await message.channel.send(f"Looking for {user_name}.")

            # If user still not found, skip to the next row
            if not user:
                await message.channel.send(f"User {user_name} not found.")
                continue

            # Unassign each role from the user
            for role_name in roles:
                role_name = role_name.strip()  # Remove leading/trailing spaces
                # Check if the role exists, continue if not
                role = discord.utils.get(guild.roles, name=role_name)                    
                if not role:
                    continue
                # Remove the role from the user
                await user.remove_roles(role)
                await message.channel.send(f"Removed role {role_name} from {user.display_name}")

@client.command(name='create_channels', help='Create channels from CSV column 2. You need to pass a category name.')
async def create_channels(message, category_name):
    # Check if the user who sent the message has the necessary permissions
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You do not have permission to use this command.")
        return

    created_channels = set()
    # Get the guild from the message
    guild = message.guild

    # Create category if it doesn't exist
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
        await message.channel.send(f"Created category {category_name}.")

    # Open the CSV file and read the second row
    with open(f'./{FILE_NAME}', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header row
        for row in reader:
            # Skip empty rows
            if not row:
                continue

            channel_names = [name.strip() for name in row[1].split(',')]

            # Create channels under the specified category
            for channel_name in channel_names:
                #save role name and then format role name into a channel name
                role_name = channel_name
                #channel_name = channel_name.strip().lower().replace(":", "-").replace(" ", "-").replace("&", "n"). replace(".", "")
                channel_name = format_channel_name(channel_name)

                # Check if the channel has already been processed
                if channel_name in created_channels:
                    continue
                
                # Check if the channel already exists
                existing_channel = discord.utils.get(guild.channels, name=channel_name)
                if existing_channel:
                    await message.channel.send(f"Channel {channel_name} already exists.")
                else:
                    # Create the channel under the specified category
                    channel = await guild.create_text_channel(channel_name, category=category)
                    await message.channel.send(f"Created channel {channel_name} under category {category_name}.")

                    # Add the channel to the set of processed channels
                    created_channels.add(channel_name)

                    # Check if a role with the same name already exists
                    role = discord.utils.get(guild.roles, name=role_name)
                    if not role:
                        # Create a role for the channel and set permissions
                        role = await guild.create_role(name=channel_name)
                    await channel.set_permissions(role, read_messages=True)
                    await message.channel.send(f"Gave the role {role.name} permissions for channel {channel_name}.")

@client.command(name='delete_channels', help='Delete channels from CSV column 2. You need to pass a category name')
async def delete_channels(message, category_name):
    # Check if the user who sent the message has the necessary permissions
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You do not have permission to use this command.")
        return

    guild = message.guild
    deleted_channels = set()

    # Get the category object
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await message.channel.send(f"Category {category_name} not found.")
        return

    # Open the CSV file and delete channels under the specified category
    with open(f'./{FILE_NAME}', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header row
        for row in reader:
            # Skip empty rows
            if not row:
                continue


            # Look up channel names using the format_channel_name function
            channel_names = [format_channel_name(name) for name in row[1].split(',')]


            # Iterate through channel names
            for channel_name in channel_names:
                if channel_name in deleted_channels:
                    continue
                # Add the channel to the set of processed channels
                deleted_channels.add(channel_name)
                # Check if the channel exists in the category and delete it
                channel = discord.utils.get(category.channels, name=channel_name)
                if channel:
                    await channel.delete()
                    await message.channel.send(f"Deleted channel {channel_name} under category {category_name}.")
                else:
                    await message.channel.send(f"Channel {channel_name} not found under category {category_name}.")

@client.command(name='delete_roles', help='delete roles from CSV column 2')
async def delete_roles(message):
    # Check if the user who sent the message has the necessary permissions
    if not message.author.guild_permissions.administrator:
        await message.channel.send("You do not have permission to use this command.")
        return

    # Open the CSV file and delete roles
    with open(f'./{FILE_NAME}', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header row
        for row in reader:
            # Skip empty rows
            if not row:
                continue

            role_names = [name.strip() for name in row[1].split(',')]

            # Iterate through role names
            for role_name in role_names:
                # Check if the role exists and delete it
                role = discord.utils.get(message.guild.roles, name=role_name)
                if role:
                    await role.delete()
                    await message.channel.send(f"Deleted role {role_name}.")
                else:
                    await message.channel.send(f"Role {role_name} not found.")
                    
client.run(TOKEN)
