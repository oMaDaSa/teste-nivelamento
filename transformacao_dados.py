import pdfplumber
import pandas as pd
import zipfile
import os

DIRETORIO = os.path.abspath(os.path.dirname(__file__))
PDF = os.path.join(DIRETORIO, "anexo_1.pdf")

def extrair_tabelas_do_pdf(caminho_pdf):
    tabelas = []
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for indice, pagina in enumerate(pdf.pages):
                if indice >= 2:  # Ignora as duas primeiras páginas
                    tabela = pagina.extract_table()
                    if tabela:
                        tabelas.extend(tabela)
    except Exception as erro:
        print(f"Erro ao extrair tabelas do PDF: {erro}")
    return tabelas


def processar_dados(tabelas):
    if not tabelas:
        print("Nenhuma tabela encontrada no PDF.")
        return None
    
    try:
        df = pd.DataFrame(tabelas[1:], columns=tabelas[0])  # Primeira linha é o cabeçalho
    except Exception as erro:
        print(f"Erro ao criar DataFrame: {erro}")
        return None
    
    substituicoes = {
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial",
        "HCO": "Seg. Hospitalar Com Obstetrícia",
        "HSO": "Seg. Hospitalar Sem Obstetrícia",
        "REF": "Plano Referência"
    }
    
    #Alterar as siglas pelos nomes
    df.columns = [substituicoes.get(col, col) for col in df.columns]
    df.replace(substituicoes, inplace=True)
    return df


def salvar_csv(df, nome_arquivo):
    df.to_csv(nome_arquivo, index=False)
    print(f"Dados salvos em {nome_arquivo}.")


def compactar_arquivo(arquivo, nome_zip):
    with zipfile.ZipFile(nome_zip, 'w') as zipf:
        zipf.write(arquivo, os.path.basename(arquivo))
    print(f"CSV compactado em {nome_zip}.")


def main():
    if not os.path.exists(PDF):
        print(f"Erro: O arquivo PDF '{PDF}' não foi encontrado.")
        return
    
    tabelas = extrair_tabelas_do_pdf(PDF)
    df = processar_dados(tabelas)
    
    if df is not None:
        csv_path = os.path.join(DIRETORIO, "tabela_rol.csv")
        zip_path = os.path.join(DIRETORIO, "Teste_Matheus_Dantas_Santana.zip")
        
        salvar_csv(df, csv_path)
        compactar_arquivo(csv_path, zip_path)


if __name__ == "__main__":
    main()
