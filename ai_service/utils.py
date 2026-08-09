"""Utility functions for AI service."""
import cv2
import numpy as np
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)


def load_image_from_file(file_path):
    """
    Load image from file path.
    
    Args:
        file_path: Path to image file
    
    Returns:
        Image array (BGR format) or None if failed
    """
    try:
        image = cv2.imread(file_path)
        if image is None:
            logger.error(f"Failed to load image from {file_path}")
            return None
        return image
    except Exception as e:
        logger.error(f"Error loading image: {str(e)}")
        return None


def load_image_from_bytes(image_bytes):
    """
    Load image from bytes.
    
    Args:
        image_bytes: Image data as bytes
    
    Returns:
        Image array (BGR format) or None if failed
    """
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            logger.error("Failed to decode image from bytes")
            return None
        
        return image
    except Exception as e:
        logger.error(f"Error loading image from bytes: {str(e)}")
        return None


def bgr_to_rgb(image):
    """Convert BGR image to RGB."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def rgb_to_bgr(image):
    """Convert RGB image to BGR."""
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def save_image(image, file_path):
    """
    Save image to file.
    
    Args:
        image: Image array
        file_path: Path to save image
    
    Returns:
        True if successful, False otherwise
    """
    try:
        cv2.imwrite(file_path, image)
        logger.info(f"Image saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        return False


def resize_image(image, max_width=800, max_height=600):
    """
    Resize image while maintaining aspect ratio.
    
    Args:
        image: Image array
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    # Calculate scaling factor
    scale = min(max_width / width, max_height / height, 1.0)
    
    if scale < 1.0:
        new_width = int(width * scale)
        new_height = int(height * scale)
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return image


def validate_image(image):
    """
    Validate image array.
    
    Args:
        image: Image array
    
    Returns:
        True if valid, False otherwise
    """
    if image is None:
        return False
    
    if not isinstance(image, np.ndarray):
        return False
    
    if len(image.shape) != 3:
        return False
    
    if image.shape[2] != 3:
        return False
    
    return True
