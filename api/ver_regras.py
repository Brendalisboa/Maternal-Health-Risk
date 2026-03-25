import joblib
from sklearn.tree import export_text

# Carrega o seu modelo treinado
modelo = joblib.load('modelo_risco_materno_cart.pkl')

# Nomes das colunas exatamente na ordem que você treinou
features = ['Age', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate']

# Extrai as regras da árvore em formato de texto
regras = export_text(modelo, feature_names=features)

print("--- REGRAS DE DECISÃO DO MODELO CART ---")
print(regras)