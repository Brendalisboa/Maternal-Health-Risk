import pytest
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

# 1. Carrega o modelo oficial exportado
modelo = joblib.load('MachineLearning/models/modelo_risco_materno_cart.pkl')

def test_desempenho_modelo():
    """
    Testa se a acurácia do modelo atende ao requisito mínimo (Threshold)
    lendo os dados de teste reais (Holdout) separados no Google Colab.
    """
    # 2. Carrega os dados reais do CSV (exatamente como a professora fez)
    X_test = pd.read_csv('MachineLearning/data/X_test_risco_materno.csv')
    y_test = pd.read_csv('MachineLearning/data/y_test_risco_materno.csv')
    
    # 3. Faz as predições com os dados do CSV
    previsoes = modelo.predict(X_test)
    
    # 4. Calcula a acurácia (comparando o gabarito y_test com as previsoes)
    acuracia = accuracy_score(y_test, previsoes)
    
    # 5. Define o Threshold (Valor Limite Aceitável de 75%)
    threshold_aceitavel = 0.75 
    
    # 6. A asserção do teste
    assert acuracia >= threshold_aceitavel, f"Acurácia de {acuracia*100:.2f}% está abaixo do limite de {threshold_aceitavel*100}%"