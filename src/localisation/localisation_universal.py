"""
This module contains English/Ukrainian language localization messages for the Telegram bot.
All user-facing text messages are stored in the BOT_COMMANDS dictionary.
"""
COMPONENTS_HTML = {
    "link": {
        "simple": "<a href='{link}'>{text}</a>",
        "sticker_set": (
            "<a href='https://t.me/addstickers/{name}'>"
            "{title}</a>"
        )
    }
}

BOT_COMMANDS = {
    "ua": {
        "start": "Старт",
        "info": "Інфо про бота",
        "mypacks": "Мої паки наліпок",
        "newpack": "Створити новий пак наліпок",
        "newvideopack": "Створити відео-стікерпак",
        "cancel": "Скасувати поточну дію",
        "setlanguage": "Вибрати мову"
    },
    "en": {
        "start": "Start",
        "info": "Info about bot",
        "mypacks": "My sticker packs",
        "newpack": "Create new sticker pack",
        "newvideopack": "Create video sticker pack",
        "cancel": "Cancel current action",
        "setlanguage": "Choose language"
    }

}
