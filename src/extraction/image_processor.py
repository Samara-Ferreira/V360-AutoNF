import pytesseract
from PIL.Image import Image # Import because we are using PIL images

# Import the configurations from our config.py file
from config import TESSERACT_CMD

# Set the Tesseract path once when the module is imported
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text_from_image(image: Image) -> str:
    """
    Extract text from an image object using Tesseract OCR.
    """
    # Add the language to improve accuracy
    text = pytesseract.image_to_string(image, lang='por')
    return text
