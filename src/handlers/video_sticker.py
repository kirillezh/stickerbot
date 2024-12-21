"""
This module handles video sticker processing.
"""
import os
import logging
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.states.forms import Form
from src.services.converter import VideoConverter
from src.keyboards.reply import Keyboards
from src.utils.string_generator import get_random_string
from src.utils.utils import get_messages

router = Router()

@router.message(Command("newvideopack"))
async def start_new_video_pack(message: Message, state: FSMContext):
    """Starting the new video sticker pack creation process"""
    messages = await get_messages(user_id=message.from_user.id)
    await state.set_state(Form.title_videopack)
    await message.reply(messages["new_pack_prompt"])

@router.message(Form.title_videopack)
async def process_title_videopack(message: Message, state: FSMContext):
    """Processing video sticker pack title input"""
    messages = await get_messages(user_id=message.from_user.id)
    if len(message.text) > 30:
        return await message.reply(messages["title_too_long"])

    await state.update_data(title_videopack=message.text)
    await state.set_state(Form.name_videopack)
    await message.reply(messages["short_name_prompt"])

@router.message(Form.name_videopack)
async def process_name_videopack(message: Message, state: FSMContext):
    """Processing video sticker pack name input"""
    messages = await get_messages(user_id=message.from_user.id)
    if not message.text[0].isalpha():
        return await message.reply(messages["name_must_start_with_letter"])

    if len(message.text) > 15:
        return await message.reply(messages["name_too_long"])

    me = await message.bot.get_me()
    full_name = f"{message.text}_by_{me.username}"

    try:
        existing_set = await message.bot.get_sticker_set(full_name)
        if existing_set:
            return await message.reply(messages["pack_exists"])
    except Exception:
        pass

    await state.update_data(name=full_name)
    await state.set_state(Form.video_type_select)
    await message.reply(
        messages["choose_video_type"],
        reply_markup=await Keyboards.get_video_type_keyboard(user_id=message.from_user.id)
    )

@router.message(Form.video_type_select)
async def process_video_type(message: Message, state: FSMContext):
    """Processing video type selection"""
    messages = await get_messages(user_id=message.from_user.id)
    if message.text not in [messages["video_round"], messages["video_normal"]]:
        return await message.reply(messages["choose_convert_type"])

    await state.update_data(
        video_type="round"
        if message.text == messages["video_round"]
        else "video"
    )
    await state.set_state(Form.video)
    await message.reply(
        messages["send_video_for_sticker"],
        reply_markup=await Keyboards.get_video_back_keyboard(user_id=message.from_user.id)
    )

@router.message(Form.video)
async def process_video(message: Message, state: FSMContext):
    """Processing video input"""
    messages = await get_messages(user_id=message.from_user.id)
    if message.text == messages["back"]:
        await state.set_state(Form.video_type_select)
        return await message.reply(
            messages["choose_convert_type"],
            reply_markup=Keyboards.get_video_type_keyboard()
        )

    if not (message.video or message.video_note):
        return

    video_id = get_random_string(10)
    file_path = None

    try:
        await message.chat.do("upload_video")

        if message.video:
            file = await message.bot.get_file(message.video.file_id)
        else:
            file = await message.bot.get_file(message.video_note.file_id)

        file_path = f"file/{video_id}.mp4"
        await message.bot.download_file(file.file_path, file_path)

        data = await state.get_data()

        await message.chat.do("upload_document")
        convert_func = (
            VideoConverter.convert_round
            if data.get('video_type') == "round"
            else VideoConverter.convert_video
        )

        if convert_func(file_path):
            webm_path = f"file/{video_id}.webm"
            await state.update_data(video_path=webm_path)
            await state.set_state(Form.emoji_select)
            await message.reply(messages["send_emoji"], reply_markup=ReplyKeyboardRemove())
        else:
            await message.reply(messages["video_convert_error"])
            await state.clear()

    except Exception as e:
        logging.error("Error processing video: %s", str(e))
        await message.reply(messages["video_processing_error"])
        await state.clear()
    finally:
        if file_path and os.path.exists(file_path):
            #os.remove(file_path)
            ...

@router.message(Command("convertvideo"))
async def start_convert_choice(message: Message, state: FSMContext):
    """Start convert choice"""
    messages = await get_messages(user_id=message.from_user.id)
    await state.set_state(Form.choose_convert_type)
    await message.reply(
        messages["choose_convert_type"],
        reply_markup=await Keyboards.get_convert_keyboard(user_id=message.from_user.id)
    )

@router.message(Form.choose_convert_type)
async def process_convert_choice(message: Message, state: FSMContext):
    """Processing the conversion type selection"""
    messages = await get_messages(user_id=message.from_user.id)
    if message.text == messages["convert_to_round"]:
        await state.set_state(Form.convert_round)
        await message.reply(
            messages["send_video_note_for_conversion"],
            reply_markup=ReplyKeyboardRemove()
        )
    elif message.text == messages["convert_to_video"]:
        await state.set_state(Form.convert_vid)
        await message.reply(
            messages["send_video_for_conversion"],
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.reply(messages["choose_convert_type"])

@router.message(Form.convert_round, F.video | F.video_note)
async def process_convert_round_video(message: Message, state: FSMContext):
    """Processing conversion to round video"""
    messages = await get_messages(user_id=message.from_user.id)
    video_id = message.video.file_id if message.video else message.video_note.file_id

    try:
        await message.chat.do("upload_video")
        file = await message.bot.get_file(video_id)
        await message.bot.download_file(file.file_path, f"file/{video_id}.mp4")

        await message.chat.do("upload_document")
        if VideoConverter.convert_round(f"file/{video_id}.mp4"):
            await message.reply_document(FSInputFile(f"file/{video_id}.webm"))
            await state.clear()
        else:
            await message.reply(messages["video_convert_error"])
    except Exception as e:
        await message.reply(messages["video_processing_error"])
        logging.error("Error converting video: %s", str(e))
    finally:
        for ext in ['.mp4', '.webm']:
            if os.path.exists(f"file/{video_id}{ext}"):
                os.remove(f"file/{video_id}{ext}")

@router.message(Form.convert_vid, F.video | F.video_note)
async def process_convert_video(message: Message, state: FSMContext):
    """Processing conversion to regular video"""
    messages = await get_messages(user_id=message.from_user.id)
    video_id = message.video.file_id if message.video else message.video_note.file_id

    try:
        await message.chat.do("upload_video")
        file = await message.bot.get_file(video_id)
        await message.bot.download_file(file.file_path, f"file/{video_id}.mp4")

        await message.chat.do("upload_document")
        if VideoConverter.convert_video(f"file/{video_id}.mp4"):
            await message.reply_document(FSInputFile(f"file/{video_id}.webm"))
            await state.clear()
        else:
            await message.reply(messages["video_convert_error"])
    except Exception as e:
        await message.reply(messages["video_processing_error"])
        logging.error("Error converting video: %s", str(e))
    finally:
        for ext in ['.mp4', '.webm']:
            if os.path.exists(f"file/{video_id}{ext}"):
                os.remove(f"file/{video_id}{ext}")
