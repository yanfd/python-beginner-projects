import asyncio
import discord
from discord import app_commands
import sys
import os
from dotenv import load_dotenv
from Chat_GPT_Function import correct_grammar

load_dotenv(override=True)

try:
    token = os.getenv("BOT_TOKEN") # returns a str
    owner_uid = int(os.getenv("OWNER_ID")) # returns an int
    gpt_key = os.getenv("GPT_API_KEY") # returns a str
    discord_server_1 = int(os.getenv("DISCORD_SERVER_1"))  # Discord Server ID 1 returns int
    discord_server_2 = int(os.getenv("DISCORD_SERVER_2"))  # Discord Server ID 2 returns int (this one is optional)
except(TypeError, ValueError):
    sys.exit("Error: One or more environment variables are not set or contain invalid values.") # Stops the bot from starting if the .env is formatted wrong
    
discord_server_1 = discord.Object(id= discord_server_1)  # Discord Server ID 1 returns int
discord_server_2 = discord.Object(id= discord_server_2)  # Discord Server ID 2 returns int (this one is optional)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra states to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this, we just synchronize the app commands to specified guilds.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    # This allows for faster bot testing and development.
    async def setup_hook(self):
        # This copies the global commands over to your guild(s).
        self.tree.copy_global_to(guild=discord_server_1)
        await self.tree.sync(guild=discord_server_1)
        self.tree.copy_global_to(guild=discord_server_2)
        await self.tree.sync(guild=discord_server_2)

    async def on_message(self, message): # Whenever a user sends a message it is logged into the console
        try:
            print(f'Message from {message.author}({message.author.id}) in {message.guild}({message.channel.name}): {message.content}')
            if message.author.id == self.user.id:
                return
        except AttributeError:
            print("Unable to print logged user message 'DMChannel' error (Cant log sent commands)") # This print() statement isnt needed. 
                                                                                                    # you can remove it if you want. I like it for debug purposes
            return
            


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("-------------------------------")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='For Slash Commands')) # This changes the activity that is displayed
                                                                                                                           # under the bots name in the members list.


@client.tree.command(name="test_bot", description="Replies with 'Hello!'")
async def running_test(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}", ephemeral=True) # ephemeral=True means the bots response is only visible
                                                                                                  # to the user who used the command.


@client.tree.command(name="shutdown", description="Shuts down the bot") # Shuts down the bot if the user matches the owner_uid
async def shutdown_bot(interaction: discord.Interaction):
    if interaction.user.id == owner_uid:
        await interaction.response.send_message("Shutting down the bot...")
        await client.close()
    else:
        await interaction.response.send_message("You don't have permission to shut down the bot.", ephemeral=True)


@client.tree.command(name="clear", description="Deletes defined number of messages from the current channel.")
@app_commands.rename(to_delete="messages")
@app_commands.describe(to_delete="Number of messages to delete")
async def send(interaction: discord.Interaction, to_delete: int):
    await interaction.response.defer(ephemeral=True)
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.followup.send("Invalid permissions")
        return
    if to_delete <= 0:
        await interaction.followup.send("Invalid number")
        return
    else:
        await interaction.followup.send("Deleting...")
        await interaction.channel.purge(limit=to_delete)
        await interaction.edit_original_response(content=f"Deleted {to_delete} messages.")


@client.tree.command(name="ping", description="Get bot latency")
async def ping(interaction: discord.Interaction):
    try:
        await interaction.response.defer(ephemeral=True)  # Defer the response to prevent command timeout

        # Get bot latency
        latency = round(client.latency * 1000)

        # Send as followup message
        await interaction.followup.send(f"Pong! Latency: {latency}ms")
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {str(e)}")
        await interaction.followup.send("An error occurred while processing the command.")
        
@client.tree.command(name="gpt_correct_grammar", description="Corrects grammar of inputted text")
@app_commands.rename(text_to_send="text_to_correct")
@app_commands.describe(text_to_send="Text to grammar correct")
async def send(interaction: discord.Interaction, text_to_send: str):
    try:
        await interaction.response.defer(ephemeral=False)  # Defer the response to prevent command timeout

        # Send as followup message
        await interaction.followup.send(correct_grammar(text_to_send))
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {str(e)}")
        await interaction.followup.send("An error occurred while processing the command.")

client.run(token)
