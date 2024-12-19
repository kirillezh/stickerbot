"""
This module contains utility functions for the bot.
"""
from src.database.db import Database
from src.localisation.localization_en import MESSAGES as EN_MESSAGES
from src.localisation.localization_ua import MESSAGES as UA_MESSAGES

db = Database()

async def get_messages(state=None, user_id=None):
    """Get localized messages based on user's language preference."""
    if user_id:
        language = await db.get_user_language(user_id)
    else:
        data = await state.get_data()
        language = data.get("language", "ua")

    return EN_MESSAGES if language == "en" else UA_MESSAGES 