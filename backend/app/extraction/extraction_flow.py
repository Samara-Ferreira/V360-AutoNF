from pathlib import Path
from PIL import Image

from .extraction_pdf import convert_pdf_to_images
from .extraction_image import extract_text_from_image 
from .parse_data import parse_data


def run_extraction_flow(file_path: Path):
    """
    Função que executa o fluxo completo da extração de dados.
    """
    extension = file_path.suffix.lower()

    if extension == '.pdf':
        image_pages = convert_pdf_to_images(file_path)
    elif extension in ['.png', '.jpg', '.jpeg']:
        # Abrir a imagem como um objeto Image, que é o formato esperado pela função de extração de texto
        image_pages = [Image.open(file_path)] 
    else:
        raise ValueError(f"Formato de arquivo não suportado: {extension}")

    # Extrair texto de uma ou mais imagens (se for um PDF com várias páginas)
    text_complete = []
    for i, page in enumerate(image_pages):
        text_of_page = extract_text_from_image(page)
        text_complete.append(text_of_page)

    text_final = "\n".join(text_complete)

    # Analisar o texto extraído para obter os dados específicos
    json_result = parse_data(text_final)

    return json_result
