# MVP - Sistema de Classificação de Risco Materno 

Este projeto é um Produto Mínimo Viável (MVP) desenvolvido como requisito para as disciplinas de **Engenharia de Sistemas de Software Inteligentes**

O objetivo da aplicação é prever o nível de risco gestacional (Baixo, Médio ou Alto Risco) com base em métricas fisiológicas e sinais vitais das pacientes, auxiliando profissionais de saúde na triagem e tomada de decisão.

## Arquitetura e Tecnologias
O projeto foi construído utilizando uma arquitetura Full Stack simples:
* **Front-end:** Interface web construída com HTML, CSS e JavaScript puro para a entrada de dados dos sinais vitais.
* **Back-end (API):** Desenvolvido em **Python** com o microframework **Flask**, servindo como ponte entre a interface e o modelo preditivo.
* **Banco de Dados:** **SQLite** utilizado para persistência do histórico de pacientes triadas.
* **Machine Learning:** Modelo preditivo treinado e exportado utilizando **Scikit-Learn** e `joblib`.
* **Testes Automatizados:** Cobertura de testes de API e desempenho de modelo utilizando **PyTest**.

## Ciência de Dados e Machine Learning
O modelo preditivo foi treinado no Google Colab. Foram avaliados quatro algoritmos clássicos (KNN, Árvore de Decisão, Naive Bayes e SVM) submetidos a técnicas de transformação de dados (Padronização e Normalização) dentro de estruturas de *Pipelines*.

Após a Validação Cruzada e Otimização de Hiperparâmetros (GridSearchCV), a **Árvore de Classificação (CART)** obteve o melhor desempenho (Acurácia de 98.15%), sendo o modelo exportado (`.pkl`) e embarcado na API.
* **Link para o Google Colab:** [https://colab.research.google.com/drive/1pqi2cwkF5Qt_B_fnOIRRPsczy_rbfWR9?usp=sharing]


## Como Executar o Projeto

1. Clone o repositório:
git clone [https://raw.githubusercontent.com/Brendalisboa/Maternal-Health-Risk/main/Maternal_Risk.csv]

2. Instale as dependências:
Certifique-se de ter o Python instalado. É recomendada a criação de um ambiente virtual.
pip install -r requirements.txt

3. Execute a API (Back-end):
python app.py

A documentação interativa da API (Swagger) estará disponível e pronta para testes no navegador através do endereço: http://127.0.0.1:5000/apidocs/

4. Execute o Front-end:
Basta abrir o arquivo index.html diretamente no seu navegador.

# Testes Automatizados
O projeto conta com testes automatizados para garantir a estabilidade da API e o desempenho do modelo de Machine Learning.

Para rodar os testes, acesse o diretório da api pelo terminal e execute:
pytest
O teste test_desempenho_modelo garante que o modelo em produção possua uma acurácia mínima aceitável (Threshold) superior a 75%.

# Vídeo de Apresentação

Link para o vídeo no YouTube: https://www.youtube.com/watch?v=OjV4umPv6-E
---
