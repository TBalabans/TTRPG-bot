
Description:
A localy run Discord bot that takes a local csv file filled with global usernames and roles. It then uses those to create and assign roles to users and the delete those roles.
List of commands:
- !create_roles – creates roles based on the 2nd column of the .csv file and assigns them to a user in the 1st column of the .csv file. There can be multiple roles in the 2nd column. If the bot can’t find a user by the global username it will attempt to find it by a nickname.
- !create_channels {category} -  creates channels under the category given in the commad (example: !create_channels TTRPG Diena). Roles are created based on the 2nd column of the .csv file. Roles must already be created before using this command.
- !delete_channels {category] – deletes channels under the category given in the commad (example: !create_channels TTRPG Diena). Deletes channels based on the 2nd column of the .csv file. !BE VERY CAREFUL WITH THIS!
- !delete_roles – deletes roles based on the 2nd column of the .csv file. !BE VERY CAREFUL WITH THIS!
- !assign_roles - assigns roles from column 3 to users. Does not attempt to create them.
- !unassign_roles - assigns roles from column 3 to users. Does delete them.

Instructions:
1. Add the bot to a server.
	a.Give it permissions to manage channels and manage roles
2. Open the role_bot.py file in a code editor of your choice that supports python. (open with administrator privileges)
	a.Make sure you have python installed
	b.Make sure you have the discord.py library installed. This can be done by using the command “pip install discord.py”
	c.Make sure you have dotenv installed. This can be done by using the command "pip install -U python-dotenv"
3. Modify the parameters in the .env as neccesary:
	a.TOKEN: discord bot token from a developer account
	b.CHANNEL_ID: the id of the channel you want the bot to talk in. This is where it will write logs and hear commands. You can get the channel ID if you have Developer mode enabled (User Settings->Advanced->Developer mode) by right clicking on a channel and clicking “Copy Channel ID”
	c.FILE_NAME: The name of the csv file the bot will use. The default name is “Book1.csv”. The file has to be located in the same directory as the script.
4. Start the bot by running the “python role_bot.py” command in the console.
	a.If you’ve done everything correctly, then the bot will write in chat “Hello! I am ready!”
	b.Bot will only listen to commands given by a user with moderator permissions
5. Add a Book1.csv file to the directory of the bot. The file must contain 2 collumns and the first row must contain titles of the rows.
	a.Column 1 must contain the global names of the user you want to add roles to
	b.Column 2 must contain the roles you want to assign to the users. Multiple roles seperated by comma can be entered in the same line. This column will be used to create and delete roles as well.
6. The bot can then be closed by using the ctrl+c command in the console.


