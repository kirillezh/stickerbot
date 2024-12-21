"""
This module contains the Form class for managing the state of the bot.
"""
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    """Class for managing the state of the bot"""
    media_add = State()
    title_pack = State()
    name_pack = State()
    photo = State()
    convert_round = State()
    convert_vid = State()
    title_videopack = State()
    name_videopack = State()
    video = State()
    choose_convert_type = State()
    emoji_select = State()
    video_type_select = State()
    language_select = State()
    rename_pack = State()
