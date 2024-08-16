import discord
import time
import asyncio
import os
import configparser
import argparse
import string

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configPath", help = "Config File Path")

args = parser.parse_args()

config = configparser.RawConfigParser()
config.read(args.configPath)
config_values = dict(config.items('discord_settings'))

intents = discord.Intents.all()
intents.message_content = True
intents.guild_messages = True
client = discord.Client(intents=intents)

channels = config_values['channels'].split(",")
TOKEN = config_values['token']
SERVER_ID = config_values['server_id']
if config_values.get("batch_size") is None:
   batch_size = 100
else:
   batch_size = config_values['batch_size']

def channel_clear(client, channel_ids, batch_size):
    # Move this to config a file.
    BATCH_SIZE = batch_size  # Adjust batch size as needed

    async def delete_messages_in_channel(channel):
        messages_deleted = 0
        while True:
            try:
                deleted = await channel.purge(limit=BATCH_SIZE)
                messages_deleted += len(deleted)
                if len(deleted) < BATCH_SIZE:
                    break  # Reached end of messages
            except discord.errors.Forbidden:
                print(f"Bot lacks permission to delete messages in channel {channel.id}")
            except discord.HTTPException as e:
                print(f"Error deleting messages in channel {channel.id}: {e}")
        return messages_deleted

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        for channel_id in channels:  # Assuming `channels` is a list of channel IDs
            channel = await client.fetch_channel(channel_id)
            if channel:
                messages_deleted = await delete_messages_in_channel(channel)
                print(f"Deleted {messages_deleted} messages from channel {channel.id}.")
            else:
                print(f"Channel with ID {channel_id} not found.")
        os._exit(os.EX_OK)

    async def main():
        channels = channel_ids
        tasks = []
        for channel_id in channels:
            try:
                channel = await client.fetch_channel(channel_id)
                if channel:
                    task = asyncio.create_task(delete_messages_in_channel(channel))
                    tasks.append(task)
            except discord.errors.NotFound:
                print(f"Channel with ID {channel_id} not found.")
            except Exception as e:
                print(f"Error processing channel {channel_id}: {e}")

        await asyncio.gather(*tasks)

    return client.run(TOKEN)

channel_clear(client, channels, batch_size)
