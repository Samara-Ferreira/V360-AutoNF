# AutoNF V360 Extractor 🚀

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2+-green?logo=django)
![React](https://img.shields.io/badge/React-18+-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.2+-blue?logo=typescript)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Solução full-stack para automação da extração de dados (CNPJ e Razão Social) de documentos fiscais em PDF ou imagem.

---

## 💡 Sobre o Projeto

Este projeto foi desenvolvido como solução para o **Desafio V360**, com o objetivo de automatizar o processo manual e repetitivo de extração de dados de notas fiscais. A aplicação consiste em um backend REST API construído com **Django** e um frontend interativo em **React** e **TypeScript**.

## ✨ Funcionalidades Principais

-   **🖥️ Interface Web Intuitiva:** Faça upload de arquivos ou selecione exemplos diretamente pelo navegador.
-   **📄 Suporte a Múltiplos Formatos:** Processa tanto arquivos **PDF** quanto de **Imagem** (`.png`, `.jpg`, etc.).
-   **🧠 Extração Inteligente:** Utiliza OCR (Tesseract) e lógica de parsing para localizar e extrair com precisão os dados do **Prestador de Serviço**.
-   **💾 Persistência de Dados:** Os resultados de cada extração são salvos em um banco de dados para consulta.
-   **⚡ Resposta em JSON:** Retorna os dados extraídos em um formato JSON limpo, pronto para integrações.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
| :--- | :--- |
| **Backend** | Python, Django, Django REST Framework, Pytesseract |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS, Axios, Lucide React |
| **Banco de Dados** | SQLite 3 (padrão do Django) |
| **Dependências Externas** | Poppler (para conversão de PDF), Tesseract OCR |

## 🚀 Começando

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos
-   [**Python 3.11+**](https://www.python.org/downloads/)
-   [**Node.js 18+**](https://nodejs.org/en/) (que inclui o npm)
-   [**Git**](https://git-scm.com/downloads/)
-   **Tesseract OCR:** É necessário ter o executável instalado no seu sistema. [Instalador para Windows](https://github.com/UB-Mannheim/tesseract/wiki).

### Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/V360-AutoNF.git](https://github.com/seu-usuario/V360-AutoNF.git)
    cd V360-AutoNF
    ```

2.  **Configure o Backend:**
    ```bash
    # Navegue para a pasta do backend
    cd backend

    # Crie e ative o ambiente virtual (PowerShell)
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

    # Instale as dependências do Python
    pip install -r requirements.txt

    # Aplique as migrações do banco de dados
    python manage.py migrate
    ```

3.  **Configure o Frontend:**
    ```bash
    # Volte para a raiz e vá para a pasta do frontend
    cd ..\frontend 
    # Ou 'cd ../frontend' em outros terminais

    # Instale as dependências do Node.js
    npm install
    ```

4.  **Execute a Aplicação:**
    Você precisará de **dois terminais** abertos.

    * **Terminal 1 (Backend):**
        ```bash
        # A partir da pasta 'V360-AutoNF/backend'
        python manage.py runserver
        ```
        O backend estará rodando em `http://127.0.0.1:8000`.

    * **Terminal 2 (Frontend):**
        ```bash
        # A partir da pasta 'V360-AutoNF/frontend'
        npm run dev
        ```
        O frontend estará acessível em `http://localhost:5173` (ou outra porta indicada no terminal).

## ⚙️ Configuração Adicional

-   **Tesseract e Poppler:** Os caminhos para os executáveis do Tesseract e do Poppler estão no arquivo `backend/api_root/settings.py`. Ajuste-os se necessário para o seu sistema. O repositório já inclui os binários do Poppler para Windows.
-   **Variáveis de Ambiente (Backend):** Para produção, é recomendado criar um arquivo `.env` na pasta `backend/` para configurar a `SECRET_KEY` e outras variáveis.

## 🤝 Contribuição

Contribuições são bem-vindas! Para melhorias, correções de bugs ou atualizações, por favor, abra uma *Issue* para discussão ou envie um *Pull Request*.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Contato

**Samara Ferreira**

---
*Obrigado por usar o AutoNF V360!*