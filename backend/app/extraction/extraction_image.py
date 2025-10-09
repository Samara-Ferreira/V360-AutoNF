from PIL import Image
import pytesseract

from django.conf import settings

# Caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

def extract_text_from_image(image: Image) -> str:
    """
    Extração do texto de um objeto de imagem usando Tesseract OCR.
    """
    # Adicionado o idioma local para melhorar a acurácia
    text = pytesseract.image_to_string(image, lang='por')
    return text
