import re
import json


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
        
        # Search for "Nome/Razão Social:" followed by the name on the same line.
        r"Nome\s*/\s*Razão Social\s*[:\-]?\s*([^\n]+)",

        # Search for "Nome ou Razão Social:" followed by the name on the same line.
        r"Nome ou Razão Social\s*[:\-]?\s*([^\n]+)",

        # Search for "Nome:" followed by the name on the same line.
        r"Nome\s*[:\-]?\s*([^\n]+)",

        # Search for "Razão Social" and capture the content of the next line.
        r"Razão Social[^\n]*\n\s*([^\n]+)",

        # Search for "Nome/Razão Social" and capture the content of the next line.
        r"Nome\s*/\s*Razão Social[^\n]*\n\s*([^\n]+)"

        # Search for "Nome ou Razão Social" and capture the content of the next line.
        r"Nome ou Razão Social[^\n]*\n\s*([^\n]+)"

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
        print(normalized_text)

        cnpj = find_cnpj(normalized_text)
        razao_social = find_social_reason(normalized_text)

    except ValueError:
        print("WARNING: Section 'Prestador de Serviços' not found. Cannot extract data safely.")
        cnpj = None
        razao_social = None

    dados = {
        "cnpj_prestador": cnpj if cnpj else "Não encontrado",
        "nome_prestador": razao_social if razao_social else "Não encontrado"
    }
    
    return json.dumps(dados, indent=4, ensure_ascii=False)
