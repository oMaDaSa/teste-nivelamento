from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Relatorio_cadop.csv")

try:
    try:
        df_operadoras = pd.read_csv(CSV_PATH, encoding='utf-8-sig', sep=';')  
    except UnicodeDecodeError:
        df_operadoras = pd.read_csv(CSV_PATH, encoding='latin1', sep=';')

    # Substituir NaN e strings 'nan'/'NaN' por None
    df_operadoras = df_operadoras.astype(str) 
    df_operadoras = df_operadoras.replace({'nan': None, 'NaN': None, 'NAN': None, 'None': None}, regex=True)
    df_operadoras = df_operadoras.where(pd.notnull(df_operadoras), None)

    print("CSV carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o CSV: {e}")
    df_operadoras = pd.DataFrame()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Parâmetro q é obrigatório."}), 400

    if df_operadoras.empty:
        return jsonify({"error": "Dados do CSV não foram carregados corretamente."}), 500

    try:
        results = df_operadoras[
            df_operadoras.apply(
                lambda row: any(query in str(cell).lower() for cell in row if cell not in [None, 'None', 'nan']),
                axis=1
            )
        ]

        # Converter para JSON
        json_results = results.replace({pd.NA: None}).to_dict(orient='records')

        return jsonify(json_results)
    except Exception as e:
        return jsonify({"error": "Erro na busca"}), 500

if __name__ == '__main__':
    app.run(debug=True)
