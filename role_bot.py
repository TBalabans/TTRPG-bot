#                    role_name = role_name.strip().lower().replace(":", "").replace(" ", "-")
import os
import discord
import csv
from discord.ext import commands
from dotenv import load_dotenv # dependancy. Run "pip install -U python-dotenv" to install

load_dotenv() # initiates dotenv (lets read from .env file)
# Discord bot token
TOKEN = os.getenv('DISCORD_TOKEN') # change this to your own token
CHANNEL_ID = os.getenv('CHANNEL_ID') # change this to channel id you want it to work in
FILE_NAME = os.getenv('FILE_NAME')# csv file name in the directory of the script

# Define intents
intents = discord.Intents.default()
intents.members = True

# Initialize the Discord client
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    #CHANNEL_ID = int(CHANNEL_ID)
    channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("Hello! I am ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith('!create_roles'):
        # Check if the user who sent the message has the necessary permissions
        if not message.author.guild_permissions.administrator:
            await message.channel.send("You do not have permission to use this command.")
            return

        # Parse the CSV file
#        with open('./Book1.csv', 'r', newline='', encoding='utf-8') as file:
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
                    role_name = role_name.strip()  # Remove leading/trailing spaces, remove ":", replace spaces with "-"
                    # Check if the role exists, create it if not
                    role = discord.utils.get(guild.roles, name=role_name)
                    if not role:
                        role = await guild.create_role(name=role_name)
                        await message.channel.send(f"Created role {role_name}.")
                    # Assign the role to the user
                    await user.add_roles(role)
                    await message.channel.send(f"Assigned role {role_name} to {user.display_name}")

    elif message.content.startswith('!assign_roles'):
        # Check if the user who sent the message has the necessary permissions
        if not message.author.guild_permissions.administrator:
            await message.channel.send("You do not have permission to use this command.")
            return

        # Parse the CSV file
#        with open('./Book1.csv', 'r', newline='', encoding='utf-8') as file:
        with open(f'./{FILE_NAME}', 'r', newline='', encoding='utf-8') as file:
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

    if message.content.startswith('!unassign_roles'):
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

    elif message.content.startswith('!create_channels'):
            # Check if the user who sent the message has the necessary permissions
            if not message.author.guild_permissions.administrator:
                await message.channel.send("You do not have permission to use this command.")
                return

            # Extract category name from the command
            command_parts = message.content.split(' ', 1)
            if len(command_parts) < 2:
                await message.channel.send("Please provide a category name and channel names.")
                return
            category_name = command_parts[1]

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
                        channel_name = channel_name.strip().lower().replace(":", "-").replace(" ", "-").replace("&", "n"). replace(".", "")
                        # Check if the channel already exists
                        existing_channel = discord.utils.get(guild.channels, name=channel_name)
                        if existing_channel:
                            await message.channel.send(f"Channel {channel_name} already exists.")
                        else:
                            # Create the channel under the specified category
                            channel = await guild.create_text_channel(channel_name, category=category)
                            await message.channel.send(f"Created channel {channel_name} under category {category_name}.")

                            # Check if a role with the same name already exists
                            role = discord.utils.get(guild.roles, name=role_name)
                            if not role:
                                # Create a role for the channel and set permissions
                                role = await guild.create_role(name=channel_name)
                            await channel.set_permissions(role, read_messages=True)
                            await message.channel.send(f"Gave the role {role.name} permissions for channel {channel_name}.")

    elif message.content.startswith('!delete_channels'):
        # Check if the user who sent the message has the necessary permissions
        if not message.author.guild_permissions.administrator:
            await message.channel.send("You do not have permission to use this command.")
            return

        # Extract category name from the command
        command_parts = message.content.split(' ', 1)
        if len(command_parts) < 2:
            await message.channel.send("Please provide a category name.")
            return

        category_name = command_parts[1]

        # Get the guild from the message
        guild = message.guild

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

                # looks up channel names
                channel_names = [name.strip().lower().replace(":", "-").replace(" ", "-").replace("&", "n"). replace(".", "") for name in row[1].split(',')]

                # Iterate through channel names
                for channel_name in channel_names:
                    # Check if the channel exists in the category and delete it
                    channel = discord.utils.get(category.channels, name=channel_name)
                    if channel:
                        await channel.delete()
                        await message.channel.send(f"Deleted channel {channel_name} under category {category_name}.")
                    else:
                        await message.channel.send(f"Channel {channel_name} not found under category {category_name}.")

    elif message.content.startswith('!delete_roles'):
        print(f"Delete roles command heard")
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
