from pathlib import Path
from pdf2image import convert_from_path

# Import the configurations from our config.py file
from config import POPPLER_PATH

def convert_pdf_to_images(pdf_path: Path) -> list:
    """
    Convert the pages of a PDF file into a list of image objects.
    """
    print(f"Converting PDF file: {pdf_path.name}...")
    return convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
