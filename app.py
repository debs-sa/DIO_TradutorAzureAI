# Instalação das dependências
!pip install requests beautifulsoup4 openai langchain-openai python-dotenv
!pip install langchain openai

# Importando as bibliotecas
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from langchain_openai import AzureChatOpenAI

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

# Parte 1 - Função de Web Scraping
def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        texto = soup.get_text(separator=" ")
        linhas = (line.strip() for line in texto.splitlines())  
        texto_limpo = '\n'.join(line for line in linhas if line) 
        return texto_limpo
    else:
        print(f"Failed to fetch the URL. Status code: {response.status_code}")
        return None

# Testando a função
url = 'https://dev.to/marksantiago02/how-to-write-ico-smart-contract-using-solidity-and-hardhat-4pmg'
texto_extraido = extract_text_from_url(url)
if texto_extraido:
    print(texto_extraido)

# Parte 2 - Função de Tradução
client = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    max_retries=0
)

def translate_article(text, lang):
    messages = [
        ("system" , "Você atua como tradutor de textos"),
        ("user" , f"Traduza o {text} para o idioma {lang} e responda em markdown")
    ]
    response = client.invoke(messages)
    print(response.content)
    return response.content

translate_article("Let's see if the deployment was succeeded." , "portugues")

# Parte 3 - Combinando Web Scraping e Tradução
url = "https://dev.to/0thtachi/build-a-fast-and-lightweight-rust-vector-search-app-with-rig-lancedb-57h2"
texto_extraido = extract_text_from_url(url)
article = translate_article(texto_extraido , "pt-br")
print(article)
