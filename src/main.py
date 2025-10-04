from pathlib import Path

# Import the functions we created for PDF and image processing
from .extraction.pdf_processor import convert_pdf_to_images
from .extraction.image_processor import extract_text_from_image

# Import the samples directory from our config.py file
from config import SAMPLES_DIR

def main():
    """
    Main function that executes the complete extraction flow.
    """
    # Define the PDF file we want to process
    pdf_file = SAMPLES_DIR / "NFSe_ficticia_layout_completo.pdf"

    # 1. Convert the PDF to images
    paginas_imagem = convert_pdf_to_images(pdf_file)
    print(f"PDF converted. Total pages: {len(paginas_imagem)}")

    # 2. Extract text from each image
    print("Starting text extraction from each page...")
    texto_completo = []
    for i, pagina in enumerate(paginas_imagem):
        print(f"Processing page {i + 1}...")
        texto_da_pagina = extract_text_from_image(pagina)
        texto_completo.append(texto_da_pagina)

    # 3. Display the final result
    print("\n--- TEXT EXTRACTED SUCCESSFULLY ---\n")
    for i, texto in enumerate(texto_completo):
        print(f"--- Page {i + 1} ---\n{texto}\n")

if __name__ == "__main__":
    main()