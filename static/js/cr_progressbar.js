// Récupérer l'élément contenant la probabilité
const progressContainer = document.querySelector('.progress-container');

// Lire la valeur de proba_churn depuis l'attribut data-proba
const probaChurn = parseFloat(progressContainer.dataset.proba);

// Ajuster la largeur de la barre
const progressBar = document.getElementById('progress-bar');
progressBar.style.width = probaChurn + "%";

// Modifier la couleur en fonction de la probabilité
if (probaChurn < 33) {
    progressBar.style.backgroundColor = "green"; // Faible proba
} else if (probaChurn < 66) {
    progressBar.style.backgroundColor = "orange"; // Moyenne proba
} else {
    progressBar.style.backgroundColor = "red"; // Forte proba
}