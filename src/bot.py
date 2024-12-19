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
        await self.bot.set_my_commands([
            BotCommand(command="start", description=f"{ua_commands['start']} | {en_commands['start']}"),
            BotCommand(command="mypacks", description=f"{ua_commands['mypacks']} | {en_commands['mypacks']}"),
            BotCommand(command="newpack", description=f"{ua_commands['newpack']} | {en_commands['newpack']}"),
            BotCommand(command="addsticker", description=f"{ua_commands['addsticker']} | {en_commands['addsticker']}"),
            BotCommand(command="convertvideo", description=f"{ua_commands['convertvideo']} | {en_commands['convertvideo']}"),
            BotCommand(command="newvideopack", description=f"{ua_commands['newvideopack']} | {en_commands['newvideopack']}"),
            BotCommand(command="addvideosticker", description=f"{ua_commands['addvideosticker']} | {en_commands['addvideosticker']}"),
            BotCommand(command="cancel", description=f"{ua_commands['cancel']} | {en_commands['cancel']}"),
            BotCommand(command="setlanguage", description=f"{ua_commands['setlanguage']} | {en_commands['setlanguage']}")
        ])