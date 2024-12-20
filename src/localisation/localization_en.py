"""
This module contains English language localization messages for the Telegram bot.
All user-facing text messages are stored in the MESSAGES dictionary.
"""

MESSAGES = {
    "start_message": (
        "Hello! \nI'm a small Ukrainian bot that helps users create their own stickers) "
        "\nI hope you like it!)\n"
        "/info - Info about bot\n"
        "/mypacks - My sticker packs\n"
        "/newpack – Create a new sticker pack\n"
        "/newvideopack - Create a video sticker pack\n"
        "/setlanguage - Choose language\n"
        "/cancel - Cancel action"
    ),
    "cancel_message": "Cancelled(",
    "complete_message": (
        "<a href='https://t.me/addstickers/{sticker_set_name}'>{sticker_set_title}</a> new stickers added🥰"
    ),
    "new_pack_prompt": "First, please enter the name of the future sticker pack)",
    "title_too_long": "Please, no more than 30 characters in the title",
    "short_name_prompt": "Enter a short name for the pack (only Latin letters, numbers, and underscores)",
    "name_must_start_with_letter": "The name must start with a letter",
    "name_too_long": "The name must be no more than 15 characters",
    "pack_exists": "Such a pack already exists, choose another name",
    "send_photo": "Send a photo for the first sticker",
    "send_next_photo": "Send a photo for the sticker",
    "send_emoji": "Now send an emoji for this sticker",
    "error_processing_photo": "An error occurred while processing the photo",
    "add_sticker_prompt": (
        "First, please enter the name of the existing sticker pack (it must end with \"_by_{username}\"))"
    ),
    "pack_not_found": "Oops... Couldn't find this sticker pack:(\nMaybe you made a mistake, try again!",
    "pack_full": (
        "Unfortunately, the number of stickers has reached the maximum((\n\n"
        "A pack can have a maximum of 120 stickers, "
        "so I suggest creating a new pack using the /newpack command"
    ),
    "sticker_added": "Added to the pack, you can add more... \nTo stop, type /complete",
    "sticker_add_error": "Error adding sticker",
    "video_convert_error": "Error converting video",
    "video_processing_error": "An error occurred while processing the video",
    "choose_convert_type": "Choose the conversion type:",
    "choose_video_type": "Choose the video sticker type:",
    "send_video_for_conversion": "Send a video for conversion",
    "send_video_note_for_conversion": "Send a video note for conversion",
    "video_sticker_pack_full": (
        "Unfortunately, the number of video stickers has reached the maximum((\n\n"
        "A pack can have a maximum of only 50 video stickers, "
        "so I suggest creating a new pack using the /newvideopack command"
    ),
    "video_sticker_pack_not_video": "This pack is not a video sticker pack. Please choose the correct pack.",
    "video_sticker_pack_empty": "Error: the pack does not contain stickers",
    "bot_no_username": "Error: the bot does not have a username",
    "emoji_error": "Please send a valid emoji",
    "sticker_creation_error": "An error occurred while creating/adding the sticker",
    "selected_pack": "Selected pack <a href='https://t.me/addstickers/{sticker_set_name}'>{sticker_set_title}</a>\n{send_photo}",
    "new_pack_created": (
        "Created new {pack_type}sticker pack "
        "<a href='https://t.me/addstickers/{name}'>"
        "{title}</a>"
    ),
    "video_pack": "video-",
    "static_pack": "",
    "convert_to_round": "🔄 Convert to round",
    "convert_to_video": "🎬 Convert to regular video",
    "video_round": "🔄 Video round",
    "video_normal": "🎬 Regular video",
    "back": "⬅️ Back",
    "choose_language": "Please choose your language:",
    "language_set": "Language set successfully!",
    "language_ukrainian": "🇺🇦 Українська",
    "language_english": "🇬🇧 English",
    "invalid_name_chars": "Name can only contain Latin letters, numbers and underscore",
    "send_video": "Send a video for the sticker",
    "send_video_for_sticker": "Send a video to create a sticker",
    "my_packs": "My sticker packs",
    "no_packs": "You don't have any sticker packs yet, create one using /newpack",
    "page_counter": "Page {current} of {total}",
    "next_page": "Next ➡️",
    "prev_page": "⬅️ Previous",
    "pack_actions": "Actions with pack '{title}':",
    "rename_pack": "✏️ Rename pack ✏️",
    "delete_pack": "❌ Delete pack ❌",
    "delete_pack_button": "⚠️ Delete this pack ⚠️",
    "add_sticker_to_pack": "➕ Add sticker ➕",
    "delete_sticker": "🗑 Delete sticker 🗑",
    "back_to_packs": "↩️ Back to packs",
    "back_to_pack": "↩️ Back to pack",
    "close_actions": "🔒 Close 🔒",
    "closed_actions": "🔒 Closed 🔒",
    "pack_deleted": "Pack successfully deleted",
    "enter_new_title": "Enter new title for the pack:",
    "pack_renamed": "Pack successfully renamed",
    "select_sticker": "Select sticker to delete:",
    "sticker_deleted": "Sticker successfully deleted",
    "rename_error": "Error renaming pack. Please try again.",
    "pack_full_name": "<a href='https://t.me/addstickers/{name}'>{title}</a> | by @{username}",
    "select_sticker_to_delete": "Select sticker to delete from pack {title}:",
    "sticker_delete_error": "Error deleting sticker. Please try again.",
    "send_sticker_to_delete": "Send the sticker you want to delete, or choose from the list below:",
    "wrong_sticker": "This sticker doesn't belong to this pack. Try another one or choose from the list.",
    "confirm_delete_pack": (
        "⚠️ Are you absolutely sure?\n\n"
        "This will permanently delete the pack '{title}' "
        "and all its stickers. This action CANNOT be undone."
    ),
    "confirm_delete_yes": "🗑 Yes, delete this pack",
    "confirm_delete_no": "❌ No, keep it",
    "cant_delete_last_sticker": "Cannot delete the last sticker in the pack! A pack must contain at least two sticker.",
}
