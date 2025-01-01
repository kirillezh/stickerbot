"""
This module handles the management of sticker packs.
"""
import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.utils.utils import get_messages
from src.keyboards.reply import Keyboards
from src.database.db import Database
from src.states.forms import Form
from src.localisation.localisation_universal import COMPONENTS_HTML
from src.utils.message_utils import DEFAULT_HTML_OPTIONS

router = Router()
db = Database()

# Define states for pack management
class PackStates(StatesGroup):
    """States for pack management"""
    rename_pack = State()

async def show_pack_actions(
        msg: Message,
        sticker_set,
        user_id: int,
        messages: dict,
        show_back_button: bool = True,
        edit_message: bool = True
    ):
    """Helper function to show pack actions"""
    keyboard = await Keyboards.get_pack_actions_keyboard(
        sticker_set.name,
        user_id,
        show_back_button,
        remove_stickers=len(sticker_set.stickers) > 1
    )

    message_text = messages["pack_actions"].format(
        title=COMPONENTS_HTML["link"]["sticker_set"].format(
            name=sticker_set.name,
            title=sticker_set.title
        )
    )

    if edit_message:
        try:
            await msg.edit_text(
                message_text,
                reply_markup=keyboard,
                **DEFAULT_HTML_OPTIONS
            )
        except Exception as e:
            logging.error("Failed to edit message: %s", str(e))
            # Fallback to new message if edit fails
            await msg.answer(
                message_text,
                reply_markup=keyboard,
                **DEFAULT_HTML_OPTIONS
            )
    else:
        await msg.answer(
            message_text,
            reply_markup=keyboard,
            **DEFAULT_HTML_OPTIONS
        )

@router.message(Command("mypacks"))
async def show_user_packs(message: Message | CallbackQuery, page: int = 1):
    """Show user's sticker packs"""
    is_callback = isinstance(message, CallbackQuery)
    msg = message.message if is_callback else message
    user_id = message.from_user.id if is_callback else msg.from_user.id
    messages = await get_messages(user_id=user_id)
    bot_sets = []
    try:
        user_packs = await db.get_user_packs(user_id)
        if not user_packs:
            if is_callback:
                await msg.edit_text(messages["no_packs"])
            else:
                await msg.answer(messages["no_packs"])
            return
        # Get actual sticker sets from Telegram
        for pack in user_packs:
            try:
                sticker_set = await msg.bot.get_sticker_set(pack[2])
                bot_sets.append(sticker_set)
            except Exception as e:
                logging.error("Failed to get sticker set %s", str(e))
                await db.delete_pack(user_id, pack[2])
                continue

        if not bot_sets:
            if is_callback:
                await msg.edit_text(messages["no_packs"])
            else:
                await msg.answer(messages["no_packs"])
            return

        # If only one pack, show it directly
        if len(bot_sets) == 1:
            await show_pack_actions(
                msg,
                bot_sets[0],
                user_id,
                messages,
                show_back_button=False,
                edit_message=False)
            return

        # Calculate pagination for multiple packs
        total_packs = len(bot_sets)
        total_pages = (total_packs + 9) // 10

        keyboard = await Keyboards.get_packs_keyboard(
            bot_sets, page, total_pages, user_id
        )

        if is_callback:
            await msg.edit_text(messages["my_packs"], reply_markup=keyboard, **DEFAULT_HTML_OPTIONS)
        else:
            await msg.answer(messages["my_packs"], reply_markup=keyboard, **DEFAULT_HTML_OPTIONS)

    except Exception as e:
        logging.error("Error getting sticker packs: %s", str(e))
        if is_callback:
            await msg.edit_text(messages["pack_not_found"])
        else:
            await msg.answer(messages["pack_not_found"])

@router.callback_query(F.data.startswith("pack_"))
async def process_pack_selection(callback: CallbackQuery):
    """Process pack selection"""
    pack_name = callback.data[5:]
    messages = await get_messages(user_id=callback.from_user.id)

    try:
        # Verify pack exists in database
        pack_info = await db.get_pack(callback.from_user.id, pack_name)
        if not pack_info:
            await callback.message.edit_text(messages["pack_not_found"])
            return

        # Get actual sticker set from Telegram
        sticker_set = await callback.bot.get_sticker_set(pack_name)
        await show_pack_actions(
            callback.message,
            sticker_set,
            callback.from_user.id,
            messages,
            edit_message=True)
    except Exception as e:
        logging.error("Error processing pack selection: %s", str(e))
        await callback.message.edit_text(messages["pack_not_found"])

@router.callback_query(F.data.startswith("delete_"))
async def confirm_delete_pack(callback: CallbackQuery):
    """Confirm pack deletion"""
    pack_name = callback.data[7:]
    messages = await get_messages(user_id=callback.from_user.id)

    try:
        sticker_set = await callback.bot.get_sticker_set(pack_name)
        keyboard = await Keyboards.get_confirm_delete_keyboard(pack_name, callback.from_user.id)

        await callback.message.edit_text(
            messages["confirm_delete_pack"].format(title=sticker_set.title),
            reply_markup=keyboard,
            **DEFAULT_HTML_OPTIONS
        )
    except Exception as e:
        logging.error("Error confirming pack deletion: %s", str(e))
        await callback.message.edit_text(messages["pack_not_found"])

