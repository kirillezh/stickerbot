"""
This module contains handlers for common commands.
"""
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.keyboards.reply import Keyboards
from src.states.forms import Form
from src.utils.utils import get_messages
from src.utils.message_utils import DEFAULT_HTML_OPTIONS
from src.database.db import Database

router = Router()
db = Database()

@router.message(Command("start"))
async def start(message: Message):
    """Handle the /start command"""
    messages = await get_messages(user_id=message.from_user.id)
    await message.answer(messages["start_message"])

@router.message(Command("info"))
async def info(message: Message):
    """Handle the /info command"""
    with open("info.json", "r", encoding="utf-8") as f:
        await message.answer(f.read(), **DEFAULT_HTML_OPTIONS)

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    """Handle the /cancel command"""
    messages = await get_messages(user_id=message.from_user.id)
    await state.clear()
    await message.reply(messages["cancel_message"], reply_markup=ReplyKeyboardRemove())

@router.message(Command("complete"))
async def complete(message: Message, state: FSMContext):
    """Handle the /complete command"""
    messages = await get_messages(user_id=message.from_user.id)
    data = await state.get_data()
    if 'name' not in data:
        return
    try:
        sticker_set = await message.bot.get_sticker_set(data['name'])
        await message.answer(
            messages["complete_message"].format(
                sticker_set_name=sticker_set.name,
                sticker_set_title=sticker_set.title
            ),
            **DEFAULT_HTML_OPTIONS
        )
        await state.clear()
    except Exception:
        return

@router.message(Command("setlanguage"))
async def set_language(message: Message, state: FSMContext):
    """Handle the /setlanguage command"""
    messages = await get_messages(user_id=message.from_user.id)
    await state.set_state(Form.language_select)
    await message.reply(messages["choose_language"],
                        reply_markup=await Keyboards.get_language_keyboard(state))

@router.message(Form.language_select)
async def process_language_selection(message: Message, state: FSMContext):
    """Process the language selection"""
    messages = await get_messages(state)
    if message.text == messages["language_ukrainian"]:
        await db.set_user_language(message.from_user.id, "ua")
    elif message.text == messages["language_english"]:
        await db.set_user_language(message.from_user.id, "en")
    else:
        return await message.reply(messages["choose_language"])

    messages = await get_messages(user_id=message.from_user.id)
    await state.clear()
    await message.reply(messages["language_set"], reply_markup=ReplyKeyboardRemove())
