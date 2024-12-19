"""
This module contains the StringGenerator class for generating random strings.
"""
import random
import string

def get_random_string(length: int) -> str:
    """Generate a random string of a given length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length)) 