@router.callback_query(F.data.startswith("confirmdelete_"))
async def delete_pack(callback: CallbackQuery):
    """Delete pack"""
    pack_name = callback.data[14:]
    user_id = callback.from_user.id
    messages = await get_messages(user_id=user_id)
    try:
        # First verify the pack exists in Telegram
        try:
            await callback.bot.get_sticker_set(pack_name)
        except Exception as e:
            logging.error("Pack not found in Telegram: %s %s", pack_name, str(e))
            # If pack doesn't exist in Telegram, just remove from DB and continue
            await db.delete_pack(user_id, pack_name)
            await callback.message.edit_text(messages["pack_deleted"])
            await show_user_packs(callback)
            return

        # Try to delete from Telegram first - this is the crucial part
        try:
            await callback.bot.delete_sticker_set(pack_name)
        except Exception as e:
            logging.error("Failed to delete pack '%s' from Telegram: %s", pack_name, str(e))
            await callback.message.edit_text(messages["pack_not_found"])
            return

        # If Telegram deletion succeeded, clean up the DB
        await db.delete_pack(user_id, pack_name)

        await callback.message.edit_text(messages["pack_deleted"])
        await show_user_packs(callback)

    except Exception as e:
        logging.error("Unexpected error deleting pack '%s': %s", pack_name, str(e))
        await callback.message.edit_text(messages["pack_not_found"])

@router.callback_query(F.data.startswith("add_"))
async def start_add_sticker(callback: CallbackQuery, state: FSMContext):
    """Start adding sticker to pack"""
    pack_name = callback.data[4:]
    messages = await get_messages(user_id=callback.from_user.id)

    try:
        # Verify pack exists in database
        pack_info = await db.get_pack(callback.from_user.id, pack_name)
        if not pack_info:
            await callback.message.edit_text(messages["pack_not_found"])
            return

        sticker_set = await callback.bot.get_sticker_set(pack_name)
        await state.update_data(name=pack_name)

        # Check if it's a video pack
        is_video = any(s.is_video for s in sticker_set.stickers)

        if is_video:
            # Use video sticker flow
            await state.set_state(Form.video_type_select)
            # Use answer instead of edit_text for video
            await callback.message.answer(
                messages["selected_pack"].format(
                    sticker_set_name=sticker_set.name,
                    sticker_set_title=sticker_set.title,
                    send_photo=messages["send_video_for_sticker"]
                ),
                **DEFAULT_HTML_OPTIONS,
                reply_markup=await Keyboards.get_video_type_keyboard(user_id=callback.from_user.id)
            )
            await callback.message.delete()
        else:
            # Use photo sticker flow
            await state.set_state(Form.media_add)
            # For photo just send a new message
            await callback.message.answer(
                messages["selected_pack"].format(
                    sticker_set_name=sticker_set.name,
                    sticker_set_title=sticker_set.title,
                    send_photo=messages["send_next_photo"]
                ),
                **DEFAULT_HTML_OPTIONS
            )
            await callback.message.delete()

    except Exception as e:
        logging.error("Error starting sticker addition: %s", str(e))
        await callback.message.edit_text(messages["pack_not_found"])

@router.callback_query(F.data == "back_to_packs")
async def back_to_packs(callback: CallbackQuery):
    """Return to packs list"""
    await show_user_packs(callback)

@router.callback_query(F.data == "close_actions")
async def close_actions(callback: CallbackQuery):
    """Close pack actions"""
    messages = await get_messages(user_id=callback.from_user.id)
    await callback.message.edit_text(messages["closed_actions"])

@router.callback_query(F.data.startswith("rename_"))
async def start_rename_pack(callback: CallbackQuery, state: FSMContext):
    """Start pack rename process"""
    pack_name = callback.data[7:]
    messages = await get_messages(user_id=callback.from_user.id)

    try:
        # Verify pack exists
        pack_info = await db.get_pack(callback.from_user.id, pack_name)
        if not pack_info:
            await callback.message.edit_text(messages["pack_not_found"])
            return

        await state.set_state(PackStates.rename_pack)
        await state.update_data(pack_name=pack_name)

        await callback.message.edit_text(
            messages["enter_new_title"],
            **DEFAULT_HTML_OPTIONS
        )
    except Exception as e:
        logging.error("Error starting rename: %s", str(e))
        await callback.message.edit_text(messages["rename_error"])

