"""
This module initializes and runs the Telegram bot using aiogram.
"""

import asyncio
import logging
from dotenv import load_dotenv
from src.bot import BotInstance
from src.handlers.common import router as common_router
from src.handlers.photo_sticker import router as sticker_router
from src.handlers.video_sticker import router as video_router
from src.handlers.sticker_common import router as sticker_common_router
from src.handlers.pack_management import router as pack_management_router

async def main():
    """
    Main function for running the bot.
    """
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    bot_instance = BotInstance()
    # Bot commands setup
    await bot_instance.setup_commands()
    # Router registration
    bot_instance.dp.include_router(common_router)
    bot_instance.dp.include_router(sticker_common_router)
    bot_instance.dp.include_router(sticker_router)
    bot_instance.dp.include_router(video_router)
    bot_instance.dp.include_router(pack_management_router)
    # Bot startup
    await bot_instance.dp.start_polling(bot_instance.bot)

if __name__ == '__main__':
    asyncio.run(main())