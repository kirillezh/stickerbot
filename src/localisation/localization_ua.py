"""
This module contains Ukrainian language localization messages for the Telegram bot.
All user-facing text messages are stored in the MESSAGES dictionary.
"""

MESSAGES = {
    "start_message": (
        "Привіт! \nЯ маленький український бот, що допомогає користувачам створювати свої наліпки) "
        "\nСподіваюсь, Вам сподобається!)\n"
        "/info - Інфо про бота\n"
        "/mypacks - Мої паки наліпок\n"
        "/newpack – Створюю новий пак наліпок\n"
        "/newvideopack - Створюю відео-стікерпак\n"
        "/setlanguage - Вибрати мову\n"
        "/cancel - Скасувати дію"
    ),
    "cancel_message": "Скасовано(",
    "complete_message": (
        "<a href='https://t.me/addstickers/{sticker_set_name}'>{sticker_set_title}</a> додано нові наліпки🥰"
    ),
    "new_pack_prompt": "Спочатку, будь ласка, введи назву майбутнього паку наліпок)",
    "title_too_long": "Будь ласка, не більше 30 символів у назві",
    "short_name_prompt": "Введіть коротку назву для паку (тільки латинські літери, цифри та підкреслення)",
    "name_must_start_with_letter": "Назва повинна починатися з літери",
    "name_too_long": "Назва повинна бути не більше 15 символів",
    "pack_exists": "Такий пак вже існує, виберіть іншу назву",
    "send_photo": "Відправте фото для першої наліпки",
    "send_next_photo": "Відправте фото для наліпки",
    "send_emoji": "Тепер відправте емодзі для цього стікера",
    "error_processing_photo": "Сталася помилка при обробці фото",
    "add_sticker_prompt": (
        "Спочатку, будь ласка, введи назву існуючого паку наліпок(необхідно, щоб він закінчувався на \"_by_{username}\"))"
    ),
    "pack_not_found": "Упс... Не знайшов цього паку наліпок:(\nМожливо Ви допустили помилку, спробуйте ще!",
    "pack_full": (
        "Нажаль, кількість наліпок досягла максимуму((\n\n"
        "У одному паку може бути максимум 120 наліпок, "
        "тому пропоную створити новий пак за допомогою команди /newpack"
    ),
    "sticker_added": "Додано до паку, ви можете додавати ще... \nЩоб зупинитись, напишіть /complete",
    "sticker_add_error": "Помилка при додаванні стікера",
    "video_convert_error": "Помилка при конвертації відео",
    "video_processing_error": "Сталася помилка при обробці відео",
    "choose_convert_type": "Оберіть тип конвертації:",
    "choose_video_type": "Оберіть тип відео-стікера:",
    "send_video_for_conversion": "Відправте відео для конвертації",
    "send_video_note_for_conversion": "Відправте відео-кружечок для конвертації",
    "video_sticker_pack_full": (
        "Нажаль, кількість відео-наліпок досягла максимуму((\n\n"
        "У одному паку може бути максимум лише 50 відео-наліпок, "
        "тому пропоную створити один пак за допомогою команди /newvideopack"
    ),
    "video_sticker_pack_not_video": "Цей пак не є відео-стікерпаком. Будь ласка, виберіть правильний пак.",
    "video_sticker_pack_empty": "Помилка: пак не містить стікерів",
    "bot_no_username": "Помилка: бот не має username",
    "emoji_error": "Будь ласка, відправте правильний емодзі",
    "sticker_creation_error": "Сталася помилка при створенні/додаванні стікера",
    "selected_pack": "Обрано пак <a href='https://t.me/addstickers/{sticker_set_name}'>{sticker_set_title}</a>\n{send_photo}",
    "new_pack_created": (
        "Створено новий {pack_type}стікерпак "
        "<a href='https://t.me/addstickers/{name}'>"
        "{title}</a>"
    ),
    "video_pack": "відео-",
    "static_pack": "",
    "convert_to_round": "🔄 Конвертувати в кружечок",
    "convert_to_video": "🎬 Конвертувати в звичайне відео",
    "video_round": "🔄 Відео-кружечок",
    "video_normal": "🎬 Звичайне відео",
    "back": "⬅️ Назад",
    "choose_language": "Будь ласка, оберіть вашу мову:",
    "language_set": "Мову успішно встановлено!",
    "language_ukrainian": "🇺🇦 Українська",
    "language_english": "🇬🇧 English",
    "invalid_name_chars": "Назва може містити тільки латинські літери, цифри та знак підкреслення",
    "send_video": "Відправте відео для стікера",
    "send_video_for_sticker": "Відправте відео для створення стікера",
    "my_packs": "Мої стікерпаки",
    "no_packs": "У вас ще немає стікерпаків, створіть один за допомогою команди /newpack",
    "page_counter": "Сторінка {current} з {total}",
    "next_page": "Наступна ➡️",
    "prev_page": "⬅️ Попередня",
    "pack_actions": "Дії з паком '{title}':",
    "rename_pack": "✏️ Перейменувати пак ✏️",
    "delete_pack": "❌ Видалити пак ❌",
    "delete_pack_button": "⚠️ Видалити цей пак ⚠️",
    "add_sticker_to_pack": "➕ Додати стікер ➕",
    "delete_sticker": "🗑 Видалити стікер 🗑",
    "back_to_packs": "↩️ До паку",
    "back_to_pack": "↩️ До паку",
    "close_actions": "🔒 Закрити 🔒",
    "closed_actions": "🔒 Закрито 🔒",
    "pack_deleted": "Пак успішно видалено",
    "enter_new_title": "Введіть нову назву для паку:",
    "pack_renamed": "Пак успішно перейменовано",
    "select_sticker": "Виберіть стікер для видалення:",
    "sticker_deleted": "Стікер успішно видалено",
    "rename_error": "Помилка перейменування паку. Будь ласка, спробуйте ще раз.",
    "pack_full_name": "<a href='https://t.me/addstickers/{name}'>{title}</a> | by @{username}",
    "select_sticker_to_delete": "Оберіть стікер для видалення з паку {title}:",
    "sticker_delete_error": "Помилка при видаленні стікера. Будь ласка, спробуйте ще раз.",
    "send_sticker_to_delete": "Відправте стікер, який хочете видалити, або оберіть зі списку нижче:",
    "wrong_sticker": "Цей стікер не належить до цього паку. Спробуйте інший або оберіть зі списку.",
    "confirm_delete_pack": (
        "⚠️ Ви абсолютно впевнені?\n\n"
        "Це назавжди видалить пак '{title}' "
        "та всі його стікери. Цю дію НЕ МОЖНА буде скасувати."
    ),
    "confirm_delete_yes": "🗑 Так, видалити цей пак",
    "confirm_delete_no": "❌ Ні, залишити",
    "cant_delete_last_sticker": "Не можна видалити останній стікер у паку! Пак повинен містити принаймні два стікери.",
}
