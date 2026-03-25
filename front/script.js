document.getElementById('riskForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Elementos da tela que vamos manipular
    const btnSubmit = document.getElementById('btnSubmit');
    const resultadoContainer = document.getElementById('resultadoContainer');
    const resultadoTexto = document.getElementById('resultadoTexto');

    // 1. Estado de "Loading" (Carregando)
    btnSubmit.innerText = "Analisando dados...";
    btnSubmit.disabled = true; 
    resultadoContainer.classList.add('hidden'); 
    resultadoTexto.className = ''; 

    // Captura os valores digitados pelo usuário (Padrão BR)
    let glicoseBR = parseFloat(document.getElementById('BS').value);
    let temperaturaBR = parseFloat(document.getElementById('BodyTemp').value);

    // 2. Conversão invisível para o padrão internacional (que o modelo exige)
    let glicoseInternacional = glicoseBR / 18.0;
    let temperaturaInternacional = (temperaturaBR * 1.8) + 32.0;

    // Monta o pacote de dados para enviar à API local
    const dados = {
        Age: document.getElementById('Age').value,
        SystolicBP: document.getElementById('SystolicBP').value,
        DiastolicBP: document.getElementById('DiastolicBP').value,
        BS: glicoseInternacional.toFixed(2), // Envia convertido para mmol/L!
        BodyTemp: temperaturaInternacional.toFixed(2), // Envia convertido para Fahrenheit!
        HeartRate: document.getElementById('HeartRate').value
    };

    try {
        // Envia para o Back-end (Flask)
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const result = await response.json();

        if (response.ok) {
            // Pega o resultado original do modelo e converte para minúsculo
            let nivelRiscoOriginal = result.RiskLevel.toLowerCase(); 
            
            // 3. Tradução e Cores Dinâmicas
            if (nivelRiscoOriginal.includes('high')) {
                resultadoTexto.innerText = "ALTO RISCO";
                resultadoTexto.classList.add('risk-high');
            } else if (nivelRiscoOriginal.includes('mid')) {
                resultadoTexto.innerText = "MÉDIO RISCO";
                resultadoTexto.classList.add('risk-mid');
            } else if (nivelRiscoOriginal.includes('low')) {
                resultadoTexto.innerText = "BAIXO RISCO";
                resultadoTexto.classList.add('risk-low');
            } else {
                resultadoTexto.innerText = result.RiskLevel.toUpperCase();
            }

        } else {
            resultadoTexto.innerText = `Erro: ${result.erro}`;
            resultadoTexto.classList.add('risk-high'); 
        }
    } catch (error) {
        resultadoTexto.innerText = "Erro ao conectar com o servidor. A API está rodando?";
        resultadoTexto.classList.add('risk-high');
    } finally {
        // Tira o Loading e mostra o resultado final
        btnSubmit.innerText = "Avaliar Risco";
        btnSubmit.disabled = false;
        resultadoContainer.classList.remove('hidden');
    }
});