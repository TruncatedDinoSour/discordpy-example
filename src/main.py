#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample disord bot"""

import json
import os
import sys
from typing import Any, Callable, Coroutine, Dict, List, Optional

import discord  # type: ignore

CONFIG: Dict[str, Optional[Any]] = {
    "token": None,
    "bot-id": 0,
    "prefix": ";",
    "channel-id": 0,
}
CONFIG_PATH: str = "config.json"


def log(msg: str) -> None:
    print(f" > {msg}")


class CommandParser:
    def __init__(self, client: discord.Client) -> None:
        self.client: discord.Client = client

    async def _send_message(self, message: str) -> None:
        await self.client.get_channel(CONFIG["channel-id"]).send(message)

    def cmd_say(
        self,
        message: discord.Message,
    ) -> Callable[[List[str]], Coroutine[Any, Any, None]]:
        async def cmd_say_resolve(command: List[str]) -> None:
            if not command:
                return

            await self._send_message(" ".join(command))

        return cmd_say_resolve


class BotClient(discord.Client):
    async def on_ready(self) -> None:
        log(f"It's up! I am {self.user}")

    async def on_message(self, message) -> None:
        log("Message from {0.author}: {0.content}".format(message))

        if message.author.id == CONFIG["bot-id"] or not message.content.startswith(
            CONFIG["prefix"]
        ):
            return

        command: List[str] = message.content.removeprefix(CONFIG["prefix"]).split(" ")

        parser: CommandParser = CommandParser(self)

        command_handler: Optional[
            Callable[
                [discord.Message],
                Callable[[List[str]], Coroutine[Any, Any, None]],
            ]
        ] = getattr(parser, f"cmd_{command[0]}", None)

        if command_handler is None:
            await parser._send_message(
                f"<@{message.author.id}> Unknown command: {command[0]!r}"
            )
            return

        await command_handler(message)(command[1:])


def main() -> int:
    """Entry/main function"""

    if not os.path.exists(CONFIG_PATH):
        log(f"Creating new config: {CONFIG_PATH!r}")

        with open(CONFIG_PATH, "w") as cfg:
            json.dump(CONFIG, cfg, indent=4)

        log("Please configure your bot for it to run :)")
        return 1

    with open(CONFIG_PATH, "r") as cfg:
        CONFIG.update(json.load(cfg))

    BotClient().run(CONFIG["token"])

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"
    sys.exit(main())
