"""
This module handles photo sticker processing.
"""
import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.states.forms import Form
from src.services.image_processor import ImageProcessor
from src.utils.utils import get_messages
router = Router()

@router.message(Command("newpack"))
async def start_new_pack(message: Message, state: FSMContext):
    """Start creating a new sticker pack"""
    messages = await get_messages(user_id=message.from_user.id)
    await state.set_state(Form.title_pack)
    await message.reply(messages["new_pack_prompt"])

@router.message(Form.title_pack)
async def process_title(message: Message, state: FSMContext):
    """Process sticker pack title"""
    messages = await get_messages(user_id=message.from_user.id)
    if len(message.text) > 30:
        return await message.reply(messages["title_too_long"])

    await state.update_data(title_pack=message.text)
    await state.set_state(Form.name_pack)
    await message.reply(messages["short_name_prompt"])

@router.message(Form.name_pack)
async def process_name(message: Message, state: FSMContext):
    """Process short name for sticker pack"""
    messages = await get_messages(user_id=message.from_user.id)

    # Check first letter
    if not message.text[0].isalpha():
        return await message.reply(messages["name_must_start_with_letter"])

    # Check length
    if len(message.text) > 15:
        return await message.reply(messages["name_too_long"])

    # Check allowed characters
    if not all(c.isalnum() or c == '_' for c in message.text):
        return await message.reply(messages["invalid_name_chars"])

    me = await message.bot.get_me()
    full_name = f"{message.text}_by_{me.username}"

    try:
        existing_set = await message.bot.get_sticker_set(full_name)
        if existing_set:
            return await message.reply(messages["pack_exists"])
    except Exception:
        pass

    await state.update_data(name=full_name)  # Save full name
    await state.set_state(Form.photo)
    await message.reply(messages["send_photo"])

@router.message(Form.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Process photo sticker"""
    messages = await get_messages(user_id=message.from_user.id)
    photo_id = message.photo[-1].file_unique_id
    file = await message.bot.get_file(message.photo[-1].file_id)
    await message.bot.download_file(file.file_path, f"file/{photo_id}.png")

    try:
        ImageProcessor.resize_image(f"file/{photo_id}.png")
        await state.update_data(photo_path=f"file/{photo_id}.png")
        await state.set_state(Form.emoji_select)
        await message.reply(messages["send_emoji"])
    except Exception:
        await message.reply(messages["error_processing_photo"])
        if os.path.exists(f"file/{photo_id}.png"):
            os.remove(f"file/{photo_id}.png")

@router.message(Form.media_add, F.photo)
async def add_sticker_to_pack(message: Message, state: FSMContext):
    """Add sticker to pack"""
    messages = await get_messages(user_id=message.from_user.id)
    photo_id = (
        message.photo[0].file_unique_id
        if message.media_group_id is None
        else message.media_group_id
    )

    data = await state.get_data()
    if data.get('media_add') == photo_id:
        return

    await state.update_data(media_add=photo_id)

    file = await message.bot.get_file(message.photo[-1].file_id)
    await message.bot.download_file(file.file_path, f"file/{photo_id}.png")

    try:
        ImageProcessor.resize_image(f"file/{photo_id}.png")
        await state.update_data(photo_path=f"file/{photo_id}.png")
        await state.set_state(Form.emoji_select)
        await message.reply(messages["send_emoji"])
    except Exception:
        await message.reply(messages["sticker_add_error"])
        if os.path.exists(f"file/{photo_id}.png"):
            os.remove(f"file/{photo_id}.png")
