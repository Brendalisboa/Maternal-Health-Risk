from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from flasgger import Swagger
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Carrega o modelo treinado
modelo = joblib.load('MachineLearning/models/modelo_risco_materno_cart.pkl')

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    """Cria o banco de dados e a tabela caso não existam."""
    conn = sqlite3.connect('historico.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            age REAL,
            systolic_bp REAL,
            diastolic_bp REAL,
            bs REAL,
            body_temp REAL,
            heart_rate REAL,
            risk_level TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco ao ligar o servidor
init_db()
# --------------------------------------

@app.route('/predict', methods=['POST'])
def predict():
    """
    Avaliação de Risco de Saúde Materna
    Esta rota recebe dados fisiológicos da gestante, retorna a classificação de risco e salva no banco de dados.
    ---
    parameters:
      - name: body
        in: body
        required: true
        description: JSON contendo os sinais vitais e métricas da paciente.
        schema:
          type: object
          properties:
            Age:
              type: number
              example: 35
            SystolicBP:
              type: number
              example: 140
            DiastolicBP:
              type: number
              example: 90
            BS:
              type: number
              example: 15.0
            BodyTemp:
              type: number
              example: 98.0
            HeartRate:
              type: number
              example: 80
    responses:
      200:
        description: Previsão realizada com sucesso e salva no histórico.
      400:
        description: Erro na requisição.
    """
    try:
        dados = request.get_json()
        
        # 1. Prepara os dados para o modelo
        df = pd.DataFrame([{
            'Age': float(dados['Age']),
            'SystolicBP': float(dados['SystolicBP']),
            'DiastolicBP': float(dados['DiastolicBP']),
            'BS': float(dados['BS']),
            'BodyTemp': float(dados['BodyTemp']),
            'HeartRate': float(dados['HeartRate'])
        }])
        
        # 2. Faz a predição
        resultado = modelo.predict(df)
        nivel_risco = resultado[0]
        
        # 3. Salva no Banco de Dados
        conn = sqlite3.connect('historico.db')
        cursor = conn.cursor()
        
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO predicoes (data_hora, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data_atual, dados['Age'], dados['SystolicBP'], dados['DiastolicBP'], 
              dados['BS'], dados['BodyTemp'], dados['HeartRate'], nivel_risco))
        
        conn.commit()
        conn.close()
        
        # 4. Retorna a resposta para o Front-end
        return jsonify({'RiskLevel': nivel_risco})

    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# --- ROTAA VER O BANCO DE DADOS ---
@app.route('/history', methods=['GET'])
def history():
    """
    Histórico de Consultas
    Retorna todas as predições salvas no banco de dados SQLite.
    ---
    responses:
      200:
        description: Lista de histórico.
    """
    conn = sqlite3.connect('historico.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predicoes ORDER BY id DESC')
    linhas = cursor.fetchall()
    conn.close()
    
    # Formata a saída para JSON
    historico = []
    for linha in linhas:
        historico.append({
            'id': linha[0],
            'data_hora': linha[1],
            'dados_paciente': f"Idade: {linha[2]}, Pressão: {linha[3]}x{linha[4]}, Glicose: {linha[5]}",
            'risco_calculado': linha[8]
        })
        
    return jsonify(historico)

if __name__ == '__main__':
    app.run(debug=True, port=5000)