from pathlib import Path
from pdf2image import convert_from_path

from django.conf import settings

def convert_pdf_to_images(pdf_path: Path) -> list:
    """
    Converte as páginas de um arquivo PDF em uma lista de objetos de imagem.
    """
    file_converted = convert_from_path(pdf_path, poppler_path=settings.POPPLER_PATH)
    return file_converted
