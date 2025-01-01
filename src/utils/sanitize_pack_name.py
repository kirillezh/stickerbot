"""Sanitize pack name"""
import re

def sanitize_pack_name(name: str) -> str:
    """Sanitize pack name"""
    name = name.lower()
    name = re.sub(r'[^a-z0-9_]', '_', name)
    return name[:120]