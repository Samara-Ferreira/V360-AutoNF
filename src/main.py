from pathlib import Path

# Import the functions we created for PDF and image processing
from .extraction.pdf_processor import convert_pdf_to_images
from .extraction.image_processor import extract_text_from_image

from .utils import choose_file
from PIL import Image
from .parsing.data_parser import parse_data_fiscal

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

    if file_to_process.suffix == ".pdf":
        image_pages = convert_pdf_to_images(file_to_process)

    else:
        image_pages = [Image.open(file_to_process)]

    # Extract text from each image
    text_complete = []
    for i, page in enumerate(image_pages):
        text_of_page = extract_text_from_image(page)
        text_complete.append(text_of_page)


    # Test: Print the raw extracted text
    text_final = "\n".join(text_complete)
    json_result = parse_data_fiscal(text_final)
    print("\n--- EXTRACTED DATA (JSON) ---\n")
    print(json_result)


if __name__ == "__main__":
    main()
    