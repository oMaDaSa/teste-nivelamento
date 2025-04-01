import requests
from bs4 import BeautifulSoup
import os
import zipfile

URL= "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

DIRETORIO = os.path.dirname(os.path.abspath(__file__))

def baixar_arquivo(url, caminho):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        with open(caminho, 'wb') as arquivo:
            arquivo.write(resposta.content)
        print(f"Arquivo salvo: {caminho}")
    else:
        print(f"Erro ao baixar {caminho}. Código: {resposta.status_code}")


def obter_links_anexos(url):
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    anexos = []
    
    #Encontra todo link de pdf dentro de li's que contenham Anexo_I ou _II 
    anexos = [
        link['href']
        for item in soup.find_all('li')
        for link in item.find_all('a', href=True)
        if any(anexo in link['href'] for anexo in ["Anexo_I", "Anexo_II"]) and link['href'].endswith('.pdf')
    ]
    
    return anexos


def compactar_arquivos(arquivos, nome_zip):
    with zipfile.ZipFile(nome_zip, 'w') as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))
    print(f"Arquivos compactados em: {nome_zip}")


def main():
    links_anexos = obter_links_anexos(URL)
    
    if not links_anexos:
        print("Nenhum anexo encontrado.")
        return
    
    arquivos_baixados = []
    for indice, url_anexo in enumerate(links_anexos, start=1):
        caminho_arquivo = os.path.join(DIRETORIO, f"anexo_{indice}.pdf")
        baixar_arquivo(url_anexo, caminho_arquivo)
        arquivos_baixados.append(caminho_arquivo)
    
    if arquivos_baixados:
        caminho_zip = os.path.join(DIRETORIO, "anexos.zip")
        compactar_arquivos(arquivos_baixados, caminho_zip)


if __name__ == "__main__":
    main()