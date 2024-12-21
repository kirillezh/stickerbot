"""
This module contains utility functions for working with messages.
"""
from aiogram.types import LinkPreviewOptions

DEFAULT_HTML_OPTIONS = {
    "parse_mode": "HTML",
    "link_preview_options": LinkPreviewOptions(is_disabled=True)
}
