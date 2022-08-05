# Simple discord.py bot example

> A simple, FOSS discord.py bot example

# API

The API is very simple, but also annoying in a way,
so what you do is:

- Go to the `CommandParser` class
- Make a syncronous function there called `cmd_<your command>`
    - Accepts arguments: `self` (the instance itself obv) and `message` (the discord message object)
- Make an asyncronous function nested inside of it
    - Assepts arguments: `command` (the parsed command)
- Return the nested asyncronous function

So an example:

```py
def cmd_say(
    self,
    message: discord.Message,
) -> Callable[[List[str]], Coroutine[Any, Any, None]]:
    async def cmd_say_resolve(command: List[str]) -> None:
        if not command:
            return

        await self._send_message(" ".join(command))

    return cmd_say_resolve
```

To use it you type `<prefix>say <something>`

In the `self` you can access these extra properties:

- `client` -- The discord client

# Licensing

I licened this project under WTFPL for a reason, do whatever
the fuck you want with it, it's nothing special, just... use it ig?
I don't care about credit or anything, just do whatever you want

# Running the bot

In a virtual environment:

```sh
python3 -m pip install virtualenv
python3 -m virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

Or globally:

```sh
python3 -m pip install --user -r requirements.txt
python3 src/main.py
```

# Configuration

All config is in `config.json` file, it has all self-explenatory
configuration options for the bot:

- `token` -- The bot token
    - <https://www.writebots.com/discord-bot-token/>
    - <https://discordpy.readthedocs.io/en/stable/intro.html>
- `bot-id` -- The bot ID
- `prefix` -- The command prefix (e.g. `!`)
- `channel-id` -- What is the main channel the bot should listen to