@router.message(PackStates.rename_pack)
async def process_rename_pack(message: Message, state: FSMContext):
    """Process pack rename"""
    messages = await get_messages(user_id=message.from_user.id)
    data = await state.get_data()
    pack_name = data.get("pack_name")

    try:
        # Update title in Telegram
        me = await message.bot.get_me()
        new_pack_title = f"{message.text} | by @{me.username}"
        await message.bot.set_sticker_set_title(
            name=pack_name,
            title=new_pack_title
        )

        # Update title in database
        success = await db.rename_pack(message.from_user.id, pack_name, new_pack_title)
        if not success:
            raise Exception("Failed to update database")

        await message.answer(messages["pack_renamed"])
        await state.clear()
        # Get updated sticker set and show pack actions
        try:
            sticker_set = await message.bot.get_sticker_set(pack_name)
            await show_pack_actions(
                msg=message,
                sticker_set=sticker_set,
                user_id=message.from_user.id,
                messages=messages,
                edit_message=False
            )
        except Exception as e:
            logging.error("Failed to show pack actions: %s", str(e))

    except Exception as e:
        logging.error("Error renaming pack: %s", str(e))
        await message.answer(messages["rename_error"])
        await state.clear()

@router.callback_query(F.data.startswith("delsticker_"))
async def show_stickers_for_deletion(callback: CallbackQuery, state: FSMContext):
    """Show stickers for deletion"""
    pack_name = callback.data[11:]
    messages = await get_messages(user_id=callback.from_user.id)

    try:
        sticker_set = await callback.bot.get_sticker_set(pack_name)
        if not sticker_set.stickers:
            await callback.message.edit_text(messages["pack_empty"])
            return

        # Create inline keyboard with stickers
        buttons = []
        for i, _ in enumerate(sticker_set.stickers):
            buttons.append([
                InlineKeyboardButton(
                    text=f"Sticker {i+1}",
                    callback_data=f"remove_{pack_name}_{i}"
                )
            ])

        buttons.append([
            InlineKeyboardButton(
                text=messages["back"],
                callback_data=f"pack_{pack_name}"
            )
        ])

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        # Save sticker set data and original message ID to state
        await state.update_data(
            current_pack=pack_name,
            sticker_indices={
                str(i): sticker.file_id
                for i, sticker in enumerate(sticker_set.stickers)
            },
            original_message_id=callback.message.message_id  # Store the message ID
        )

        # Set state for handling sticker messages
        await state.set_state("waiting_for_sticker_to_delete")

        await callback.message.edit_text(
            messages["send_sticker_to_delete"],
            reply_markup=keyboard
        )
    except Exception as e:
        logging.error("Error showing stickers: %s", str(e))
        await callback.message.edit_text(messages["pack_not_found"])

@router.message(F.sticker, StateFilter("waiting_for_sticker_to_delete"))
async def handle_sticker_for_deletion(message: Message, state: FSMContext):
    """Handle sticker sent for deletion"""
    messages = await get_messages(user_id=message.from_user.id)
    data = await state.get_data()

    try:
        # Check if sticker belongs to the current pack
        sticker_indices = data.get("sticker_indices", {})
        pack_name = data.get('current_pack')
        original_message_id = data.get('original_message_id')

        if message.sticker.file_id not in sticker_indices.values():
            await message.reply(messages["wrong_sticker"])
            return

        # Delete from Telegram
        await message.bot.delete_sticker_from_set(message.sticker.file_id)

        # Delete the original sticker list message if we have its ID
        if original_message_id:
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=original_message_id
                )
            except Exception as e:
                logging.error("Failed to delete original message: %s", str(e))

        # Clear state
        await state.clear()

        # Show success notification
        await message.answer(messages["sticker_deleted"])

        # Get sticker set and show pack actions
        sticker_set = await message.bot.get_sticker_set(pack_name)
        await show_pack_actions(
            message,
            sticker_set,
            message.from_user.id,
            messages,
            edit_message=False
        )

    except Exception as e:
        logging.error("Error removing sticker: %s", str(e))
        await message.reply(messages["sticker_delete_error"])
        await state.clear()

@router.callback_query(F.data.startswith("remove_"))
async def remove_sticker(callback: CallbackQuery, state: FSMContext):
    """Remove sticker from pack"""
    parts = callback.data.split('_')
    index = parts[-1]  # Last element is the index

    messages = await get_messages(user_id=callback.from_user.id)

    try:
        # Get data from state
        data = await state.get_data()
        sticker_indices = data.get("sticker_indices", {})
        pack_name = data.get('current_pack')

        # Get sticker file_id using index
        file_id = sticker_indices.get(index)
        if not file_id:
            raise ValueError("Sticker not found")

        # Delete from Telegram
        await callback.bot.delete_sticker_from_set(file_id)

        # First edit the message to show deletion confirmation
        await callback.message.edit_text(messages["sticker_deleted"])

        # Get updated sticker set and show pack actions in a new message
        sticker_set = await callback.bot.get_sticker_set(pack_name)
        await show_pack_actions(
            callback.message,
            sticker_set,
            callback.from_user.id,
            messages,
            edit_message=False
        )

    except Exception as e:
        logging.error("Error removing sticker: %s", str(e))
        await callback.message.edit_text(messages["sticker_delete_error"])

@router.callback_query(F.data == "alert_one_sticker")
async def alert_one_sticker(callback: CallbackQuery):
    """Show alert when trying to delete the last sticker"""
    messages = await get_messages(user_id=callback.from_user.id)
    await callback.answer(
        messages["cant_delete_last_sticker"],
        show_alert=True
    )
