"""Common sticker creation handler"""
import os
import logging
import emoji
from aiogram import Router
from aiogram.types import Message, FSInputFile, InputSticker
from aiogram.fsm.context import FSMContext
from src.states.forms import Form
from src.utils.utils import get_messages
from src.utils.message_utils import DEFAULT_HTML_OPTIONS
from src.database.db import Database
from src.handlers.pack_management import show_pack_actions
from src.utils.sanitize_pack_name import sanitize_pack_name
router = Router()
db = Database()

@router.message(Form.emoji_select)
async def process_emoji(message: Message, state: FSMContext):
    """Processing emoji selection and finalizing pack creation"""
    messages = await get_messages(user_id=message.from_user.id)
    if not emoji.emoji_count(message.text):
        return await message.reply(messages["emoji_error"])

    data = await state.get_data()
    try:
        media_path = data.get('photo_path') or data.get('video_path')
        if not media_path:
            raise ValueError("No media path found")

        sticker_format = 'video' if 'video_path' in data else 'static'

        # Define sticker format (video or regular)
        is_video_pack = 'title_videopack' in data

        # For new pack
        if is_video_pack or 'title_pack' in data:
            me = await message.bot.get_me()  # Get bot info
            pack_title = f"{data.get('title_videopack') or data.get('title_pack')} | by @{me.username}"  # Update pack_title

            await message.bot.create_new_sticker_set(
                user_id=message.from_user.id,
                name=sanitize_pack_name(data['name']),
                title=pack_title,
                stickers=[
                    InputSticker(
                        sticker=FSInputFile(media_path),
                        emoji_list=[message.text],
                        format=sticker_format
                    )
                ],
                sticker_format=sticker_format
            )

            # Add pack to database after successful creation
            pack_type = 'video' if is_video_pack else 'static'

            await db.create_pack(
                user_id=message.from_user.id,
                pack_name=sanitize_pack_name(data['name']),
                pack_title=pack_title,
                pack_type=pack_type
            )

            # New message for pack creation
            await message.reply(
                messages["new_pack_created"].format(
                    pack_type=messages["video_pack"] if is_video_pack else messages["static_pack"],
                    name=sanitize_pack_name(data['name']),
                    title=pack_title
                ),
                **DEFAULT_HTML_OPTIONS
            )
            # Get new sticker set and show pack actions
            try:
                sticker_set = await message.bot.get_sticker_set(data['name'])
                await show_pack_actions(
                    msg=message,
                    sticker_set=sticker_set,
                    user_id=message.from_user.id,
                    messages=messages,
                    edit_message=False
                )
            except Exception as e:
                logging.error("Failed to show pack actions: %s", str(e))

        # For adding to existing pack
        else:
            await message.bot.add_sticker_to_set(
                user_id=message.from_user.id,
                name=data['name'],
                sticker=InputSticker(
                    sticker=FSInputFile(media_path),
                    emoji_list=[message.text],
                    format=sticker_format
                )
            )

            # Get pack title from database
            pack_info = await db.get_pack(message.from_user.id, data['name'])
            pack_title = pack_info[3] if pack_info else data['name']

            # Send completion message
            await message.reply(
                messages["complete_message"].format(
                    sticker_set_name=data['name'],
                    sticker_set_title=pack_title
                ),
                **DEFAULT_HTML_OPTIONS
            )

            # Get updated sticker set and show pack actions
            try:
                sticker_set = await message.bot.get_sticker_set(data['name'])
                await show_pack_actions(
                    msg=message,
                    sticker_set=sticker_set,
                    user_id=message.from_user.id,
                    messages=messages,
                    edit_message=False
                )
            except Exception as e:
                logging.error("Failed to show pack actions: %s", str(e))

        await state.clear()
    except Exception as e:
        await message.reply(messages["sticker_creation_error"])
        logging.error("Error processing sticker: %s", str(e))
        await state.clear()
    finally:
        if media_path and os.path.exists(media_path):
            os.remove(media_path)
