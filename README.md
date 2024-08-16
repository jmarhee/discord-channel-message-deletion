# Discord Channel Message Deletion Bot

When run, it will delete the available message history for a channel up to the hardcoded batch size.

Run this on a cronjob to make it a recurring behavior.

## Setup

Your Bot should have permissions to manage messages in your server.

It should be setup for Guild Install.

You will need your Server ID, and any channel IDs you wish to manage.

**Note** If you right click and "copy link" on any of your server's channel, you can find this information:

https://discord.com/channels/{server_id}/{channel_id}

In your `discord.config` file, populate the following:

```toml
[discord_settings]
token = BOT_TOKEN
channels = 123456,7890123
server_id = 123456788
```

Do **not** quote these strings.

## Running

Install the requirements:

```bash
pip3 install -r requirements.txt
```

and run the script:

```
python3 main.py -c ./discord.config
```

To have this job run periodically, one option is to run it as a Cron Job:

```
0 */6 * * * /usr/bin/nohup /usr/bin/python3 -u /home/jdmarhee/repos/discord-bot/main.py -c /home/jdmarhee/repos/discord-bot/discord.config >> /home/jdmarhee/discord_runtime.out 2>> /home/jdmarhee/discord.err &
```
