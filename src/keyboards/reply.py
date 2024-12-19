"""
This module contains keyboard classes for the Telegram bot.
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from src.utils.utils import get_messages

class Keyboards:
    """Class for creating keyboards"""
    @staticmethod
    async def get_convert_keyboard(state=None, user_id=None) -> ReplyKeyboardMarkup:
        """Get keyboard for converting video to round or normal"""
        messages = await get_messages(state=state, user_id=user_id)
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=messages["convert_to_round"]),
                    KeyboardButton(text=messages["convert_to_video"])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    @staticmethod
    async def get_video_type_keyboard(state=None, user_id=None) -> ReplyKeyboardMarkup:
        """Get keyboard for selecting video type"""
        messages = await get_messages(state=state, user_id=user_id)
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=messages["video_round"]),
                    KeyboardButton(text=messages["video_normal"])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    @staticmethod
    async def get_video_back_keyboard(state=None, user_id=None) -> ReplyKeyboardMarkup:
        """Get keyboard for going back"""
        messages = await get_messages(state=state, user_id=user_id)
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=messages["back"])]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    @staticmethod
    async def get_language_keyboard(state=None, user_id=None) -> ReplyKeyboardMarkup:
        """Get keyboard for selecting language"""
        messages = await get_messages(state=state, user_id=user_id)
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=messages["language_ukrainian"]),
                    KeyboardButton(text=messages["language_english"])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True) 

    @staticmethod
    async def get_packs_keyboard(packs, current_page, total_pages, user_id):
        """Generate keyboard for packs"""
        messages = await get_messages(user_id=user_id)
        buttons = []
        
        # Calculate slice indices for current page
        start_idx = (current_page - 1) * 10
        end_idx = start_idx + 10
        current_packs = packs[start_idx:end_idx]
        
        # Add pack buttons
        for pack in current_packs:
            buttons.append([InlineKeyboardButton(
                text=pack.title,
                callback_data=f"pack_{pack.name}"
            )])
        
        # Add navigation buttons if needed
        nav_buttons = []
        if current_page > 1:
            nav_buttons.append(InlineKeyboardButton(
                text=messages["prev_page"],
                callback_data=f"page_{current_page-1}"
            ))
        if current_page < total_pages:
            nav_buttons.append(InlineKeyboardButton(
                text=messages["next_page"],
                callback_data=f"page_{current_page+1}"
            ))
        
        if nav_buttons:
            buttons.append(nav_buttons)
        
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    async def get_pack_actions_keyboard(pack_name: str, user_id: int) -> InlineKeyboardMarkup:
        """Get keyboard with pack actions"""
        messages = await get_messages(user_id=user_id)
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=messages["rename_pack"],
                                callback_data=f"rename_{pack_name}")],
            [InlineKeyboardButton(text=messages["add_sticker_to_pack"],
                                callback_data=f"add_{pack_name}")],
            [InlineKeyboardButton(text=messages["delete_sticker"],
                                callback_data=f"delsticker_{pack_name}")],
            [InlineKeyboardButton(text=messages["back_to_packs"],
                                callback_data="back_to_packs")],
            [InlineKeyboardButton(text=messages["delete_pack"],
                                callback_data=f"delete_{pack_name}")]
        ])

    @staticmethod
    async def get_confirm_delete_keyboard(pack_name: str, user_id: int) -> InlineKeyboardMarkup:
        """Get keyboard for confirming pack deletion"""
        messages = await get_messages(user_id=user_id)
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=messages["confirm_delete_yes"], 
                                callback_data=f"confirmdelete_{pack_name}")],
            [InlineKeyboardButton(text=messages["confirm_delete_no"], 
                                callback_data=f"pack_{pack_name}")],
            [InlineKeyboardButton(text=messages["back_to_packs"], 
                                callback_data="back_to_packs")]
        ])