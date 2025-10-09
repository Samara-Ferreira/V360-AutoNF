import re

def normalize_text(texto: str) -> str:
    """
    Normaliza o texto removendo espaços extras e linhas em branco, deixando as linhas sem quebra de linhas extras.
    """
    # Divide o texto em linhas
    lines = texto.splitlines()
    
    # Lista para armazenar as linhas limpas
    cleaned_lines = []
    for line in lines:
        # Substitui múltiplos espaços por um único espaço e remove espaços no início/fim da linha específica
        normalized_line = re.sub(r'\s+', ' ', line).strip()
        cleaned_lines.append(normalized_line)

    # Remove linhas vazias
    non_empty_lines = [line for line in cleaned_lines if line]

    # Junta as linhas de volta como um único texto com quebras de linha simples
    joined_text = "\n".join(non_empty_lines)

    return joined_text


def find_cnpj(text: str) -> str | None:
    """
    Encontra a primeira ocorrência de um CNPJ no texto fornecido.
    """
    # Padrão de CNPJ
    cnpj_pattern = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"

    match = re.search(cnpj_pattern, text)

    if match:
        return match.group(0)
    return None


def find_name(text: str) -> str | None:
    """
    Encontra a razão social (nome da empresa) no texto fornecido.
    """
    # Lista de padrões para tentar em ordem de prioridade
    # [^\n]+ captura um ou mais caracteres na linha, evitando resultados vazios
    patterns_to_try = [
        # Busca por "Razão Social:" seguido do nome na mesma linha, com ou sem acento
        r"Razão Social\s*[:\-]?\s*([^\n]+)",
        r"Razao Social\s*[:\-]?\s*([^\n]+)",

        # Busca por "Nome/Razão Social:" seguido do nome na mesma linha, com ou sem acento
        r"Nome\s*/\s*Razão Social\s*[:\-]?\s*([^\n]+)",
        r"Nome\s*/\s*Razao Social\s*[:\-]?\s*([^\n]+)",

        # Busca por "Nome:" seguido do nome na mesma linha
        r"Nome\s*[:\-]?\s*([^\n]+)",

        # Busca por "Razão Social" e captura o conteúdo da próxima linha
        r"Razão Social[^\n]*\n\s*([^\n]+)",
        r"Razao Social[^\n]*\n\s*([^\n]+)",

        # Busca por "Nome" e captura o conteúdo da próxima linha
        r"Nome[^\n]*\n\s*([^\n]+)",

        # Busca por "Nome/Razão Social" e captura o conteúdo da próxima linha
        r"Nome\s*/\s*Razão Social[^\n]*\n\s*([^\n]+)",
        r"Nome\s*/\s*Razao Social[^\n]*\n\s*([^\n]+)",
    ]
    
    for pattern in patterns_to_try:
        # Tenta encontrar uma correspondência com o padrão atual
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            # Se encontrado, obtém o resultado (sempre no grupo de captura 1)
            social_reason = match.group(1).strip()

            # Se o resultado não estiver vazio, encontramos o que queríamos
            if social_reason:
                return social_reason
    return None


def find_email(text: str) -> str | None:
    """
    Encontra a primeira ocorrência de um email no texto fornecido.
    """
    # Padrão de email que aceita '@' ou 'Q' como separador
    email_pattern = r"[a-zA-Z0-9._%+-]+[@Q][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(email_pattern, text)

    if match:
        email_correto = match.group(0).replace('Q', '@').replace('q', '@')
        return email_correto
    return None 


def find_phone(text: str) -> str | None:
    """
    Encontra a primeira ocorrência de um telefone no texto fornecido.
    """
    # Padrão de telefone (formato brasileiro)
    phone_pattern = r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"

    match = re.search(phone_pattern, text)

    if match:
        return match.group(0)
    return None


def parse_data(text: str) -> str:
    """
    Função que analisa o texto extraído para obter dados específicos.
    """
    try:
        begin_section = text.lower().index("prestador de serviços")
        relevant_text = text[begin_section:]

        end_section = relevant_text.lower().find("tomador de serviços")
        if end_section != -1:
            text_section_prestador = relevant_text[:end_section]
        else:
            text_section_prestador = relevant_text[:1000]

        normalized_text = normalize_text(text_section_prestador)

        cnpj = find_cnpj(normalized_text)
        razao_social = find_name(normalized_text)
        email = find_email(normalized_text)
        telefone = find_phone(normalized_text)

    except ValueError:
        print("ALERTA: Seção 'Prestador de Serviços' não encontrada no texto.")
        cnpj = None
        razao_social = None
        email = None
        telefone = None

    return {
        "cnpj_prestador": cnpj if cnpj else "Não encontrado",
        "nome_prestador": razao_social if razao_social else "Não encontrado",
        "email_prestador": email if email else "Não encontrado",
        "telefone_prestador": telefone if telefone else "Não encontrado"
    }
