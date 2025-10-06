import re
import json
import pytesseract
from pathlib import Path

from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
from PIL import Image

from django.conf import settings

def normalize_text(texto: str) -> str:
    """
    Normalizes the text by removing extra spaces and empty lines.
    """
    # Divide text in lines 
    lines = texto.splitlines()
    
    # Clean each line
    cleaned_lines = []
    for line in lines:
        # Change multiple spaces to a single space and trim leading/trailing spaces
        normalized_line = re.sub(r'\s+', ' ', line).strip()
        cleaned_lines.append(normalized_line)

    # Remove empty lines
    non_empty_lines = [line for line in cleaned_lines if line]

    # Join the lines back together with a single newline
    return "\n".join(non_empty_lines)

def find_cnpj(text: str) -> str | None:
    """
    Finds the first occurrence of a CNPJ in the given text.
    """
    # Regular Expression (Regex) for the CNPJ pattern
    cnpj_pattern = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"

    match = re.search(cnpj_pattern, text)

    if match:
        return match.group(0)
    return None

def find_social_reason(text: str) -> str | None:
    """
    Finds the social reason (company name) in the given text.
    """
   
    # Patterns list to try in order of priority.
    # [^\n]+ captures one or more characters on the line, avoiding empty results.
    patterns_to_try = [
        # Search for "Razão Social:" followed by the name on the same line.
        r"Razão Social\s*[:\-]?\s*([^\n]+)",
        r"Razao Social\s*[:\-]?\s*([^\n]+)",
        
        # Search for "Nome/Razão Social:" followed by the name on the same line.
        r"Nome\s*/\s*Razão Social\s*[:\-]?\s*([^\n]+)",
        r"Nome\s*/\s*Razao Social\s*[:\-]?\s*([^\n]+)",

        # Search for "Nome ou Razão Social:" followed by the name on the same line.
        r"Nome ou Razão Social\s*[:\-]?\s*([^\n]+)",
        r"Nome ou Razao Social\s*[:\-]?\s*([^\n]+)",

        # Search for "Nome:" followed by the name on the same line.
        r"Nome\s*[:\-]?\s*([^\n]+)",

        # Search for "Razão Social" and capture the content of the next line.
        r"Razão Social[^\n]*\n\s*([^\n]+)",
        r"Razao Social[^\n]*\n\s*([^\n]+)",

        # Search for "Nome/Razão Social" and capture the content of the next line.
        r"Nome\s*/\s*Razão Social[^\n]*\n\s*([^\n]+)",
        r"Nome\s*/\s*Razao Social[^\n]*\n\s*([^\n]+)",

        # Search for "Nome ou Razão Social" and capture the content of the next line.
        r"Nome ou Razão Social[^\n]*\n\s*([^\n]+)",
        r"Nome ou Razao Social[^\n]*\n\s*([^\n]+)",

        # Search for "Nome" and capture the content of the next line.
        r"Nome[^\n]*\n\s*([^\n]+)",
    ]
    
    for pattern in patterns_to_try:
        # Try to find a match with the current pattern
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            # If found, get the result (always in capture group 1)
            social_reason = match.group(1).strip()

            # If the result is not empty, we found what we wanted!
            if social_reason:
                return social_reason

    return None

def parse_data_fiscal(text: str) -> str:
    """
    Parses the fiscal data from the extracted text and returns it as a JSON string.
    """
    try:
        begin_section = text.lower().index("prestador de serviços")
        relevant_text = text[begin_section:]

        end_section = relevant_text.lower().find("tomador de serviços")
        if end_section != -1:
            text_section_prestador = relevant_text[:end_section]
        else:
            text_section_prestador = relevant_text[:500] # Plan B: Take 500 characters

        normalized_text = normalize_text(text_section_prestador)

        cnpj = find_cnpj(normalized_text)
        razao_social = find_social_reason(normalized_text)

    except ValueError:
        print("WARNING: Section 'Prestador de Serviços' not found. Cannot extract data safely.")
        cnpj = None
        razao_social = None

    return {
        "cnpj_prestador": cnpj if cnpj else "Não encontrado",
        "nome_prestador": razao_social if razao_social else "Não encontrado"
    }
    


# --- LÓGICA DE EXTRAÇÃO PRINCIPAL ---
# Import the configurations from our config.py file

# Set the Tesseract path once when the module is imported
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

def extract_text_from_image(image: Image) -> str:
    """
    Extract text from an image object using Tesseract OCR.
    """
    # Add the language to improve accuracy
    text = pytesseract.image_to_string(image, lang='por')
    return text

def convert_pdf_to_images(pdf_path: Path) -> list:
    """
    Convert the pages of a PDF file into a list of image objects.
    """
    print(f"Converting PDF file: {pdf_path.name}...")
    return convert_from_path(pdf_path, poppler_path=settings.POPPLER_PATH)

def choose_file():
    """
    Function able to user choose the file to be processed, PDF or image.
    """
    available_files = [
        f for f in settings.SAMPLES_DIR.iterdir() 
        if f.is_file()
    ]

    for i, file in enumerate(available_files, start=1):
        print(f"[{i}] {file.name}")
        i += 1

    choice = int(input("Enter the number of the file to process: ")) - 1

    if 0 <= choice < len(available_files):
        return available_files[choice]
    else:
        print("Invalid choice. Please try again.")
        return None

def run_extraction_flow(file_path: Path):
    """
    Function that runs the entire extraction process.
    """
    extension = file_path.suffix.lower()

    if extension == '.pdf':
        image_pages = convert_pdf_to_images(file_path)
    elif extension in ['.png', '.jpg', '.jpeg']:
        image_pages = [Image.open(file_path)]
    else:
        raise ValueError(f"Formato de arquivo não suportado: {extension}")

    # Extract text from each image
    text_complete = []
    for i, page in enumerate(image_pages):
        text_of_page = extract_text_from_image(page)
        text_complete.append(text_of_page)

    text_final = "\n".join(text_complete)
    json_result = parse_data_fiscal(text_final)

    return json_result
