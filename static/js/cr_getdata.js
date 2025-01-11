// Fonction pour récupérer le jeton CSRF depuis le meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Fonction pour envoyer les données
async function sendData() {
    // Numerical values
    const esValue = document.getElementById('es-input').value;
    const balValue = document.getElementById('bal-input').value;
    const csValue = document.getElementById('cs-input').value;
    const ageValue = document.getElementById('age-input').value;
    const tenValue = document.getElementById('ten-input').value;
    const nbValue = document.getElementById('nb-input').value;

    // Categorical Values
    const ccValue = document.getElementById('cc-selector').value;
    const amValue = document.getElementById('am-selector').value;
    const geoValue = document.getElementById('geo-selector').value;
    const genValue = document.getElementById('gen-selector').value;

    const data = {
        esValue: esValue,
        balValue: balValue,
        csValue: csValue,
        ageValue: ageValue,
        tenValue: tenValue,
        nbValue: nbValue,
        ccValue: ccValue === "Yes" ? 1 : 0,
        amValue: amValue === "Yes" ? 1 : 0,
        geoValue: geoValue,
        genValue: genValue,
    };

    try {
        const response = await fetch('/process-input/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), // Ajout du token CSRF
            },
            body: JSON.stringify(data),
        });

        // Vérifiez si la réponse est correcte
        if (response.ok) {
            const result = await response.json();
            const probaChurn = result.proba_churn;

            // Mettre à jour la probabilité et la barre de progression
            document.getElementById('churn-rate-value').innerText = `Churn probability: ${probaChurn}%`;

            const progressBar = document.getElementById('progress-bar');
            progressBar.style.width = probaChurn + '%';

            if (probaChurn < 33) {
                progressBar.style.backgroundColor = 'green';
            } else if (probaChurn < 66) {
                progressBar.style.backgroundColor = 'orange';
            } else {
                progressBar.style.backgroundColor = 'red';
            }
        } else {
            console.error('Failed to fetch data:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error sending data:', error);
    }
}
