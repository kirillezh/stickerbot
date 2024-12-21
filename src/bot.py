"""
This module contains the BotInstance class for initializing and configuring the bot instance.
"""
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from src.localisation.localisation_universal import BOT_COMMANDS

class BotInstance:
    """Class for initializing and configuring bot instance."""

    def __init__(self):
        self.bot = Bot(token=os.getenv("TOKEN"))
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)

    async def setup_commands(self):
        """Setup bot commands for both Ukrainian and English languages."""
        ua_commands = BOT_COMMANDS["ua"]
        en_commands = BOT_COMMANDS["en"]
        commands = [
            ("start", ua_commands['start'], en_commands['start']),
            ("info", ua_commands['info'], en_commands['info']),
            ("mypacks", ua_commands['mypacks'], en_commands['mypacks']),
            ("newpack", ua_commands['newpack'], en_commands['newpack']),
            ("newvideopack", ua_commands['newvideopack'], en_commands['newvideopack']),
            ("setlanguage", ua_commands['setlanguage'], en_commands['setlanguage']),
            ("cancel", ua_commands['cancel'], en_commands['cancel'])
        ]
        await self.bot.set_my_commands([
            BotCommand(command=cmd, description=f"{ua} | {en}") for cmd, ua, en in commands
        ])
