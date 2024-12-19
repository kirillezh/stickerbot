"""Common sticker creation handler"""
import os
import logging
import emoji
from aiogram import Router
from aiogram.types import Message, FSInputFile, InputSticker
from aiogram.fsm.context import FSMContext
from src.states.forms import Form
from src.utils.utils import get_messages
from src.database.db import Database

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
            await message.bot.create_new_sticker_set(
                user_id=message.from_user.id,
                name=data['name'],
                title=data.get('title_videopack') or data.get('title_pack'),
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
            pack_title = data.get('title_videopack') or data.get('title_pack')
            pack_type = 'video' if is_video_pack else 'static'
            
            await db.create_pack(
                user_id=message.from_user.id,
                pack_name=data['name'],
                pack_title=pack_title,
                pack_type=pack_type
            )
            
            # New message for pack creation
            await message.reply(
                messages["new_pack_created"].format(
                    pack_type=messages["video_pack"] if is_video_pack else messages["static_pack"],
                    name=data['name'].split('_by_')[0],
                    username=data['name'].split('_by_')[1]
                ),
                parse_mode="HTML"
            )
            
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
            
            await message.reply(
                messages["complete_message"].format(
                    sticker_set_name=data['name'],
                    sticker_set_title=data.get('title_videopack') or data.get('title_pack', data['name'])
                ),
                parse_mode="HTML"
            )

        await state.clear()
    except Exception as e:
        await message.reply(messages["sticker_creation_error"])
        logging.error(f"Error processing sticker: {e}")
        await state.clear()
    finally:
        if media_path and os.path.exists(media_path):
            os.remove(media_path)