from pathlib import Path

# Root path of the project, making all other paths relative to the project location
PROJECT_ROOT = Path(__file__).parent

# Path to the Tesseract executable
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to the Poppler bin folder
POPPLER_PATH = PROJECT_ROOT / "poppler-25.07.0" / "Library" / "bin"

# Path to the folder with sample invoices
SAMPLES_DIR = PROJECT_ROOT / "samples"
