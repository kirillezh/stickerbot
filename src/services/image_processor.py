"""
This module contains the ImageProcessor class for processing images.
"""
import os
import logging
from typing import Tuple
from PIL import Image

class ImageProcessor:
    """Class for image processing"""
    @staticmethod
    def resize_image(file: str, size: Tuple[int, int] = (512, 512)) -> None:
        """Resize image to 512x512"""
        try:
            original_image = Image.open(file)
            width, height = original_image.size
            rel = max(width, height) / 512
            width = int(width / rel)
            height = int(height / rel)
            size = (width, height)
            resized_image = original_image.resize(size)
            resized_image.save(file)
        except Exception as e:
            os.remove(file)
            logging.warning('Error at %s', 'division', exc_info=e) 