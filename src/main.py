from pathlib import Path

# Import the functions we created for PDF and image processing
from .extraction.pdf_processor import convert_pdf_to_images
from .extraction.image_processor import extract_text_from_image

from .utils import choose_file
from PIL import Image

# Import the samples directory from our config.py file
from config import SAMPLES_DIR

def main():
    """
    Main function that executes the complete extraction flow.
    """
    # User chooses the file to be processed 
    file_to_process = choose_file()

    if file_to_process is None:
        return
    print(f"File chosen: {file_to_process.name}")

    if file_to_process.suffix == ".pdf":
        print("Processing as PDF...")
        image_pages = convert_pdf_to_images(file_to_process)
        print(f"PDF converted. Total pages: {len(image_pages)}")

    else:
        print("Processing as image...")
        image_pages = [Image.open(file_to_process)]
        print("Image loaded.")

    # Extract text from each image
    print("Starting text extraction from each page...")
    text_complete = []
    for i, page in enumerate(image_pages):
        print(f"Processing page {i + 1}...")
        text_of_page = extract_text_from_image(page)
        text_complete.append(text_of_page)

    # 3. Display the final result
    print("\n--- TEXT EXTRACTED SUCCESSFULLY ---\n")
    for i, text in enumerate(text_complete):
        print(f"--- Page {i + 1} ---\n{text}\n")

if __name__ == "__main__":
    main()
    